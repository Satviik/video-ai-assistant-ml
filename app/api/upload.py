from fastapi import APIRouter, UploadFile, File
import os
import uuid

from app.utils.chunking import chunk_transcript_segments
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import store_embeddings
from app.services.audio_service import extract_audio
from app.services.whisper_service import transcribe_audio
from app.utils.transcript_utils import save_transcript


router = APIRouter(prefix="/upload", tags=["Upload"])

VIDEO_DIR = "data/videos"
AUDIO_DIR = "data/audio"


@router.post("/")
async def upload_video(file: UploadFile = File(...)):

    video_id = str(uuid.uuid4())

    video_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")

    # Save uploaded video
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract audio
    audio_path = os.path.join(AUDIO_DIR, f"{video_id}.wav")
    extract_audio(video_path, audio_path)

    # Transcribe audio
    transcript, segments = transcribe_audio(audio_path)

    # Save transcript
    transcript_path = save_transcript(video_id, segments)

    # Chunk transcript
    chunks = chunk_transcript_segments(segments)
    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store in vector database
    store_embeddings(video_id, chunks, embeddings)

    return {
        "video_id": video_id,
        "transcript_file": transcript_path,
        "chunks_created": len(chunks),
        "status": "transcribed_and_indexed"
    }