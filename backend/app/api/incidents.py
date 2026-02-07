from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Request

from app.models.incident import Incident, IncidentCreate, IncidentUpdate

router = APIRouter()


@router.get("/", response_model=List[Incident])
async def list_incidents(request: Request) -> List[Incident]:
    state = request.app.state.state
    return list(state.incidents.values())


@router.post("/", response_model=Incident)
async def create_incident(payload: IncidentCreate, request: Request) -> Incident:
    now = datetime.utcnow()
    incident = Incident(
        id=str(uuid4()),
        title=payload.title,
        type=payload.type,
        hostname=payload.hostname,
        region=payload.region,
        environment=payload.environment,
        severity=payload.severity,
        created_at=now,
        updated_at=now,
    )
    state = request.app.state.state
    state.incidents[incident.id] = incident
    await request.app.state.bus.publish({"event": "incident_created", "data": incident.model_dump()})
    return incident


@router.patch("/{incident_id}", response_model=Incident)
async def update_incident(incident_id: str, payload: IncidentUpdate, request: Request) -> Incident:
    state = request.app.state.state
    incident = state.incidents[incident_id]
    update_data = payload.model_dump(exclude_unset=True)
    updated = incident.model_copy(update=update_data | {"updated_at": datetime.utcnow()})
    state.incidents[incident_id] = updated
    await request.app.state.bus.publish({"event": "incident_updated", "data": updated.model_dump()})
    return updated
