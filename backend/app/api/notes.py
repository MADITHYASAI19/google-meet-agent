from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
import json

from backend.app.schemas.api_schemas import APIResponse, NotesRead
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import NotesGenerationStarted

router = APIRouter()

@router.post("/{meeting_id}/generate", tags=["Notes"], dependencies=[RequireFaculty])
async def generate_notes(meeting_id: str):
    """
    Manually triggers the notes generation pipeline.
    """
    try:
        await dispatcher.publish(NotesGenerationStarted(meeting_id=meeting_id))
        return APIResponse(
            data={"status": "started"},
            message="Notes generation pipeline triggered"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{meeting_id}", response_model=APIResponse[NotesRead], tags=["Notes"], dependencies=[RequireStudent])
async def get_notes(meeting_id: str):
    """
    Retrieves the generated notes for a meeting.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    notes_file = meeting_dir / "notes" / "notes.json"

    if not notes_file.exists():
        raise EntityNotFoundException(f"Notes not found for meeting {meeting_id}")

    with open(notes_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return APIResponse(
        data=NotesRead(**data)
    )

@router.get("/{meeting_id}/download", tags=["Notes"], dependencies=[RequireStudent])
async def download_notes_md(meeting_id: str):
    """
    Retrieves the generated notes as a Markdown file.
    """
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    notes_md = meeting_dir / "notes" / "notes.md"

    if not notes_md.exists():
        raise EntityNotFoundException(f"Notes Markdown not found for meeting {meeting_id}")

    return FileResponse(
        path=notes_md,
        media_type="text/markdown",
        filename=f"{meeting_id}_notes.md"
    )
