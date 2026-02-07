from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Incident(BaseModel):
    id: str
    title: str
    type: str
    hostname: str
    region: str
    environment: str
    severity: str
    status: str = "new"
    assigned_engineer: Optional[str] = None
    escalation_path: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    logs: List[str] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)


class IncidentCreate(BaseModel):
    title: str
    type: str
    hostname: str
    region: str
    environment: str
    severity: str


class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    assigned_engineer: Optional[str] = None
    resolution_notes: Optional[str] = None
