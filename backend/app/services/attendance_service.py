import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    MeetingJoined, MeetingEnded, ParticipantJoined, ParticipantLeft,
    AttendanceStarted, AttendanceUpdated, AttendanceCompleted, AttendanceFailed
)
from backend.app.services.storage_service import storage_manager

logger = logging.getLogger("ai_lecture_assistant")

class AttendanceService:
    """
    Deterministic Attendance Detection Engine.
    Tracks meeting participants, join/leave times, and calculates total duration.
    """

    def __init__(self):
        # In-memory state for active participants:
        # { meeting_id: { participant_id: { "join_time": datetime } } }
        self._active_sessions: Dict[str, Dict[str, Any]] = {}

    async def handle_meeting_joined(self, event: MeetingJoined):
        """Handles the start of a meeting's attendance tracking."""
        meeting_id = event.meeting_id
        logger.info(f"Attendance tracking started for meeting: {meeting_id}")

        self._active_sessions[meeting_id] = {}

        await dispatcher.publish(AttendanceStarted(meeting_id=meeting_id))

    async def handle_participant_joined(self, event: ParticipantJoined):
        """Handles a participant joining the meeting."""
        meeting_id = event.meeting_id
        p_id = event.participant_id
        timestamp = event.timestamp

        if meeting_id not in self._active_sessions:
            # Ensure we have a session if MeetingJoined was missed
            self._active_sessions[meeting_id] = {}
            await dispatcher.publish(AttendanceStarted(meeting_id=meeting_id))

        # Duplicate handling: ignore if already active
        if p_id in self._active_sessions[meeting_id]:
            logger.debug(f"Duplicate join event for participant {p_id} in meeting {meeting_id}")
            return

        # Track session start
        self._active_sessions[meeting_id][p_id] = {
            "join_time": timestamp,
        }

        # Update persistent record
        await self._update_participant_record(
            meeting_id=meeting_id,
            timestamp=timestamp,
            p_id=p_id,
            display_name=event.display_name,
            email=event.email
        )
        await self._add_timeline_event(meeting_id, "JOIN", p_id, event.display_name, timestamp)

        logger.info(f"Participant joined: {event.display_name} ({p_id}) in meeting {meeting_id}")
        await dispatcher.publish(AttendanceUpdated(meeting_id=meeting_id, participant_id=p_id))

    async def handle_participant_left(self, event: ParticipantLeft):
        """Handles a participant leaving the meeting."""
        meeting_id = event.meeting_id
        p_id = event.participant_id
        timestamp = event.timestamp

        if meeting_id not in self._active_sessions or p_id not in self._active_sessions[meeting_id]:
            # Handle "Ghost" participants: Left without a recorded join
            logger.warning(f"Participant {p_id} left without recorded join in meeting {meeting_id}")
            # Create a minimal record with 0 duration
            await self._update_participant_record(
                meeting_id=meeting_id,
                timestamp=timestamp,
                p_id=p_id,
                force_leave=True
            )
            await self._add_timeline_event(meeting_id, "LEAVE", p_id, "Unknown", timestamp)
            return

        # Calculate duration
        join_time = self._active_sessions[meeting_id][p_id]["join_time"]
        duration = (timestamp - join_time).total_seconds()

        # Update record and timeline
        await self._update_participant_record(
            meeting_id=meeting_id,
            timestamp=timestamp,
            p_id=p_id,
            duration=duration
        )
        await self._add_timeline_event(meeting_id, "LEAVE", p_id, None, timestamp, duration)

        # Remove from active sessions
        del self._active_sessions[meeting_id][p_id]

        logger.info(f"Participant left: {p_id} in meeting {meeting_id}")
        await dispatcher.publish(AttendanceUpdated(meeting_id=meeting_id, participant_id=p_id))

    async def handle_meeting_ended(self, event: MeetingEnded):
        """Handles the end of a meeting, closing all active participant sessions."""
        meeting_id = event.meeting_id
        timestamp = event.timestamp

        if meeting_id not in self._active_sessions:
            return

        # Close all remaining active sessions
        active_participants = list(self._active_sessions[meeting_id].keys())
        for p_id in active_participants:
            # Manually trigger a leave event for each active participant
            join_time = self._active_sessions[meeting_id][p_id]["join_time"]
            duration = (timestamp - join_time).total_seconds()

            await self._update_participant_record(
                meeting_id=meeting_id,
                timestamp=timestamp,
                p_id=p_id,
                duration=duration
            )
            await self._add_timeline_event(meeting_id, "LEAVE", p_id, None, timestamp, duration)

        # Generate statistics and save final package
        try:
            await self._generate_statistics(meeting_id, timestamp)
            logger.info(f"Attendance completed for meeting: {meeting_id}")
            await dispatcher.publish(AttendanceCompleted(meeting_id=meeting_id))
        except Exception as e:
            logger.error(f"Failed to complete attendance for meeting {meeting_id}: {e}")
            await dispatcher.publish(AttendanceFailed(meeting_id=meeting_id, error_message=str(e)))
        finally:
            # Cleanup in-memory state
            if meeting_id in self._active_sessions:
                del self._active_sessions[meeting_id]

    # --- Persistence Helpers ---

    async def _get_attendance_path(self, meeting_id: str) -> Path:
        meeting_folder = storage_manager.get_meeting_folder(meeting_id)
        attendance_dir = meeting_folder / "attendance"
        attendance_dir.mkdir(parents=True, exist_ok=True)
        return attendance_dir

    async def _update_participant_record(self, meeting_id: str, timestamp: datetime, p_id: str, display_name: Optional[str] = None, email: Optional[str] = None, duration: float = 0, force_leave: bool = False):
        """Updates the attendance.json master record."""
        path = await self._get_attendance_path(meeting_id) / "attendance.json"

        data = {}
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Corrupted attendance file {path}, starting fresh.")

        record = data.get(p_id, {
            "participant_id": p_id,
            "display_name": display_name or "Unknown",
            "email": email or "Unknown",
            "first_seen": timestamp.isoformat(),
            "last_seen": timestamp.isoformat(),
            "total_duration_seconds": 0,
            "status": "joined",
            "join_count": 0
        })

        # Update fields
        if display_name: record["display_name"] = display_name
        if email: record["email"] = email

        record["last_seen"] = timestamp.isoformat()
        record["total_duration_seconds"] += duration

        if force_leave:
            record["status"] = "left"
        elif duration == 0 and not force_leave:
            # Participant joined
            record["status"] = "joined"
            record["join_count"] += 1
            # Only update first_seen if this is the very first time
            if record["join_count"] == 1:
                record["first_seen"] = timestamp.isoformat()
        else:
            # Participant left
            record["status"] = "left"

        data[p_id] = record

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    async def _add_timeline_event(self, meeting_id: str, event_type: str, p_id: str, name: Optional[str], timestamp: datetime, duration: Optional[float] = None):
        """Adds an entry to timeline.json."""
        path = await self._get_attendance_path(meeting_id) / "timeline.json"

        timeline = []
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    timeline = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Corrupted timeline file {path}, starting fresh.")

        event_entry = {
            "timestamp": timestamp.isoformat(),
            "event": event_type,
            "participant_id": p_id,
            "display_name": name or "Unknown",
        }
        if duration is not None:
            event_entry["session_duration_seconds"] = duration

        timeline.append(event_entry)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=2)

    async def _generate_statistics(self, meeting_id: str, end_time: datetime):
        """Computes and saves statistics.json."""
        path = await self._get_attendance_path(meeting_id) / "attendance.json"
        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as f:
            participants = json.load(f)

        if not participants:
            return

        total_participants = len(participants)
        durations = [p["total_duration_seconds"] for p in participants.values()]
        avg_duration = sum(durations) / total_participants if durations else 0

        # For peak concurrent, we'd need to analyze the timeline
        # Let's do a simple timeline analysis
        timeline_path = await self._get_attendance_path(meeting_id) / "timeline.json"
        peak_participants = 0
        if timeline_path.exists():
            with open(timeline_path, "r", encoding="utf-8") as f:
                timeline = json.load(f)

            current_active = set()
            for event in timeline:
                if event["event"] == "JOIN":
                    current_active.add(event["participant_id"])
                elif event["event"] == "LEAVE":
                    current_active.discard(event["participant_id"])
                peak_participants = max(peak_participants, len(current_active))

        # Get meeting bounds
        first_seen = min(p["first_seen"] for p in participants.values())
        last_seen = max(p["last_seen"] for p in participants.values())

        start_dt = datetime.fromisoformat(first_seen)
        end_dt = datetime.fromisoformat(last_seen)
        meeting_duration = (end_dt - start_dt).total_seconds()

        stats = {
            "total_participants": total_participants,
            "average_attendance_duration_seconds": avg_duration,
            "peak_participants": peak_participants,
            "meeting_duration_seconds": meeting_duration,
            "earliest_join": first_seen,
            "latest_leave": last_seen
        }

        stats_path = await self._get_attendance_path(meeting_id) / "statistics.json"
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

attendance_service = AttendanceService()
