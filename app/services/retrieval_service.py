import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_timestamp(chunk):

    match = re.search(r"\[(\d+)s\]", chunk)

    if match:
        return int(match.group(1))

    return None

def rerank_chunks(question, chunks):

    question_embedding = model.encode([question])[0]

    scored_chunks = []

    for chunk in chunks:

        chunk_embedding = model.encode([chunk])[0]

        score = np.dot(question_embedding, chunk_embedding)

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)

    reranked = [chunk for score, chunk in scored_chunks]

    return reranked


def retrieve_chunks(video_id, question, top_k=6):

    index = faiss.read_index(f"data/vector_db/{video_id}.index")

    with open(f"data/vector_db/{video_id}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    question_embedding = model.encode([question])

    distances, indices = index.search(question_embedding, top_k)

    retrieved = [chunks[i] for i in indices[0]]

    reranked = rerank_chunks(question, retrieved)
    best_chunks = reranked[:3]
    timestamp = extract_timestamp(best_chunks[0])

    return best_chunks, timestamp