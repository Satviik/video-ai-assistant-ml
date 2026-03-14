"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UploadResponse(BaseModel):
    """Response for file upload"""
    file_id: str
    filename: str
    size: int
    duration: Optional[float] = None
    format: str

class TranscriptSegment(BaseModel):
    """Transcript segment with timestamp"""
    id: int
    start: float
    end: float
    text: str

class TranscriptResponse(BaseModel):
    """Response for transcript retrieval"""
    video_id: str
    text: str
    segments: List[TranscriptSegment]
    language: str = "en"

class ChatRequest(BaseModel):
    """Chat request for RAG queries"""
    video_id: str
    question: str
    top_k: int = Field(default=5, ge=1, le=20)

class ChatResponse(BaseModel):
    """Response from chat/RAG query"""
    question: str
    answer: str
    sources: List[dict]
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)

class VideoMetadata(BaseModel):
    """Video metadata"""
    video_id: str
    filename: str
    upload_date: datetime
    duration: float
    transcript_status: str = "pending"  # pending, processing, completed
    indexing_status: str = "pending"  # pending, processing, completed

class EmbeddingRequest(BaseModel):
    """Request to generate embeddings"""
    text: str

class SearchRequest(BaseModel):
    """Request to search transcripts"""
    video_id: str
    query: str
    top_k: int = Field(default=5, ge=1, le=20)

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
