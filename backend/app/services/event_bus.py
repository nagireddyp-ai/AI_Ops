import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, List


class EventBus:
    def __init__(self) -> None:
        self._subscribers: List[asyncio.Queue[Dict]] = []

    async def publish(self, event: Dict) -> None:
        for queue in list(self._subscribers):
            await queue.put(event)

    @asynccontextmanager
    async def subscribe(self) -> AsyncGenerator[AsyncGenerator[Dict, None], None]:
        queue: asyncio.Queue[Dict] = asyncio.Queue()
        self._subscribers.append(queue)

        async def generator() -> AsyncGenerator[Dict, None]:
            while True:
                event = await queue.get()
                yield event

        try:
            yield generator()
        finally:
            self._subscribers.remove(queue)
