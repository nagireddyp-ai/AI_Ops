from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class SimulationCommand(BaseModel):
    action: str


@router.post("/control")
async def control_simulation(payload: SimulationCommand, request: Request) -> dict:
    await request.app.state.bus.publish({"event": "simulation_command", "data": payload.model_dump()})
    return {"status": "accepted", "action": payload.action}
