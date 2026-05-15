# Docker AI Documentation Assistant

A portfolio project that answers questions about Docker documentation using RAG (Retrieval-Augmented Generation).

## Tech Stack

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Database: PostgreSQL with pgvector
- AI: Ollama (local LLMs) for embeddings and answer generation
- Containerization: Docker + Docker Compose

## Architecture

- `frontend/` - Next.js chat UI
- `backend/` - FastAPI API
- `backend/app/ai/` - Ollama client for embeddings and LLM
- `backend/app/ingestion/` - Scripts for loading and chunking Docker docs
- `backend/app/retrieval/` - Vector search logic
- `backend/app/api/` - Chat and search endpoints

## Setup

1. Install Ollama: https://ollama.ai/
2. Pull the required models:
   ```
   ollama pull mistral:7b
   ollama pull nomic-embed-text
   ```
3. Start Ollama: `ollama serve`
4. Clone the repository
5. Run `docker-compose up --build`
6. Access the frontend at http://localhost:3000

## MVP Features

1. Backend health endpoint: GET /health
2. Chat endpoint: POST /chat
3. Ingestion script for Docker docs
4. Simple frontend chat interface

## TODO

- Implement full ingestion script
- Implement vector search with pgvector
- Add database schema and models
- Test end-to-end RAG flow