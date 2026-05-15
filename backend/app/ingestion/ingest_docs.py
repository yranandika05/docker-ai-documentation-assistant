import os
from app.ai.ollama_client import generate_embedding

def ingest_docker_docs():
    """Ingest Docker docs: read, chunk, embed, store in DB."""
    docs_dir = "backend/data/docker-docs"
    
    # TODO: Read Markdown files from docs_dir
    # For now, placeholder
    sample_text = "This is a sample Docker documentation chunk."
    
    # Generate embedding
    embedding = generate_embedding(sample_text)
    
    # TODO: Store in PostgreSQL/pgvector
    print(f"Generated embedding for: {sample_text[:50]}...")
    print(f"Embedding length: {len(embedding)}")

if __name__ == "__main__":
    ingest_docker_docs()