from fastapi import FastAPI
from app.api import upload, chat, transcript

app = FastAPI(
    title="AI Video Assistant API",
    version="1.0.0"
)

# Register routes
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(transcript.router)


@app.get("/")
def root():
    return {"message": "AI Video Assistant Backend Running"}