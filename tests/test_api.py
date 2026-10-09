import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.storage_service import storage_manager
from pathlib import Path
import json
import os

# Use the FastAPI TestClient for synchronous tests or AsyncClient for async
client = TestClient(app)

@pytest.fixture
def mock_meeting_data(tmp_path):
    """Creates a dummy meeting directory structure for testing API retrieval."""
    meeting_id = "test_meeting_123"
    meeting_dir = tmp_path / meeting_id

    # Create necessary sub-folders
    (meeting_dir / "audio").mkdir(parents=True)
    (meeting_dir / "transcripts").mkdir(parents=True)
    (meeting_dir / "attendance").mkdir(parents=True)
    (meeting_dir / "notes").mkdir(parents=True)
    (meeting_dir / "quiz").mkdir(parents=True)
    (meeting_dir / "flashcards").mkdir(parents=True)
    (meeting_dir / "assignment").mkdir(parents=True)
    (meeting_dir / "study_pack").mkdir(parents=True)

    # Create dummy files
    with open(meeting_dir / "audio" / "lecture_audio.wav", "wb") as f:
        f.write(b"fake audio data")

    with open(meeting_dir / "transcripts" / "transcript.json", "w") as f:
        json.dump({"full_text": "Hello world", "segments": []}, f)

    with open(meeting_dir / "transcripts" / "transcript.md", "w") as f:
        f.write("# Transcript\nHello world")

    with open(meeting_dir / "attendance" / "attendance.json", "w") as f:
        json.dump([{"participant_id": "p1", "display_name": "User 1", "joined_at": "2023-01-01T10:00:00"}], f)

    with open(meeting_dir / "notes" / "notes.json", "w") as f:
        json.dump({
            "title": "Test Lecture",
            "summary": "Summary",
            "key_takeaways": ["T1"],
            "detailed_notes": "Details",
            "generated_at": "2023-01-01T10:00:00"
        }, f)

    with open(meeting_dir / "notes" / "notes.md", "w") as f:
        f.write("# Notes\nDetailed notes")

    # Monkeypatch storage_manager to use this tmp_path
    original_get_folder = storage_manager.get_meeting_folder
    storage_manager.get_meeting_folder = lambda mid: tmp_path / mid

    yield meeting_id

    # Restore original method
    storage_manager.get_meeting_folder = original_get_folder

def test_health_endpoint():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "status" in data["data"]

def test_join_meeting():
    payload = {"meeting_id": "meet123", "url": "https://meet.google.com/abc"}
    response = client.post("/api/v1/meetings/", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["meeting_id"] == "meet123"

def test_get_meeting_not_found():
    response = client.get("/api/v1/meetings/non_existent")
    assert response.status_code == 404

def test_get_meeting_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/meetings/{meeting_id}")
    assert response.status_code == 200
    assert response.json()["data"]["meeting_id"] == meeting_id

def test_download_audio_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/audio/{meeting_id}/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"

def test_get_transcription_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/transcriptions/{meeting_id}")
    assert response.status_code == 200
    assert response.json()["data"]["full_text"] == "Hello world"

def test_get_attendance_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/attendance/{meeting_id}")
    assert response.status_code == 200
    assert len(response.json()["data"]["participants"]) == 1

def test_get_notes_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/notes/{meeting_id}")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Test Lecture"

def test_download_notes_md_success(mock_meeting_data):
    meeting_id = mock_meeting_data
    response = client.get(f"/api/v1/notes/{meeting_id}/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/markdown"
