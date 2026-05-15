from app.ai.ollama_client import generate_embedding

def search_documents(query: str) -> list[dict]:
    """Search for relevant documents using vector similarity."""
    # TODO: Embed the query
    query_embedding = generate_embedding(query)
    
    # TODO: Query PostgreSQL/pgvector for similar embeddings
    # For now, return placeholder
    return [{"text": "Placeholder document chunk", "source": "placeholder.md"}]