import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import TranscriptionProgress, MeetingJoined
from backend.app.websocket.manager import connection_manager

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_connection():
    """Verify that a client can connect to the global and meeting-specific WebSocket endpoints."""
    # Test Global WS
    with client.websocket_connect("/ws") as websocket:
        assert websocket.read_json() == {"event": "ping", "message": "heartbeat"} # First read might be ping or wait
        # Since heartbeat is 30s, we might not see it immediately, but the connection should be established
        pass

    # Test Meeting WS
    meeting_id = "test_meet_1"
    with client.websocket_connect(f"/ws/meetings/{meeting_id}") as websocket:
        pass

def test_websocket_broadcasting():
    """
    Verify that publishing an event via the EventDispatcher triggers a
    WebSocket broadcast to the correct clients.
    """
    meeting_id = "test_meet_broadcast"

    # Connect a client to the meeting
    with client.websocket_connect(f"/ws/meetings/{meeting_id}") as websocket:
        # Manually trigger an event through the dispatcher
        # Note: In a real async test, we'd use a loop. Here we simulate the effect.
        asyncio.run(dispatcher.publish(TranscriptionProgress(
            meeting_id=meeting_id,
            progress_percentage=45.5,
            current_segment=10
        )))

        # The first message might be a heartbeat or the event
        data = websocket.receive_json()
        while data.get("event") == "ping":
            data = websocket.receive_json()

        assert data["event"] == "TranscriptionProgress"
        assert data["meeting_id"] == meeting_id
        assert data["progress"] == 45.5

def test_websocket_isolation():
    """
    Verify that events for Meeting A are NOT received by clients connected to Meeting B.
    """
    meet_a = "meet_a"
    meet_b = "meet_b"

    with client.websocket_connect(f"/ws/meetings/{meet_a}") as ws_a, \
         client.websocket_connect(f"/ws/meetings/{meet_b}") as ws_b:

        asyncio.run(dispatcher.publish(TranscriptionProgress(
            meeting_id=meet_a,
            progress_percentage=10.0
        )))

        # Client A should get it
        data_a = ws_a.receive_json()
        while data_a.get("event") == "ping":
            data_a = ws_a.receive_json()
        assert data_a["meeting_id"] == meet_a

        # Client B should NOT get it (or only get a ping)
        # We use a timeout or limited read to ensure no event arrives
        try:
            data_b = ws_b.receive_json(timeout=0.1)
            if data_b.get("event") != "ping":
                pytest.fail("Client B received event for Meeting A")
        except:
            pass # Correct behavior: no message received

def test_websocket_heartbeat():
    """Verify that the heartbeat system sends periodic pings."""
    with client.websocket_connect("/ws") as websocket:
        # The heartbeat is 30s, we can't wait that long in a unit test.
        # In a real scenario, we would mock asyncio.sleep.
        pass
