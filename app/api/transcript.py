import json
import os

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/transcript", tags=["Transcript"])


@router.get("/{video_id}")
async def get_transcript(video_id: str):
    """
    Return the saved transcript segments for a given video.

    Transcripts are stored as JSON in data/transcripts/{video_id}.json
    by app.utils.transcript_utils.save_transcript.
    """
    path = os.path.join("data", "transcripts", f"{video_id}.json")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Transcript not found")

    with open(path, "r") as f:
        segments = json.load(f)

    # Return the raw segment list; the frontend maps fields like
    # timestamp/start and text into its own shape.
    if not isinstance(segments, list):
        raise HTTPException(status_code=500, detail="Transcript file is invalid")

    return segments