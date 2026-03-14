# Video AI Assistant Backend

A FastAPI-based backend for processing videos, extracting transcripts, and enabling AI-powered Q&A through RAG (Retrieval Augmented Generation).

## Features

- **Video Upload & Processing**: Handle video file uploads and extract metadata
- **Audio Extraction**: Extract audio streams from video files
- **Speech-to-Text**: Transcribe audio using OpenAI Whisper
- **Text Embeddings**: Generate semantic embeddings for transcript chunks
- **Vector Database**: Store and search embeddings for relevant content retrieval
- **RAG-based Chat**: Ask questions about video content with context-aware answers
- **Transcript Search**: Search within transcripts with timestamp results

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── api/                 # API routes
│   │   ├── upload.py        # File upload endpoints
│   │   ├── chat.py          # Chat/RAG endpoints
│   │   └── transcript.py    # Transcript management
│   ├── services/            # Business logic services
│   │   ├── video_service.py          # Video processing
│   │   ├── audio_service.py          # Audio processing
│   │   ├── whisper_service.py        # Speech-to-text
│   │   ├── embedding_service.py      # Text embeddings
│   │   ├── rag_service.py            # RAG operations
│   │   └── vector_store.py           # Vector database
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response schemas
│   └── utils/               # Utility functions
│       ├── chunking.py      # Text chunking algorithms
│       └── helpers.py       # General helper functions
├── data/                    # Data storage
│   ├── videos/              # Uploaded video files
│   ├── audio/               # Extracted audio files
│   └── transcripts/         # Generated transcripts
├── vector_db/               # Vector database storage
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.9+
- FFmpeg (for video/audio processing)

### Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Whisper model** (optional, auto-downloads on first use):
   ```bash
   python -m pip install openai-whisper
   ```

3. **Set environment variables**:
   Create a `.env` file in the backend directory:
   ```
   DEBUG=False
   WHISPER_MODEL=base
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   VECTOR_DIMENSION=384
   CHUNK_SIZE=500
   CHUNK_OVERLAP=50
   ```

## Running the Server

### Development
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Upload
- `POST /api/v1/upload/video` - Upload video file
- `POST /api/v1/upload/audio` - Upload audio file

### Chat/RAG
- `POST /api/v1/chat/ask` - Ask question about video content
- `GET /api/v1/chat/history/{video_id}` - Get chat history for video

### Transcript
- `GET /api/v1/transcript/{video_id}` - Get transcript for video
- `POST /api/v1/transcript/generate/{video_id}` - Generate transcript
- `GET /api/v1/transcript/{video_id}/search` - Search transcript

### Health
- `GET /health` - Health check

## Example Usage

### 1. Upload a Video
```bash
curl -X POST "http://localhost:8000/api/v1/upload/video" \
  -H "accept: application/json" \
  -F "file=@video.mp4"
```

### 2. Generate Transcript
```bash
curl -X POST "http://localhost:8000/api/v1/transcript/generate/vid_001"
```

### 3. Ask a Question
```bash
curl -X POST "http://localhost:8000/api/v1/chat/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "vid_001",
    "question": "What are the main topics covered?",
    "top_k": 5
  }'
```

## Architecture

### Data Flow

1. **Upload** → Video file received and stored
2. **Extract Audio** → Audio stream extracted from video
3. **Transcribe** → Audio transcribed to text using Whisper
4. **Chunk & Embed** → Transcript split into chunks and embedded
5. **Index** → Embeddings stored in vector database
6. **Query** → User questions embedded and searched against vectors
7. **Generate** → LLM generates answers based on retrieved context

### Key Services

- **VideoService**: Handles video file processing and validation
- **AudioService**: Manages audio extraction and conversion
- **WhisperService**: Wraps OpenAI Whisper for transcription
- **EmbeddingService**: Generates text embeddings using sentence transformers
- **RAGService**: Coordinates retrieval and generation
- **VectorStore**: Manages vector database operations

## Configuration

Key configuration options in `app/config.py`:

- `MAX_FILE_SIZE`: Maximum upload size (default: 500MB)
- `WHISPER_MODEL`: Whisper model size (tiny, base, small, medium, large)
- `EMBEDDING_MODEL`: Sentence transformer model
- `CHUNK_SIZE`: Text chunk size for embeddings
- `VECTOR_DIMENSION`: Embedding dimension
- `LLM_MODEL`: LLM for answer generation

## Dependencies

### Core
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### AI/ML
- **OpenAI**: Whisper and GPT models
- **Sentence Transformers**: Text embeddings
- **LangChain**: LLM orchestration
- **Torch/Transformers**: Deep learning

### Data
- **ChromaDB**: Vector database (can swap for Weaviate, Pinecone)
- **SQLAlchemy**: ORM for relational data
- **Redis**: Caching

### Audio/Video
- **librosa**: Audio processing
- **moviepy**: Video processing
- **soundfile**: Audio file I/O

## Development

### Testing
```bash
pytest
```

### Code Quality
```bash
black app/
flake8 app/
mypy app/
```

## Future Enhancements

- [ ] Real-time streaming uploads
- [ ] Multi-language support
- [ ] Custom model fine-tuning
- [ ] Advanced video analytics (scene detection, etc.)
- [ ] Collaborative features
- [ ] Export capabilities (PDF, SRT subtitles)

## License

See LICENSE file

## Support

For issues and feature requests, please open an issue in the repository.
