from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
import json

from backend.app.schemas.api_schemas import APIResponse, TranscriptionRead
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import TranscriptionQueued

router = APIRouter()

@router.post("/{meeting_id}/trigger", tags=["Transcription"], dependencies=[RequireFaculty])
async def trigger_transcription(meeting_id: str):
    """
    Manually triggers transcription for a meeting.
    """
    try:
        # In a real scenario, we'd check if audio exists first
        await dispatcher.publish(TranscriptionQueued(meeting_id=meeting_id))
        return APIResponse(
            data={"status": "queued"},
            message="Transcription has been queued"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{meeting_id}", response_model=APIResponse[TranscriptionRead], tags=["Transcription"], dependencies=[RequireStudent])
async def get_transcription(meeting_id: str):
    """
    Retrieves the full transcription for a meeting.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    transcript_file = meeting_dir / "transcripts" / "transcript.json"

    if not transcript_file.exists():
        raise EntityNotFoundException(f"Transcription not found for meeting {meeting_id}")

    with open(transcript_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return APIResponse(
        data=TranscriptionRead(
            meeting_id=meeting_id,
            full_text=data.get("full_text", ""),
            segments=data.get("segments", []),
            status="completed"
        )
    )

@router.get("/{meeting_id}/download", tags=["Transcription"], dependencies=[RequireStudent])
async def download_transcript_md(meeting_id: str):
    """
    Retrieves the transcription as a Markdown file.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    transcript_md = meeting_dir / "transcripts" / "transcript.md"

    if not transcript_md.exists():
        raise EntityNotFoundException(f"Transcript Markdown not found for meeting {meeting_id}")

    return FileResponse(
        path=transcript_md,
        media_type="text/markdown",
        filename=f"{meeting_id}_transcript.md"
    )
