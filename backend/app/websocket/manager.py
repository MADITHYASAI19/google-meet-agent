import asyncio
import logging
from typing import Dict, Set, List
from fastapi import WebSocket
from backend.app.websocket.events import WebSocketEvent

logger = logging.getLogger("ai_lecture_assistant.websocket.manager")

class ConnectionManager:
    """
    Singleton manager for WebSocket connections.
    Tracks connections globally and per meeting.
    """
    def __init__(self):
        # Maps meeting_id -> Set of WebSockets
        self.meeting_connections: Dict[str, Set[WebSocket]] = {}
        # Set of all connected WebSockets
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, meeting_id: Optional[str] = None):
        """Connect a WebSocket and optionally associate it with a meeting."""
        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)
            if meeting_id:
                if meeting_id not in self.meeting_connections:
                    self.meeting_connections[meeting_id] = set()
                self.meeting_connections[meeting_id].add(websocket)
        logger.debug(f"WebSocket connected. Total: {len(self.active_connections)} Meeting: {meeting_id}")

    async def disconnect(self, websocket: WebSocket, meeting_id: Optional[str] = None):
        """Disconnect a WebSocket and clean up associations."""
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            if meeting_id and meeting_id in self.meeting_connections:
                if websocket in self.meeting_connections[meeting_id]:
                    self.meeting_connections[meeting_id].remove(websocket)
                if not self.meeting_connections[meeting_id]:
                    del self.meeting_connections[meeting_id]
        logger.debug(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, event: WebSocketEvent):
        """Broadcast an event to all connected clients."""
        message = event.model_dump_json()
        async with self._lock:
            if not self.active_connections:
                return
            
            # Use gather to send concurrently, but handle failures per socket
            await asyncio.gather(
                *[self._send_safe(ws, message) for ws in self.active_connections],
                return_exceptions=True
            )

    async def broadcast_to_meeting(self, meeting_id: str, event: WebSocketEvent):
        """Broadcast an event to all clients subscribed to a specific meeting."""
        message = event.model_dump_json()
        async with self._lock:
            connections = self.meeting_connections.get(meeting_id, set())
            if not connections:
                return
            
            await asyncio.gather(
                *[self._send_safe(ws, message) for ws in connections],
                return_exceptions=True
            )

    async def send_personal_message(self, websocket: WebSocket, event: WebSocketEvent):
        """Send a message to a specific WebSocket connection."""
        message = event.model_dump_json()
        await self._send_safe(websocket, message)

    async def _send_safe(self, websocket: WebSocket, message: str):
        """Helper to send message and handle potential disconnects."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            # We don't disconnect here because the router's try-finally usually handles it

# Singleton instance
manager = ConnectionManager()
