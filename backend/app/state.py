from dataclasses import dataclass, field
from typing import Dict, List

from app.models.incident import Incident
from app.models.kb import KnowledgeArticle
from app.models.log import LogEntry
from app.rag.service import RAGService
from app.simulation.controller import SimulationController


@dataclass
class AppState:
    incidents: Dict[str, Incident] = field(default_factory=dict)
    logs: List[LogEntry] = field(default_factory=list)
    knowledge_base: Dict[str, KnowledgeArticle] = field(default_factory=dict)
    sla_timers: Dict[str, int] = field(default_factory=dict)
    simulation: SimulationController | None = None
    rag: RAGService | None = None
