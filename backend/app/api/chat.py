from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatQuery(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=ChatResponse)
async def chat_query(payload: ChatQuery) -> ChatResponse:
    return ChatResponse(
        answer=f"RAG placeholder response for: {payload.question}",
        sources=["incidents", "knowledge_base", "logs"],
    )
