from dataclasses import dataclass
from typing import Any, Dict

from langgraph.graph import END, StateGraph

from app.services.event_bus import EventBus


@dataclass
class AgentState:
    incident: Dict[str, Any]
    notes: str | None = None
    resolution: str | None = None
    kb_article_id: str | None = None


def triage_node(state: AgentState) -> AgentState:
    state.notes = f"Triage complete for {state.incident.get('title')}"
    return state


def resolution_node(state: AgentState) -> AgentState:
    state.resolution = "Apply rollback, restart service, monitor metrics."
    return state


def kb_node(state: AgentState) -> AgentState:
    state.kb_article_id = f"kb-{state.incident.get('id')}"
    return state


class AgentOrchestrator:
    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("triage", triage_node)
        graph.add_node("resolution", resolution_node)
        graph.add_node("kb", kb_node)
        graph.add_edge("triage", "resolution")
        graph.add_edge("resolution", "kb")
        graph.add_edge("kb", END)
        graph.set_entry_point("triage")
        return graph.compile()

    async def run(self, incident: Dict[str, Any]) -> AgentState:
        state = AgentState(incident=incident)
        result = self.graph.invoke(state)
        await self.bus.publish({"event": "agent_run_complete", "data": result.__dict__})
        return result
