import os
from app.ai.ollama_client import generate_embedding
import glob

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Simple text chunking by character count. Use Overlap to maintain context."""
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def clean_text(text: str) -> str:
    """Basic cleanup: remove excessive blank lines and strip whitespace."""
    # Split into lines
    lines = text.split('\n')
    
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in lines]
    
    # Remove excessive blank lines (keep max 1 consecutive blank line)
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if line:  # Non-empty line
            cleaned_lines.append(line)
            prev_blank = False
        elif not prev_blank:  # First blank line after content
            cleaned_lines.append('')
            prev_blank = True
    
    # Join back and strip final result
    return '\n'.join(cleaned_lines).strip()

def ingest_docker_docs():
    """Ingest Docker docs: read, chunk, embed, store in DB."""
    from app.models import DocumentChunk, SessionLocal, engine, Base

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
            
            # Clean the content
            content = clean_text(content)
            
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

def test_chunking():
    """Read sample docs recursively, clean, chunk, and print first 10 chunks."""
    docs_dir = os.path.join(os.path.dirname(__file__), "../../data/sample-docs")
    patterns = ["**/*.md", "**/*.mdx"]
    file_paths = []
    for pattern in patterns:
        file_paths.extend(glob.glob(os.path.join(docs_dir, pattern), recursive=True))
    file_paths.sort()

    chunk_count = 0
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_text(content)
        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            preview = chunk.replace("\n", " ")[:100]
            print(f"{chunk_count+1}. {file_path} | chunk {i} | len={len(chunk)}")
            print(f"   preview: {preview}...\n")

            chunk_count += 1
            if chunk_count >= 10:
                return

if __name__ == "__main__":
    ingest_docker_docs()