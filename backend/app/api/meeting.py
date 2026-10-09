from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
import uuid
from sqlalchemy.orm import Session

from backend.app.agents.meeting_agent import meeting_agent
from backend.app.config.settings import settings
from backend.app.database.session import get_db
from backend.app.repositories.meeting_repository import MeetingRepository
from backend.app.core.exceptions import APIResponse

router = APIRouter()

class JoinMeetingRequest(BaseModel):
    url: str

class JoinMeetingResponse(BaseModel):
    meeting_id: str
    status: str

@router.post("/join", response_model=APIResponse[JoinMeetingResponse])
async def join_meeting(request: JoinMeetingRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Triggers the Meeting Agent to join a Google Meet session.
    """
    repo = MeetingRepository(db)

    # Create record in DB first
    meeting_session = repo.create(request.url)
    meeting_id = meeting_session.id

    # Launch joining process in background
    background_tasks.add_task(meeting_agent.join_meeting, meeting_id, request.url)

    return APIResponse(
        data=JoinMeetingResponse(
            meeting_id=meeting_id,
            status="joining"
        ),
        message="Meeting join process initiated."
    )

@router.post("/leave")
async def leave_meeting(db: Session = Depends(get_db)):
    """
    Triggers the Meeting Agent to leave the current meeting.
    """
    # Note: In a real scenario, we'd need the meeting_id to mark it as completed in DB
    # For now, the meeting_agent.leave_meeting() is the primary trigger.
    await meeting_agent.leave_meeting()
    return APIResponse(
        data={"status": "leaving"},
        message="Leaving meeting session."
    )
