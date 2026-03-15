from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import retrieve_chunks
from app.services.llm_service import generate_answer
from app.services.memory_service import add_message, format_history
from app.services.timestamp_service import extract_timestamp

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    video_id: str
    question: str


@router.post("/")
async def chat_with_video(request: ChatRequest):

    # Always store the user message
    add_message(request.video_id, "User", request.question)

    # Lightweight handling for simple greetings / thanks so they feel conversational.
    normalized = request.question.strip().lower()
    greeting_responses = {
        "hi": "Hi! Ask me anything about the video.",
        "hello": "Hi! Ask me anything about the video.",
        "hey": "Hey! What would you like to know about the video?",
        "thanks": "You're welcome! Let me know if you have more questions.",
        "thank you": "You're welcome! Feel free to ask more about the video.",
    }
    if normalized in greeting_responses:
        answer = greeting_responses[normalized]
        add_message(request.video_id, "Assistant", answer)
        return {
            "question": request.question,
            "answer": answer,
            "recommended_timestamp": None,
        }

    # Default behaviour: full RAG pipeline
    chunks, timestamp = retrieve_chunks(
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

    timestamp = extract_timestamp(
        request.question,
        context,
        answer
    )

    add_message(request.video_id, "Assistant", answer)

    return {
        "question": request.question,
        "answer": answer,
        "recommended_timestamp": timestamp
    }