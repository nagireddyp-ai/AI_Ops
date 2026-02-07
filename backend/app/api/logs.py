from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.models.log import LogEntry

router = APIRouter()


class LogCreate(BaseModel):
    incident_id: str
    level: str
    message: str


@router.get("/", response_model=List[LogEntry])
async def list_logs(request: Request, incident_id: str | None = None) -> List[LogEntry]:
    logs = request.app.state.state.logs
    if incident_id:
        return [log for log in logs if log.incident_id == incident_id]
    return logs


@router.post("/", response_model=LogEntry)
async def create_log(payload: LogCreate, request: Request) -> LogEntry:
    entry = LogEntry(
        id=str(uuid4()),
        incident_id=payload.incident_id,
        level=payload.level,
        message=payload.message,
        timestamp=datetime.utcnow(),
    )
    state = request.app.state.state
    state.logs.append(entry)
    await request.app.state.bus.publish({"event": "log_created", "data": entry.model_dump()})
    return entry
