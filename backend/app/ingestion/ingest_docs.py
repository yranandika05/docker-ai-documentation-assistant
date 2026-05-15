import os
from app.ai.ollama_client import generate_embedding
from app.models import DocumentChunk, SessionLocal, engine, Base
import glob

def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """Simple text chunking by character count."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def ingest_docker_docs():
    """Ingest Docker docs: read, chunk, embed, store in DB."""
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)
    
    docs_dir = os.path.join(os.path.dirname(__file__), "../../data/docker-docs")
    db = SessionLocal()
    
    try:
        # Get all .md files
        md_files = glob.glob(os.path.join(docs_dir, "*.md"))
        
        for file_path in md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chunk the content
            chunks = chunk_text(content)
            filename = os.path.basename(file_path)
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Skip empty chunks
                    # Generate embedding
                    embedding = generate_embedding(chunk)
                    
                    # Store in DB
                    doc_chunk = DocumentChunk(
                        content=chunk,
                        source=f"{filename}#chunk_{i}",
                        embedding=embedding
                    )
                    db.add(doc_chunk)
        
        db.commit()
        print(f"Ingested {len(md_files)} files successfully")
    
    except Exception as e:
        db.rollback()
        print(f"Error during ingestion: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    ingest_docker_docs()