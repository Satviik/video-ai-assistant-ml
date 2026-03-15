import json
import math
import os
import re
from typing import Any, Dict, List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.services.retrieval_service import extract_timestamp


TRANSCRIPTS_DIR = os.path.join("data", "transcripts")
VECTOR_DB_DIR = os.path.join("data", "vector_db")


_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
_VECTOR_DB_NAME = "FAISS"


_embedding_model = SentenceTransformer(_EMBEDDING_MODEL_NAME)


def _load_transcript_segments(video_id: str) -> List[Dict[str, Any]]:

    path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.json")

    if not os.path.exists(path):
        raise FileNotFoundError("Transcript not found")

    with open(path, "r") as f:
        segments = json.load(f)

    if not isinstance(segments, list):
        raise ValueError("Transcript file is invalid")

    return segments


def _load_chunks(video_id: str) -> List[str]:

    import pickle

    chunks_path = os.path.join(VECTOR_DB_DIR, f"{video_id}_chunks.pkl")

    if not os.path.exists(chunks_path):
        return []

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    if not isinstance(chunks, list):
        return []

    return chunks


def _compute_transcript_stats(
    segments: List[Dict[str, Any]], chunks: List[str]
) -> Dict[str, Any]:

    all_text = " ".join(str(seg.get("text", "") or "").strip() for seg in segments)
    words = [w for w in re.split(r"\s+", all_text.strip()) if w]

    sentence_candidates = re.split(r"[.!?]+", all_text)
    sentences = [s.strip() for s in sentence_candidates if s.strip()]

    duration_candidates = []
    for seg in segments:
        if "end" in seg and seg["end"] is not None:
            duration_candidates.append(float(seg["end"]))
        elif "start" in seg and seg["start"] is not None:
            duration_candidates.append(float(seg["start"]))

    video_duration = max(duration_candidates) if duration_candidates else 0.0

    return {
        "total_words": len(words),
        "total_sentences": len(sentences),
        "video_duration": video_duration,
        "chunks_created": len(chunks),
    }


def _compute_speech_rate(stats: Dict[str, Any]) -> Dict[str, Any]:

    total_words = stats.get("total_words") or 0
    duration_seconds = stats.get("video_duration") or 0.0

    if not duration_seconds or duration_seconds <= 0:
        wpm = 0.0
    else:
        wpm = (total_words / duration_seconds) * 60.0

    return {"speech_rate_wpm": round(wpm, 2)}


def _get_embeddings(chunks: List[str]) -> np.ndarray:

    if not chunks:
        return np.empty((0, 0), dtype="float32")

    embeddings = _embedding_model.encode(chunks)
    return np.asarray(embeddings, dtype="float32")


def _summarize_with_llm(prompt: str) -> str:

    import ollama

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.get("message", {}).get("content", "")
    return content.strip()


def _detect_topics(chunks: List[str], embeddings: np.ndarray) -> List[Dict[str, Any]]:

    if not chunks or embeddings.size == 0:
        return []

    n, d = embeddings.shape

    if n == 1:
        base_text = re.sub(r"^\[\d+s\]\s*", "", chunks[0]).strip()
        label_prompt = (
            "You are labeling a transcript topic.\n\n"
            "Transcript snippet:\n"
            f"{base_text}\n\n"
            "Return a **very short** 1–3 word topic label only."
        )
        label = _summarize_with_llm(label_prompt)
        return [{"topic": label or "Main Topic", "weight": 1.0}]

    k = min(5, max(2, n // 4))

    kmeans = faiss.Kmeans(d, k, niter=10, verbose=False)
    kmeans.train(embeddings)
    distances, assignments = kmeans.index.search(embeddings, 1)

    assignments = assignments.reshape(-1)
    counts = np.bincount(assignments, minlength=k).astype(float)
    total = counts.sum() or 1.0
    weights = counts / total

    topics: List[Dict[str, Any]] = []

    for cluster_id in range(k):
        if counts[cluster_id] <= 0:
            continue

        indices_in_cluster = np.where(assignments == cluster_id)[0]
        if indices_in_cluster.size == 0:
            continue

        rep_index = int(indices_in_cluster[0])
        rep_chunk = chunks[rep_index]
        base_text = re.sub(r"^\[\d+s\]\s*", "", rep_chunk).strip()

        label_prompt = (
            "You are labeling a topic discussed in a video transcript.\n\n"
            "Representative transcript snippet:\n"
            f"{base_text}\n\n"
            "Return a **very short** 1–3 word topic label only."
        )
        label = _summarize_with_llm(label_prompt) or f"Topic {cluster_id + 1}"

        topics.append(
            {
                "topic": label,
                "weight": float(round(weights[cluster_id], 4)),
            }
        )

    topics.sort(key=lambda t: t["weight"], reverse=True)
    return topics


def _generate_chapters(chunks: List[str]) -> List[Dict[str, Any]]:

    if not chunks:
        return []

    n = len(chunks)
    num_chapters = min(6, max(2, math.ceil(n / 8)))

    chapter_boundaries = np.linspace(0, n, num_chapters + 1, dtype=int)

    chapters: List[Dict[str, Any]] = []

    for i in range(num_chapters):
        start_idx = chapter_boundaries[i]
        end_idx = max(start_idx + 1, chapter_boundaries[i + 1])

        group = chunks[start_idx:end_idx]
        if not group:
            continue

        group_text = " ".join(
            re.sub(r"^\[\d+s\]\s*", "", c).strip() for c in group
        ).strip()

        timestamp = extract_timestamp(group[0]) or 0

        prompt = (
            "You are creating a chapter title for a segment of a video.\n\n"
            "Here is the transcript segment:\n"
            f"{group_text}\n\n"
            "Return a **short, descriptive** chapter title (max 6 words). "
            "Return only the title text."
        )
        title = _summarize_with_llm(prompt) or f"Chapter {i + 1}"

        chapters.append({"title": title, "timestamp": int(timestamp)})

    return chapters


def _detect_key_moments(chunks: List[str], embeddings: np.ndarray) -> List[Dict[str, Any]]:

    if not chunks or embeddings.size == 0:
        return []

    norms = np.linalg.norm(embeddings, axis=1)
    if not np.isfinite(norms).all():
        norms = np.nan_to_num(norms, nan=0.0, posinf=0.0, neginf=0.0)

    top_k = min(5, len(chunks))
    top_indices = norms.argsort()[::-1][:top_k]

    key_moments: List[Dict[str, Any]] = []

    for idx in top_indices:
        chunk = chunks[int(idx)]
        text = re.sub(r"^\[\d+s\]\s*", "", chunk).strip()
        timestamp = extract_timestamp(chunk) or 0

        prompt = (
            "You are naming a key moment in a video based on a short transcript excerpt.\n\n"
            "Transcript excerpt:\n"
            f"{text}\n\n"
            "Return a **concise insight label** (max 8 words) describing why this moment is important. "
            "Return only the label text."
        )
        label = _summarize_with_llm(prompt) or "Key moment"

        key_moments.append(
            {
                "insight": label,
                "timestamp": int(timestamp),
            }
        )

    key_moments.sort(key=lambda m: m["timestamp"])
    return key_moments


def _get_rag_metrics(chunks: List[str]) -> Dict[str, Any]:

    return {
        "embedding_model": _EMBEDDING_MODEL_NAME,
        "vector_database": _VECTOR_DB_NAME,
        "chunks_indexed": len(chunks),
    }


def generate_analytics(video_id: str) -> Dict[str, Any]:

    segments = _load_transcript_segments(video_id)
    chunks = _load_chunks(video_id)

    stats = _compute_transcript_stats(segments, chunks)
    embeddings = _get_embeddings(chunks) if chunks else np.empty((0, 0), dtype="float32")

    topics = _detect_topics(chunks, embeddings)
    chapters = _generate_chapters(chunks)
    key_moments = _detect_key_moments(chunks, embeddings)
    speech_rate = _compute_speech_rate(stats)
    rag_metrics = _get_rag_metrics(chunks)

    return {
        "transcript_stats": stats,
        "topics": topics,
        "chapters": chapters,
        "key_moments": key_moments,
        "speech_rate": speech_rate,
        "rag_metrics": rag_metrics,
    }

