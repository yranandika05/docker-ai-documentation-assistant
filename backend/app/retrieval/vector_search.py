from app.ai.ollama_client import generate_embedding
from app.models import DocumentChunk, SessionLocal
from sqlalchemy import text

def search_documents(query: str, top_k: int = 5) -> list[dict]:
    """Search for relevant documents using vector similarity."""
    # Generate embedding for query
    query_embedding = generate_embedding(query)
    
    db = SessionLocal()
    try:
        # Use pgvector's cosine similarity
        # Note: <-> is cosine distance, we want smallest distance (most similar)
        result = db.execute(
            text("""
                SELECT content, source, 1 - (embedding <=> :query_emb) as similarity
                FROM document_chunks
                ORDER BY embedding <=> :query_emb
                LIMIT :top_k
            """),
            {"query_emb": query_embedding, "top_k": top_k}
        ).fetchall()
        
        # Return as list of dicts
        return [{"text": row[0], "source": row[1], "similarity": row[2]} for row in result]
    
    finally:
        db.close()