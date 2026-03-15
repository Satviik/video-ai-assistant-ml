from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, chat, transcript, upload

app = FastAPI(
    title="AI Video Assistant API",
    version="1.0.0"
)

# CORS for local frontend (Vite dev server)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(transcript.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "AI Video Assistant Backend Running"}