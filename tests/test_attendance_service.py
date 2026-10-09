import pytest
import asyncio
from datetime import datetime, timedelta
from backend.app.services.attendance_service import AttendanceService
from backend.app.events.meeting_events import (
    MeetingJoined, MeetingEnded, ParticipantJoined, ParticipantLeft
)
from backend.app.core.event_dispatcher import dispatcher
from backend.app.services.storage_service import storage_manager
import json
from pathlib import Path
import shutil

@pytest.fixture
def attendance_service():
    service = AttendanceService()
    # Clear storage before each test
    meeting_dir = storage_manager.base_path / "meetings"
    if meeting_dir.exists():
        shutil.rmtree(meeting_dir)
    storage_manager.initialize_storage()
    return service

@pytest.mark.asyncio
async def test_basic_attendance(attendance_service):
    meeting_id = "test_meeting_1"
    p_id = "user_1"
    p_name = "Alice"
    start_time = datetime(2023, 10, 1, 10, 0, 0)
    end_time = start_time + timedelta(minutes=30)

    # 1. Meeting Joined
    await attendance_service.handle_meeting_joined(MeetingJoined(meeting_id=meeting_id, timestamp=start_time))
    
    # 2. Participant Joined
    await attendance_service.handle_participant_joined(
        ParticipantJoined(meeting_id=meeting_id, participant_id=p_id, display_name=p_name, timestamp=start_time)
    )
    
    # 3. Participant Left
    await attendance_service.handle_participant_left(
        ParticipantLeft(meeting_id=meeting_id, participant_id=p_id, timestamp=end_time)
    )
    
    # 4. Meeting Ended
    await attendance_service.handle_meeting_ended(MeetingEnded(meeting_id=meeting_id, timestamp=end_time))

    # Verify attendance.json
    path = storage_manager.get_meeting_folder(meeting_id) / "attendance" / "attendance.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    assert p_id in data
    assert data[p_id]["total_duration_seconds"] == 1800
    assert data[p_id]["status"] == "left"
    assert data[p_id]["join_count"] == 1

@pytest.mark.asyncio
async def test_flaky_connection(attendance_service):
    meeting_id = "test_meeting_2"
    p_id = "user_2"
    p_name = "Bob"
    t0 = datetime(2023, 10, 1, 10, 0, 0)
    
    await attendance_service.handle_meeting_joined(MeetingJoined(meeting_id=meeting_id, timestamp=t0))
    
    # First session: 10 mins
    await attendance_service.handle_participant_joined(ParticipantJoined(meeting_id=meeting_id, participant_id=p_id, display_name=p_name, timestamp=t0))
    await attendance_service.handle_participant_left(ParticipantLeft(meeting_id=meeting_id, participant_id=p_id, timestamp=t0 + timedelta(minutes=10)))
    
    # Second session: 20 mins
    await attendance_service.handle_participant_joined(ParticipantJoined(meeting_id=meeting_id, participant_id=p_id, display_name=p_name, timestamp=t0 + timedelta(minutes=15)))
    await attendance_service.handle_participant_left(ParticipantLeft(meeting_id=meeting_id, participant_id=p_id, timestamp=t0 + timedelta(minutes=35)))
    
    await attendance_service.handle_meeting_ended(MeetingEnded(meeting_id=meeting_id, timestamp=t0 + timedelta(minutes=40)))

    path = storage_manager.get_meeting_folder(meeting_id) / "attendance" / "attendance.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    assert data[p_id]["total_duration_seconds"] == (10*60) + (20*60)
    assert data[p_id]["join_count"] == 2

@pytest.mark.asyncio
async def test_ghost_participant(attendance_service):
    meeting_id = "test_meeting_3"
    p_id = "user_3"
    t0 = datetime(2023, 10, 1, 10, 0, 0)
    
    # Leave event without join
    await attendance_service.handle_participant_left(ParticipantLeft(meeting_id=meeting_id, participant_id=p_id, timestamp=t0))
    
    path = storage_manager.get_meeting_folder(meeting_id) / "attendance" / "attendance.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    assert p_id in data
    assert data[p_id]["total_duration_seconds"] == 0
    assert data[p_id]["status"] == "left"

@pytest.mark.asyncio
async def test_missing_leave_on_end(attendance_service):
    meeting_id = "test_meeting_4"
    p_id = "user_4"
    t0 = datetime(2023, 10, 1, 10, 0, 0)
    t_end = t0 + timedelta(minutes=60)
    
    await attendance_service.handle_meeting_joined(MeetingJoined(meeting_id=meeting_id, timestamp=t0))
    await attendance_service.handle_participant_joined(ParticipantJoined(meeting_id=meeting_id, participant_id=p_id, display_name="Charlie", timestamp=t0))
    
    # No leave event, just meeting ended
    await attendance_service.handle_meeting_ended(MeetingEnded(meeting_id=meeting_id, timestamp=t_end))

    path = storage_manager.get_meeting_folder(meeting_id) / "attendance" / "attendance.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    assert data[p_id]["total_duration_seconds"] == 3600
    assert data[p_id]["status"] == "left"
