from fastapi import APIRouter, HTTPException

from app.services.analytics_service import generate_analytics


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/{video_id}")
async def get_analytics(video_id: str):

    try:
        analytics = generate_analytics(video_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript not found")
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate analytics: {exc}",
        )

    return analytics

