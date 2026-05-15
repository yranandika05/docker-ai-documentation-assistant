from fastapi import APIRouter
from pydantic import BaseModel
from app.retrieval.vector_search import search_documents
from app.ai.ollama_client import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[str]

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # Retrieve relevant context
    context_chunks = search_documents(request.question)
    
    # Generate answer using Ollama
    answer = generate_answer(request.question, context_chunks)
    
    # Extract citations (e.g., sources from chunks)
    citations = [chunk.get('source', '') for chunk in context_chunks]
    
    return ChatResponse(answer=answer, citations=citations)