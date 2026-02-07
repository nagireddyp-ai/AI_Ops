from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class SLATimer(BaseModel):
    incident_id: str
    remaining_minutes: int


@router.get("/", response_model=list[SLATimer])
async def list_sla(request: Request) -> list[SLATimer]:
    timers = request.app.state.state.sla_timers
    return [SLATimer(incident_id=key, remaining_minutes=value) for key, value in timers.items()]
