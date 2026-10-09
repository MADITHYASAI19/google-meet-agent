from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
import json

from backend.app.schemas.api_schemas import APIResponse, QuizRead, FlashcardRead, AssignmentRead, StudyPackRead
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import EntityNotFoundException

router = APIRouter()

@router.get("/quiz/{meeting_id}", response_model=APIResponse[QuizRead], tags=["Study Materials"], dependencies=[RequireStudent])
async def get_quiz(meeting_id: str):
    """Retrieves generated quiz for a meeting."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    quiz_file = meeting_dir / "quiz" / "quiz.json"

    if not quiz_file.exists():
        raise EntityNotFoundException(f"Quiz not found for meeting {meeting_id}")

    with open(quiz_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return APIResponse(data=QuizRead(**data))

@router.get("/quiz/{meeting_id}/download", tags=["Study Materials"], dependencies=[RequireStudent])
async def download_quiz_md(meeting_id: str):
    """Retrieves quiz as Markdown."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    quiz_md = meeting_dir / "quiz" / "quiz.md"

    if not quiz_md.exists():
        raise EntityNotFoundException(f"Quiz Markdown not found for meeting {meeting_id}")

    return FileResponse(path=quiz_md, media_type="text/markdown")

@router.get("/flashcards/{meeting_id}", response_model=APIResponse[FlashcardRead], tags=["Study Materials"], dependencies=[RequireStudent])
async def get_flashcards(meeting_id: str):
    """Retrieves generated flashcards for a meeting."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    cards_file = meeting_dir / "flashcards" / "flashcards.json"

    if not cards_file.exists():
        raise EntityNotFoundException(f"Flashcards not found for meeting {meeting_id}")

    with open(cards_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return APIResponse(data=FlashcardRead(**data))

@router.get("/flashcards/{meeting_id}/download", tags=["Study Materials"], dependencies=[RequireStudent])
async def download_cards_md(meeting_id: str):
    """Retrieves flashcards as Markdown."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    cards_md = meeting_dir / "flashcards" / "flashcards.md"

    if not cards_md.exists():
        raise EntityNotFoundException(f"Flashcards Markdown not found for meeting {meeting_id}")

    return FileResponse(path=cards_md, media_type="text/markdown")

@router.get("/assignment/{meeting_id}", response_model=APIResponse[AssignmentRead], tags=["Study Materials"], dependencies=[RequireStudent])
async def get_assignment(meeting_id: str):
    """Retrieves generated assignment for a meeting."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    assign_file = meeting_dir / "assignment" / "assignment.json"

    if not assign_file.exists():
        raise EntityNotFoundException(f"Assignment not found for meeting {meeting_id}")

    with open(assign_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return APIResponse(data=AssignmentRead(**data))

@router.get("/assignment/{meeting_id}/download", tags=["Study Materials"], dependencies=[RequireStudent])
async def download_assign_md(meeting_id: str):
    """Retrieves assignment as Markdown."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    assign_md = meeting_dir / "assignment" / "assignment.md"

    if not assign_md.exists():
        raise EntityNotFoundException(f"Assignment Markdown not found for meeting {meeting_id}")

    return FileResponse(path=assign_md, media_type="text/markdown")

@router.get("/pack/{meeting_id}", response_model=APIResponse[StudyPackRead], tags=["Study Materials"], dependencies=[RequireStudent])
async def get_study_pack(meeting_id: str):
    """Retrieves the study pack manifest for a meeting."""
    meeting_dir = storage_manager.get_meeting_folder(meeting_id)
    pack_file = meeting_dir / "study_pack" / "study_pack.json"

    if not pack_file.exists():
        raise EntityNotFoundException(f"Study pack not found for meeting {meeting_id}")

    with open(pack_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Calculate basic stats from statistics.json if available
    stats = {}
    stats_file = meeting_dir / "study_pack" / "statistics.json"
    if stats_file.exists():
        with open(stats_file, "r", encoding="utf-8") as f:
            stats = json.load(f)

    return APIResponse(
        data=StudyPackRead(
            meeting_id=meeting_id,
            package_path=str(meeting_dir / "study_pack"),
            artifacts=list(data.get("contents", {}).keys()),
            stats=stats
        )
    )
