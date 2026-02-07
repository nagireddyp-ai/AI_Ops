from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class SimulationCommand(BaseModel):
    action: str


@router.post("/control")
async def control_simulation(payload: SimulationCommand, request: Request) -> dict:
    controller = request.app.state.state.simulation
    if payload.action == "start":
        await controller.start()
    elif payload.action == "stop":
        await controller.stop()
    elif payload.action == "pause":
        controller.pause()
    elif payload.action == "resume":
        controller.resume()
    elif payload.action == "reset":
        await controller.reset()
    elif payload.action == "generate_10":
        await controller.generate_incidents(count=10)
    elif payload.action == "trigger_outage":
        await controller.trigger_outage()
    elif payload.action == "simulate_sla_breach":
        await controller.simulate_sla_breach()
    elif payload.action == "inject_log_spike":
        await controller.inject_log_spike()
    elif payload.action == "escalate":
        await controller.escalate()
    elif payload.action == "embed_kb":
        await request.app.state.bus.publish({"event": "kb_embedding_requested", "data": {}})
    elif payload.action == "chat_update_ticket":
        await request.app.state.bus.publish({"event": "chat_update_ticket", "data": {}})
    else:
        await request.app.state.bus.publish({"event": "simulation_command", "data": payload.model_dump()})
    return {"status": "accepted", "action": payload.action}
