from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.models.kb import KnowledgeArticle

router = APIRouter()


class KnowledgeCreate(BaseModel):
    title: str
    summary: str
    content: str
    tags: List[str]
    incident_id: str


class EmbedRequest(BaseModel):
    ids: List[str]
    documents: List[str]
    metadata: List[dict]


@router.get("/", response_model=List[KnowledgeArticle])
async def list_articles(request: Request) -> List[KnowledgeArticle]:
    state = request.app.state.state
    return list(state.knowledge_base.values())


@router.post("/", response_model=KnowledgeArticle)
async def create_article(payload: KnowledgeCreate, request: Request) -> KnowledgeArticle:
    now = datetime.utcnow()
    article = KnowledgeArticle(
        id=str(uuid4()),
        title=payload.title,
        summary=payload.summary,
        content=payload.content,
        tags=payload.tags,
        incident_id=payload.incident_id,
        created_at=now,
        updated_at=now,
    )
    state = request.app.state.state
    state.knowledge_base[article.id] = article
    await request.app.state.bus.publish({"event": "kb_created", "data": article.model_dump()})
    return article


@router.post("/embed")
async def embed_articles(payload: EmbedRequest, request: Request) -> dict:
    rag = request.app.state.state.rag
    rag.embed_documents(payload.ids, payload.documents, payload.metadata)
    await request.app.state.bus.publish({"event": "kb_embedded", "data": {"count": len(payload.ids)}})
    return {"status": "embedded", "count": len(payload.ids)}
