from fastapi import APIRouter

router = APIRouter(prefix="/transcript", tags=["Transcript"])


@router.get("/{video_id}")
async def get_transcript(video_id: str):
    return {"video_id": video_id, "transcript": []}