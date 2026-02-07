import pytest

from app.simulation.controller import SimulationController
from app.simulation.synthetic import generate_incident
from app.services.event_bus import EventBus
from app.state import AppState


@pytest.mark.asyncio
async def test_generate_incident_populates_state_and_sla():
    state = AppState()
    bus = EventBus()
    controller = SimulationController(state, bus)

    await controller.generate_incidents(count=2)

    assert len(state.incidents) == 2
    assert len(state.sla_timers) == 2


def test_generate_incident_fields():
    incident = generate_incident()
    assert incident.hostname
    assert incident.severity
    assert incident.type
