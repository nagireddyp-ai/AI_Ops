from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class ChatQuery(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/query", response_model=ChatResponse)
async def chat_query(payload: ChatQuery, request: Request) -> ChatResponse:
    rag = request.app.state.state.rag
    result = rag.query(payload.question)
    return ChatResponse(answer=result.answer, sources=result.sources)
