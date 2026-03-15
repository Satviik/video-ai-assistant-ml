# AI Video Analysis Assistant

A machine learning powered video understanding system designed to extract semantic knowledge from long videos and allow users to interact with video content through natural language queries.

The system converts raw video into structured semantic representations, enabling timestamp-grounded explanations, contextual question answering, and deep content analysis.

---

# Features
<pre>
• Video upload support
• Automatic speech transcription
• AI generated video chapters
• Semantic search inside video
• Timestamp grounded answers
• Context aware chat interface
• Video knowledge retrieval system
• Analytics dashboard for insights
</pre>
---

# System Overview

The system processes videos through a multi-stage AI pipeline that transforms audiovisual information into searchable semantic knowledge.
<div align="center">
<pre>
Video

↓

Audio Extraction

↓

Speech Transcription

↓

Chunking (Transcript Segmentation)

↓

Embedding Generation

↓

Vector Indexing

↓

Semantic Retrieval

↓

Reranking

↓

LLM Reasoning

↓

Timestamp Grounded Answers
</pre>
</div>

# Live Architecture
<div align="center">
<pre>
Frontend (React + Vercel)

↓

HTTPS API Requests

↓

FastAPI Backend

↓

Video Processing Pipeline

↓

Vector Database (FAISS)

↓

LLM Reasoning Layer

↓

Timestamp Grounded Responses
</pre>
</div>



# Technology Stack

## Machine Learning
<pre>
Python
PyTorch
Whisper
Sentence Transformers
FAISS
NumPy
Pandas
</pre>
---

## Backend
<pre>
FastAPI
Pydantic
Uvicorn
FFmpeg
</pre>
---

## Infrastructure
<pre>
AWS EC2
Ubuntu Server
GPU acceleration support
Async worker processing
</pre>
---

## Frontend
<pre>
React
TailwindCSS
Streaming chat interface
Deployment via Vercel.
</pre>
---

# Data Pipeline
<div align="center">

<pre>
Video Upload

↓

Audio Extraction (FFmpeg)

↓

Speech Recognition

↓

Chunking (Transcript Segmentation)

↓

Embedding Generation

↓

Vector Database Indexing

↓

Semantic Retrieval

↓

Reranking

↓

LLM Context Reasoning

↓

Chat Response
</pre>
</div>

# Video Understanding Pipeline

## 1. Audio Extraction

The uploaded video is processed using FFmpeg to extract the audio track.

Example command:

ffmpeg -i input_video.mp4 -q:a 0 -map a audio.wav

This prepares the audio for transcription.

---

## 2. Speech Transcription

Audio is transcribed using a speech recognition model.

Model used:

Whisper

Output:

timestamped transcript

Example:

[00:00:02] Welcome to the tutorial
[00:00:06] Today we will learn machine learning

---

## 3. Chunking (Transcript Segmentation)

After transcription, the transcript is divided into smaller semantic chunks. Long transcripts cannot be embedded effectively as a single unit, so chunking improves retrieval and semantic understanding.

Each chunk contains:

text content
start timestamp
end timestamp

Example:

Chunk 1 → 0:00–0:30
Text: Introduction to machine learning concepts

Chunk 2 → 0:30–1:00
Text: Explanation of supervised learning

Chunk 3 → 1:00–1:30
Text: Example datasets and training process

---

## Chunking Strategy

The system uses sliding window chunking to preserve context across boundaries.

Example:

Chunk Size: 30 seconds
Overlap: 10 seconds

Result:

Chunk 1 → 0:00–0:30
Chunk 2 → 0:20–0:50
Chunk 3 → 0:40–1:10

Overlap ensures that important context spanning chunk boundaries is not lost.

---

## 4. Embedding Generation

Each transcript chunk is converted into a semantic vector representation.

Example embedding models:

all-MiniLM-L6-v2
bge-small-en

Example:

segment_vector = embedding(chunk_text)

These embeddings encode the semantic meaning of the content.

---

## 5. Vector Indexing

Embeddings are stored inside a FAISS vector database.

Purpose:

Enable efficient similarity search for user queries.

User query example:

"Explain backpropagation"

The system retrieves the most relevant transcript chunks.

---

## 6. Semantic Retrieval

Top-K relevant chunks are retrieved from the FAISS index.

Example:

Chunk 42 → 03:12–03:45
Chunk 43 → 03:45–04:20
Chunk 44 → 04:20–04:50

These chunks form the context for answering the user’s query.

---

## 7. Semantic Reranking

A reranking model evaluates retrieved chunks to improve relevance.

Example models:

bge-reranker
cross-encoder/ms-marco

The reranker ensures that the most useful chunks are sent to the LLM.

---

## 8. LLM Reasoning

Relevant chunks are provided to a large language model.

Prompt structure:

User Question
+
Relevant Transcript Chunks

The model performs:

contextual reasoning
summarization
explanation generation

---

## 9. Timestamp Grounded Response

The system returns:

answer
source timestamps
video jump references

Example:

"Gradient descent is explained between 03:12–04:20 in the video."

Users can jump directly to the relevant section of the video.

---

# Backend Architecture
## Backend Architecture

<div align="center">

<pre>

+-------------------------+
| Video Upload API        |
+-------------------------+
            |
            v
+-------------------------+
| FFmpeg Audio Extractor  |
+-------------------------+
            |
            v
+-------------------------+
| Whisper Transcription   |
+-------------------------+
            |
            v
+-------------------------+
| Chunking Engine         |
+-------------------------+
            |
            v
+-------------------------+
| Embedding Generator     |
+-------------------------+
            |
            v
+-------------------------+
| FAISS Vector Index      |
+-------------------------+
            |
            v
+-------------------------+
| Semantic Retrieval      |
+-------------------------+
            |
            v
+-------------------------+
| Reranker Model          |
+-------------------------+
            |
            v
+-------------------------+
| LLM Reasoning Engine    |
+-------------------------+
            |
            v
+-------------------------+
| Chat Response API       |
+-------------------------+

</pre>

</div>
# Cloud Backend

Hosted on AWS EC2.

Responsibilities:

Video processing
Transcription pipeline
Embedding generation
Vector database management
LLM inference
Chat response serving

---

# Analytics Generation

During processing the system also generates analytics used in the dashboard.

Examples:

AI video chapters
topic segmentation
keyword extraction
content summary
speaker segments

These power the analytics tab of the application.

---

# Future Work

Multi-video knowledge graph

Cross-video semantic search

Scene level video understanding

Multimodal embeddings (video + audio + text)

Automatic lecture notes generation

Knowledge extraction from entire video libraries

---

# Author

Satvik Singh Rathore

---

# License

MIT License
