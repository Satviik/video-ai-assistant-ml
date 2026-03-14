# Backend Setup & Development Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Development Server
```bash
python -m uvicorn app.main:app --reload
```

Server will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

## Project Architecture

### Core Components

**API Layer** (`app/api/`)
- `upload.py`: Video and audio file upload endpoints
- `chat.py`: Chat and RAG query endpoints
- `transcript.py`: Transcript management and search

**Services Layer** (`app/services/`)
- `video_service.py`: Video processing and metadata extraction
- `audio_service.py`: Audio extraction and conversion
- `whisper_service.py`: Speech-to-text transcription
- `embedding_service.py`: Text embedding generation
- `rag_service.py`: Retrieval Augmented Generation orchestration
- `vector_store.py`: Vector database operations

**Data Models** (`app/models/`)
- `schemas.py`: Pydantic models for request/response validation

**Utilities** (`app/utils/`)
- `chunking.py`: Text splitting and chunking algorithms
- `helpers.py`: General utility functions

**Configuration** (`app/`)
- `main.py`: FastAPI app initialization
- `config.py`: Settings management

### Data Flow

```
Upload Video
    ↓
Extract Audio
    ↓
Transcribe (Whisper)
    ↓
Chunk Text
    ↓
Generate Embeddings
    ↓
Store in Vector DB
    ↓
Ready for Queries
```

## Development Workflow

### Testing
```bash
pytest
pytest -v  # Verbose output
pytest --cov  # With coverage report
```

### Code Quality
```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## API Usage Examples

### Upload Video
```bash
curl -X POST "http://localhost:8000/api/v1/upload/video" \
  -F "file=@sample.mp4"
```

### Generate Transcript
```bash
curl -X POST "http://localhost:8000/api/v1/transcript/generate/vid_001"
```

### Ask Question
```bash
curl -X POST "http://localhost:8000/api/v1/chat/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "vid_001",
    "question": "What is the main topic?",
    "top_k": 5
  }'
```

## Configuration Options

See `app/config.py` for all available settings. Key options:

- `WHISPER_MODEL`: Model size (tiny, base, small, medium, large)
- `EMBEDDING_MODEL`: Sentence transformer model
- `CHUNK_SIZE`: Size of text chunks for embeddings
- `VECTOR_DIMENSION`: Embedding vector dimension
- `LLM_MODEL`: Language model for answer generation

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

**Whisper model download fails**
- Solution: `python -m pip install openai-whisper --upgrade`

**CUDA/GPU issues**
- Solution: Install CPU-only PyTorch or configure CUDA properly

**Permission denied on data directories**
- Solution: Check file permissions or run with appropriate user

## Environment Setup

### Install ffmpeg (required for video/audio processing)

**Windows**:
```bash
# Using choco
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt-get install ffmpeg
```

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Copy and configure: `cp .env.example .env`
3. Run dev server: `python -m uvicorn app.main:app --reload`
4. Check API docs: Open browser to `http://localhost:8000/docs`
5. Test upload: Use the Swagger UI or curl commands above
