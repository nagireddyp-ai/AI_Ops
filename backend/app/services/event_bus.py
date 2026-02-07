import asyncio
from typing import AsyncGenerator, Dict


class EventBus:
    def __init__(self) -> None:
        self._queue: asyncio.Queue[Dict] = asyncio.Queue()

    async def publish(self, event: Dict) -> None:
        await self._queue.put(event)

    async def stream(self) -> AsyncGenerator[Dict, None]:
        while True:
            event = await self._queue.get()
            yield event
