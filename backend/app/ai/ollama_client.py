import os
import ollama

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "mistral:7b")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

# Set the base URL for Ollama
ollama.base_url = OLLAMA_BASE_URL

def generate_embedding(text: str) -> list[float]:
    """Generate embeddings for the given text using Ollama."""
    response = ollama.embeddings(model=OLLAMA_EMBEDDING_MODEL, prompt=text)
    return response['embedding']

def generate_answer(question: str, context_chunks: list[dict]) -> str:
    """Generate an answer using Ollama LLM with question and context."""
    # Combine context chunks into a single string
    context = "\n".join([chunk.get('text', '') for chunk in context_chunks])
    
    # Craft the prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    
    # Generate response
    response = ollama.generate(model=OLLAMA_LLM_MODEL, prompt=prompt)
    return response['response']