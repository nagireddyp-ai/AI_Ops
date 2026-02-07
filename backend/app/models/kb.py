from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class KnowledgeArticle(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    tags: List[str] = Field(default_factory=list)
    incident_id: str
    created_at: datetime
    updated_at: datetime
