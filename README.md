# Docker AI Documentation Assistant

A portfolio project that answers questions about Docker documentation using RAG (Retrieval-Augmented Generation).

## Tech Stack

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Database: PostgreSQL with pgvector
- AI: OpenAI API for embeddings and answer generation
- Containerization: Docker + Docker Compose

## Architecture

- `frontend/` - Next.js chat UI
- `backend/` - FastAPI API
- `backend/app/ingestion/` - Scripts for loading and chunking Docker docs
- `backend/app/retrieval/` - Vector search logic
- `backend/app/api/` - Chat and search endpoints

## Setup

1. Clone the repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
3. Run `docker-compose up --build`
4. Access the frontend at http://localhost:3000

## MVP Features

1. Backend health endpoint: GET /health
2. Chat endpoint: POST /chat
3. Ingestion script for Docker docs
4. Simple frontend chat interface

## TODO

- Implement ingestion script
- Implement retrieval logic
- Implement API endpoints
- Build frontend UI