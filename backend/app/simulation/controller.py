import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from app.models.kb import KnowledgeArticle
from app.simulation.synthetic import generate_incident, generate_log


@dataclass
class SimulationConfig:
    incident_interval_seconds: int = 6
    sla_minutes: int = 45


class SimulationController:
    def __init__(self, state, bus) -> None:
        self.state = state
        self.bus = bus
        self.config = SimulationConfig()
        self._task: Optional[asyncio.Task] = None
        self._paused = False

    @property
    def running(self) -> bool:
        return self._task is not None and not self._task.done()

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False

    async def start(self) -> None:
        if self.running:
            return
        self._task = asyncio.create_task(self._run())
        await self.bus.publish({"event": "simulation_started", "data": {"ts": datetime.utcnow().isoformat()}})

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None
        await self.bus.publish({"event": "simulation_stopped", "data": {"ts": datetime.utcnow().isoformat()}})

    async def reset(self) -> None:
        self.state.incidents.clear()
        self.state.logs.clear()
        self.state.knowledge_base.clear()
        self.state.sla_timers.clear()
        await self.bus.publish({"event": "simulation_reset", "data": {"ts": datetime.utcnow().isoformat()}})

    async def generate_incidents(self, count: int = 1) -> None:
        for _ in range(count):
            incident = generate_incident()
            self.state.incidents[incident.id] = incident
            self.state.sla_timers[incident.id] = self.config.sla_minutes
            await self.bus.publish({"event": "incident_created", "data": incident.model_dump()})

    async def inject_log_spike(self) -> None:
        for incident_id in list(self.state.incidents.keys())[:5]:
            for _ in range(3):
                entry = generate_log(incident_id)
                self.state.logs.append(entry)
                await self.bus.publish({"event": "log_created", "data": entry.model_dump()})

    async def simulate_sla_breach(self) -> None:
        for incident_id in list(self.state.sla_timers.keys())[:3]:
            self.state.sla_timers[incident_id] = 0
            await self.bus.publish({"event": "sla_breached", "data": {"incident_id": incident_id}})

    async def trigger_outage(self) -> None:
        await self.generate_incidents(count=5)
        await self.bus.publish({"event": "outage_triggered", "data": {"count": 5}})

    async def escalate(self) -> None:
        for incident in self.state.incidents.values():
            incident.status = "escalated"
            incident.updated_at = datetime.utcnow()
            await self.bus.publish({"event": "incident_escalated", "data": incident.model_dump()})

    async def create_kb_article(self, incident_id: str) -> None:
        incident = self.state.incidents.get(incident_id)
        if not incident:
            return
        now = datetime.utcnow()
        article = KnowledgeArticle(
            id=f"kb-{incident_id}",
            title=f"Resolution for {incident.type}",
            summary=f"Auto-generated KB for {incident.hostname}",
            content="Steps: identify root cause, mitigate, verify, and monitor.",
            tags=[incident.type.lower().replace(" ", "-")],
            incident_id=incident_id,
            created_at=now,
            updated_at=now,
        )
        self.state.knowledge_base[article.id] = article
        await self.bus.publish({"event": "kb_created", "data": article.model_dump()})

    async def _run(self) -> None:
        try:
            while True:
                if not self._paused:
                    await self.generate_incidents(count=1)
                    await self._tick_sla()
                await asyncio.sleep(self.config.incident_interval_seconds)
        except asyncio.CancelledError:
            return

    async def _tick_sla(self) -> None:
        updated = {}
        for incident_id, remaining in list(self.state.sla_timers.items()):
            remaining = max(0, remaining - 1)
            self.state.sla_timers[incident_id] = remaining
            updated[incident_id] = remaining
            if remaining == 0:
                await self.bus.publish({"event": "sla_breached", "data": {"incident_id": incident_id}})
        if updated:
            await self.bus.publish({"event": "sla_tick", "data": updated})
