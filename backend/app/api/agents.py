from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AgentStatus(BaseModel):
    name: str
    status: str
    last_action: str


@router.get("/status", response_model=list[AgentStatus])
async def list_agents() -> list[AgentStatus]:
    return [
        AgentStatus(name="triage", status="idle", last_action="waiting"),
        AgentStatus(name="resolution", status="idle", last_action="waiting"),
        AgentStatus(name="knowledge", status="idle", last_action="waiting"),
        AgentStatus(name="sla", status="idle", last_action="waiting"),
        AgentStatus(name="simulation", status="idle", last_action="waiting"),
        AgentStatus(name="chat", status="idle", last_action="waiting"),
    ]
