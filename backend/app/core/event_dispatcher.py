import asyncio
import logging
from typing import Any, Callable, Dict, List, Type, TypeVar

T = TypeVar("T")

class EventDispatcher:
    """
    A simple asynchronous event dispatcher for decoupled communication.
    """
    def __init__(self):
        self._listeners: Dict[Type, List[Callable]] = {}
        self.logger = logging.getLogger("ai_lecture_assistant.event_dispatcher")

    def subscribe(self, event_type: Type, callback: Callable):
        """
        Subscribe a callback to a specific event type.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        self.logger.debug(f"Subscribed to event {event_type.__name__}")

    async def publish(self, event: Any):
        """
        Publish an event to all registered listeners.
        """
        event_type = type(event)
        if event_type in self._listeners:
            self.logger.debug(f"Publishing event {event_type.__name__}")
            tasks = [callback(event) for callback in self._listeners[event_type]]
            await asyncio.gather(*tasks, return_exceptions=True)

# Global dispatcher instance
dispatcher = EventDispatcher()
