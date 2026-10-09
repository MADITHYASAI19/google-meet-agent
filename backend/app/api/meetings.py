from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List, Optional
from datetime import datetime

from backend.app.schemas.api_schemas import APIResponse, MeetingRead, MeetingCreate, ErrorResponse
from backend.app.config.settings import settings
from backend.app.core.exceptions import AppException, EntityNotFoundException
from backend.app.services.storage_service import storage_manager
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import MeetingJoined, MeetingEnded

router = APIRouter()

@router.post("/", response_model=APIResponse[MeetingRead], tags=["Meetings"])
async def join_meeting(meeting: MeetingCreate):
    """
    Triggers the system to join a Google Meet session.
    """
    try:
        # In a real scenario, this would trigger the Playwright bot.
        # For now, we publish the event to trigger backend pipelines.
        await dispatcher.publish(MeetingJoined(meeting_id=meeting.meeting_id))

        # Return a mock MeetingRead for now as the bot initialization is async
        return APIResponse(
            data=MeetingRead(
                meeting_id=meeting.meeting_id,
                url=meeting.url,
                status="joining"
            ),
            message="Join request submitted successfully"
        )
    except Exception as e:
        raise AppException(f"Failed to join meeting: {str(e)}")

@router.post("/{meeting_id}/leave", tags=["Meetings"])
async def leave_meeting(meeting_id: str):
    """
    Triggers the system to leave a Google Meet session.
    """
    try:
        await dispatcher.publish(MeetingEnded(meeting_id=meeting_id))
        return APIResponse(
            data={"status": "left"},
            message=f"Successfully left meeting {meeting_id}"
        )
    except Exception as e:
        raise AppException(f"Failed to leave meeting: {str(e)}")

@router.get("/{meeting_id}", response_model=APIResponse[MeetingRead], tags=["Meetings"], dependencies=[RequireStudent])
async def get_meeting_status(meeting_id: str):
    """
    Retrieves current status and metadata for a specific meeting.
    """
    # Check if meeting folder exists
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    if not meeting_dir.exists():
        raise EntityNotFoundException(f"Meeting {meeting_id} not found")

    # Mocking detailed status - in production this comes from a DB
    return APIResponse(
        data=MeetingRead(
            meeting_id=meeting_id,
            status="active",
            start_time=datetime.now()
        )
    )
