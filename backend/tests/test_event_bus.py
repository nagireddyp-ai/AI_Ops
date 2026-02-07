import asyncio

import pytest

from app.services.event_bus import EventBus


@pytest.mark.asyncio
async def test_event_bus_broadcasts_to_all_subscribers():
    bus = EventBus()

    async with bus.subscribe() as stream_a:
        async with bus.subscribe() as stream_b:
            await bus.publish({"event": "ping"})
            event_a = await asyncio.wait_for(stream_a.__anext__(), timeout=1)
            event_b = await asyncio.wait_for(stream_b.__anext__(), timeout=1)

    assert event_a == {"event": "ping"}
    assert event_b == {"event": "ping"}
