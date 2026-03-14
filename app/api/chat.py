from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import retrieve_chunks
from app.services.llm_service import generate_answer
from app.services.memory_service import add_message, format_history

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    video_id: str
    question: str


@router.post("/")
async def chat_with_video(request: ChatRequest):

    add_message(request.video_id, "User", request.question)

    chunks = retrieve_chunks(
        request.video_id,
        request.question
    )

    history = format_history(request.video_id)

    context = "\n".join(chunks)

    answer = generate_answer(
        request.question,
        context,
        history
    )

    add_message(request.video_id, "Assistant", answer)

    return {
        "question": request.question,
        "answer": answer
    }