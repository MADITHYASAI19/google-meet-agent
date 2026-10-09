from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path

from backend.app.schemas.api_schemas import APIResponse, AudioStatus
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import AudioCaptureStopped

router = APIRouter()

@router.post("/{meeting_id}/stop", tags=["Audio"], dependencies=[RequireFaculty])
async def stop_audio_capture(meeting_id: str):
    """
    Manually stops audio capture for a meeting.
    """
    try:
        # Trigger the event to stop capture and start transcription
        await dispatcher.publish(AudioCaptureStopped(meeting_id=meeting_id))
        return APIResponse(
            data={"status": "stopping"},
            message="Audio capture stop signal sent"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{meeting_id}/download", tags=["Audio"], dependencies=[RequireStudent])
async def download_audio(meeting_id: str):
    """
    Retrieves the raw audio file for a meeting.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    audio_file = meeting_dir / "audio" / "lecture_audio.wav"

    if not audio_file.exists():
        raise EntityNotFoundException(f"Audio file not found for meeting {meeting_id}")

    return FileResponse(
        path=audio_file,
        media_type="audio/wav",
        filename=f"{meeting_id}_audio.wav"
    )
