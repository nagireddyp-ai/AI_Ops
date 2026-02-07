from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class ServiceNowUpdate(BaseModel):
    incident_id: str
    status: str
    notes: str | None = None


@router.post("/update")
async def update_ticket(payload: ServiceNowUpdate, request: Request) -> dict:
    await request.app.state.bus.publish({"event": "servicenow_update", "data": payload.model_dump()})
    return {"status": "updated", "incident_id": payload.incident_id}
