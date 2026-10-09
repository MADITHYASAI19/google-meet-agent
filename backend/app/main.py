from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import os
from pathlib import Path

from backend.app.config.settings import settings
from backend.app.config.logging_config import setup_logging
from backend.app.services.storage_service import storage_manager
from backend.app.core.exceptions import register_exception_handlers
from backend.app.database.database import engine
from backend.app.services.audio_capture_service import audio_capture_service

# API Routers
from backend.app.api import (
    health, meetings, audio, transcription,
    attendance, notes, study_materials, auth
)
# WebSocket Router
from backend.app.websocket import routes as websocket_router

# Initialize logging
logger = setup_logging()

# --- Production Middleware ---

class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to log the execution time of each request."""
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Process-Time"] = str(f"{process_time:.2f}ms")
        return response

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add a unique request ID to each response."""
    async def dispatch(self, request: Request, call_next):
        import uuid
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    debug=settings.app.debug
)

# 1. Security & Performance Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.server.trusted_hosts)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, this should be settings.server.cors_origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Static Files Serving
from fastapi.staticfiles import StaticFiles
# Auto-create storage dirs before mounting
for dir_name in settings.storage.required_dirs:
    os.makedirs(os.path.join(settings.storage.base_path, dir_name), exist_ok=True)

app.mount("/storage", StaticFiles(directory=settings.storage.base_path), name="storage")

# Include Routers
api_prefix = settings.server.api_prefix

app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(health.router, prefix=f"{api_prefix}/health", tags=["Health"])
app.include_router(meetings.router, prefix=f"{api_prefix}/meetings", tags=["Meetings"])
app.include_router(audio.router, prefix=f"{api_prefix}/audio", tags=["Audio"])
app.include_router(transcription.router, prefix=f"{api_prefix}/transcriptions", tags=["Transcriptions"])
app.include_router(attendance.router, prefix=f"{api_//attendance}", tags=["Attendance"])
app.include_router(notes.router, prefix=f"{api_prefix}/notes", tags=["Notes"])
app.include_router(study_materials.router, prefix=f"{api_prefix}/study-materials", tags=["Study Materials"])
app.include_router(websocket_router.router)

# Register global exception handlers
register_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    """
    Application startup logic.
    """
    logger.info("Starting up AI Lecture Assistant Backend...")
    storage_manager.initialize_storage()

    # Ensure logs directory exists
    os.makedirs(settings.logging.path, exist_ok=True)

    # Verify DB connectivity
    try:
        from backend.app.db.database import engine as async_engine, init_db
        await init_db()
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    # Setup Event Subscriptions
    from backend.app.core.event_dispatcher import dispatcher
    from backend.app.events.meeting_events import (
        MeetingJoined, MeetingEnded, AudioCaptureStopped,
        TranscriptionCompleted, NotesGenerationCompleted,
        AssignmentGenerationCompleted
    )
    dispatcher.subscribe(MeetingJoined, audio_capture_service.handle_meeting_joined)
    dispatcher.subscribe(MeetingEnded, audio_capture_service.handle_meeting_ended)
    from backend.app.services.attendance_service import attendance_service
    from backend.app.events.meeting_events import ParticipantJoined, ParticipantLeft
    dispatcher.subscribe(MeetingJoined, attendance_service.handle_meeting_joined)
    dispatcher.subscribe(MeetingEnded, attendance_service.handle_meeting_ended)
    dispatcher.subscribe(ParticipantJoined, attendance_service.handle_participant_joined)
    dispatcher.subscribe(ParticipantLeft, attendance_service.handle_participant_left)
    from backend.app.services.notes_service import notes_service
    dispatcher.subscribe(TranscriptionCompleted, notes_service.handle_transcription_completed)
    from backend.app.services.quiz_service import quiz_service
    dispatcher.subscribe(NotesGenerationCompleted, quiz_service.handle_notes_completed)
    from backend.app.services.flashcard_service import flashcard_service
    dispatcher.subscribe(NotesGenerationCompleted, flashcard_service.handle_notes_completed)
    from backend.app.services.assignment_service import assignment_service
    dispatcher.subscribe(NotesGenerationCompleted, assignment_service.handle_notes_completed)
    from backend.app.services.study_pack_service import study_pack_service
    dispatcher.subscribe(AssignmentGenerationCompleted, study_pack_service.handle_assignment_completed)
    from backend.app.services.whisper_transcription_service import whisper_transcription_service
    dispatcher.subscribe(AudioCaptureStopped, whisper_transcription_service.handle_audio_capture_stopped)
    from backend.app.websocket.broadcaster import broadcaster
    await broadcaster.setup_subscriptions()
    from backend.app.core.persistence_listeners import setup_persistence_listeners
    await setup_persistence_listeners()
    logger.info("Backend foundation initialized successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown logic.
    """
    logger.info("Shutting down AI Lecture Assistant Backend...")
    from backend.app.db.database import engine as async_engine
    await async_engine.dispose()
    from backend.app.database.database import engine as old_engine
    old_engine.dispose()
    audio_capture_service.shutdown()
    from backend.app.services.whisper_model_manager import whisper_model_manager
    whisper_model_manager.unload_model()
    logger.info("Backend shutdown complete.")
