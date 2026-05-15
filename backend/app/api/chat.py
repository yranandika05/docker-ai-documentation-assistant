from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    citations: list[str]

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # TODO: implement retrieval and OpenAI call
    return ChatResponse(answer="TODO: implement chat logic", citations=[])