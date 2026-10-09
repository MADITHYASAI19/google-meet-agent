from fastapi import APIRouter, HTTPException
from typing import List
import json

from backend.app.schemas.api_schemas import APIResponse, AttendanceRead, ParticipantRead
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import EntityNotFoundException

router = APIRouter()

@router.get("/{meeting_id}", response_model=APIResponse[AttendanceRead], tags=["Attendance"], dependencies=[RequireFaculty])
async def get_attendance(meeting_id: str):
    """
    Retrieves attendance data for a meeting.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    attendance_file = meeting_dir / "attendance" / "attendance.json"

    if not attendance_file.exists():
        raise EntityNotFoundException(f"Attendance data not found for meeting {meeting_id}")

    with open(attendance_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    participants = [ParticipantRead(**p) for p in data]

    return APIResponse(
        data=AttendanceRead(
            meeting_id=meeting_id,
            participants=participants,
            total_count=len(participants)
        )
    )
