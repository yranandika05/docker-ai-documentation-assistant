# Docker AI Documentation Assistant

A portfolio project that answers questions about Docker documentation using RAG (Retrieval-Augmented Generation).

## Tech Stack

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Database: PostgreSQL with pgvector
- AI: Ollama (local LLMs) for embeddings and answer generation
- Containerization: Docker + Docker Compose

## Database Architecture

- **Database**: PostgreSQL with pgvector extension
- **Table**: `document_chunks`
  - `id`: Primary key
  - `content`: Text content of the chunk
  - `source`: Source file and chunk identifier
  - `embedding`: 768-dimensional vector (nomic-embed-text)
- **Vector Search**: Uses cosine similarity for retrieval

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
4. Ingest documents: `docker-compose exec backend python -m app.ingestion.ingest_docs`
5. Access the frontend at http://localhost:3000

## MVP Features

1. Backend health endpoint: GET /health
2. Chat endpoint: POST /chat
3. Ingestion script for Docker docs
4. Simple frontend chat interface

## TODO

- Add sample Docker docs to `backend/data/docker-docs/`
- Test ingestion and retrieval
- Optimize chunking and embedding dimensions