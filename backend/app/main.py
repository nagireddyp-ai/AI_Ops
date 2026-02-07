from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, chat, incidents, kb, logs, simulation, sla, servicenow
from app.rag.service import RAGService
from app.services.event_bus import EventBus
from app.simulation.controller import SimulationController
from app.state import AppState


def create_app() -> FastAPI:
    app = FastAPI(title="SitePulse Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.state = AppState()
    app.state.bus = EventBus()
    app.state.state.simulation = SimulationController(app.state.state, app.state.bus)
    app.state.state.rag = RAGService()

    app.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
    app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])
    app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(kb.router, prefix="/api/kb", tags=["kb"])
    app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
    app.include_router(sla.router, prefix="/api/sla", tags=["sla"])
    app.include_router(servicenow.router, prefix="/api/servicenow", tags=["servicenow"])

    @app.websocket("/ws/events")
    async def events_socket(websocket: WebSocket) -> None:
        await websocket.accept()
        async with app.state.bus.subscribe() as stream:
            async for event in stream:
                await websocket.send_json(event)

    return app


app = create_app()
