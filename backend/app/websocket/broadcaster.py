import logging
from typing import Any, Dict, Optional, Type
from datetime import datetime

from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import MeetingEvent
from backend.app.websocket.manager import connection_manager
from backend.app.websocket.events import WebSocketEvent
from backend.app.config.logging_config import setup_logging

logger = setup_logging()

class WebSocketBroadcaster:
    """
    The relay component that bridges the EventDispatcher and the ConnectionManager.
    Subscribes to all MeetingEvents and formats them as WebSocketEvents.
    """

    def __init__(self):
        self._initialized = False

    async def setup_subscriptions(self):
        """
        Registers the Broadcaster as a listener for all meeting-related events.
        """
        if self._initialized:
            return

        # List of all event types we want to relay.
        from backend.app.events.meeting_events import (
            MeetingJoined, MeetingEnded, AudioCaptureStarted, AudioCaptureStopped,
            TranscriptionStarted, TranscriptionProgress, TranscriptionCompleted, TranscriptionFailed,
            ParticipantJoined, ParticipantLeft, AttendanceStarted, AttendanceUpdated, AttendanceCompleted, AttendanceFailed,
            NotesGenerationStarted, NotesGenerationProgress, NotesGenerationCompleted, NotesGenerationFailed,
            QuizGenerationStarted, QuizGenerationProgress, QuizGenerationCompleted, QuizGenerationFailed,
            FlashcardGenerationStarted, FlashcardGenerationProgress, FlashcardGenerationCompleted, FlashcardGenerationFailed,
            AssignmentGenerationStarted, AssignmentGenerationProgress, AssignmentGenerationCompleted, AssignmentGenerationFailed,
            StudyPackGenerationStarted, StudyPackGenerationProgress, StudyPackGenerationCompleted, StudyPackGenerationFailed
        )

        events_to_relay = [
            MeetingJoined, MeetingEnded, AudioCaptureStarted, AudioCaptureStopped,
            TranscriptionStarted, TranscriptionProgress, TranscriptionCompleted, TranscriptionFailed,
            ParticipantJoined, ParticipantLeft, AttendanceStarted, AttendanceUpdated, AttendanceCompleted, AttendanceFailed,
            NotesGenerationStarted, NotesGenerationProgress, NotesGenerationCompleted, NotesGenerationFailed,
            QuizGenerationStarted, QuizGenerationProgress, QuizGenerationCompleted, QuizGenerationFailed,
            FlashcardGenerationStarted, FlashcardGenerationProgress, FlashcardGenerationCompleted, FlashcardGenerationFailed,
            AssignmentGenerationStarted, AssignmentGenerationProgress, AssignmentGenerationCompleted, AssignmentGenerationFailed,
            StudyPackGenerationStarted, StudyPackGenerationProgress, StudyPackGenerationCompleted, StudyPackGenerationFailed
        ]

        for event_type in events_to_relay:
            dispatcher.subscribe(event_type, self.handle_event)

        self._initialized = True
        logger.info("WebSocketBroadcaster: All event subscriptions established.")

    async def handle_event(self, event: MeetingEvent):
        """
        Generic event handler that transforms any MeetingEvent into a WebSocketEvent.
        """
        try:
            # Extract common attributes
            meeting_id = getattr(event, "meeting_id", None)

            # Determine progress if available
            progress = 0.0
            if hasattr(event, "progress_percentage"):
                progress = event.progress_percentage
            elif hasattr(event, "progress"):
                progress = event.progress

            # Determine status based on event name
            status = "info"
            event_name = event.__class__.__name__
            if "Started" in event_name:
                status = "processing"
            elif "Completed" in event_name:
                status = "completed"
            elif "Failed" in event_name:
                status = "failed"
            elif "Progress" in event_name:
                status = "processing"

            # Create the unified WebSocket message
            ws_event = WebSocketEvent(
                event=event_name,
                meeting_id=meeting_id,
                status=status,
                progress=progress,
                message=self._get_event_message(event),
                payload=self._extract_payload(event)
            )

            # Broadcast based on scope
            if meeting_id:
                # Broadcast to the specific meeting stream
                await connection_manager.broadcast_to_meeting(meeting_id, ws_event.model_dump(mode="json"))

            # Also broadcast to the global stream for system monitoring
            await connection_manager.broadcast_to_system(ws_event.model_dump(mode="json"))

        except Exception as e:
            logger.error(f"WebSocketBroadcaster failed to relay event {type(event).__name__}: {e}")

    def _get_event_message(self, event: MeetingEvent) -> str:
        """Generates a human-readable message for the event."""
        event_name = event.__class__.__name__

        if "Progress" in event_name:
            return f"{event_name.replace('Progress', '')} is {getattr(event, 'progress_percentage', 0):.1f}% complete"
        if "Completed" in event_name:
            return f"{event_name.replace('Completed', '')} finished successfully"
        if "Failed" in event_name:
            return f"{event_name.replace('Failed', '')} failed: {getattr(event, 'error_message', 'Unknown error')}"
        if "Started" in event_name:
            return f"Started {event_name.replace('Started', '')}"

        return f"Event {event_name} occurred"

    def _extract_payload(self, event: MeetingEvent) -> Dict[str, Any]:
        """Extracts data from the event dataclass to send as payload."""
        payload = {}
        for field in event.__dataclass_fields__:
            if field not in ["timestamp", "meeting_id"]:
                payload[field] = getattr(event, field)
        return payload

# Singleton instance
broadcaster = WebSocketBroadcaster()
