import logging
from typing import Any
from backend.app.core.event_dispatcher import dispatcher
from backend.app.events.meeting_events import (
    MeetingStarted, TranscriptionCompleted, NotesGenerationCompleted,
    QuizGenerationCompleted, FlashcardGenerationCompleted,
    AssignmentGenerationCompleted, StudyPackGenerationCompleted,
    AttendanceCompleted
)
from backend.app.db.session import DBContextManager
from backend.app.repositories.meeting_repository import MeetingRepository
from backend.app.repositories.artifact_repositories import (
    TranscriptRepository, AttendanceRepository, NotesRepository,
    QuizRepository, FlashcardRepository, AssignmentRepository, StudyPackRepository
)
from backend.config.logging_config import setup_logging

logger = setup_logging()

class PersistenceListener:
    """
    Listens to system events and persists metadata to the database.
    This keeps the services pure and decouples business logic from persistence.
    """

    async def handle_meeting_started(self, event: MeetingStarted):
        async with DBContextManager() as session:
            repo = MeetingRepository(session)
            try:
                await repo.create(uuid=event.meeting_id, title="New Lecture")
                logger.info(f"Persisted new meeting: {event.meeting_id}")
            except Exception as e:
                logger.error(f"Failed to persist meeting {event.meeting_id}: {e}")

    async def handle_transcription_completed(self, event: TranscriptionCompleted):
        async with DBContextManager() as session:
            # We first need the internal meeting_id from the uuid
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            t_repo = TranscriptRepository(session)
            await t_repo.create(
                meeting_id=meeting.id,
                file_path=event.transcript_package_path
            )
            logger.info(f"Persisted transcript for meeting {event.meeting_id}")

    async def handle_notes_completed(self, event: NotesGenerationCompleted):
        async with DBContextManager() as session:
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            n_repo = NotesRepository(session)
            await n_repo.create(
                meeting_id=meeting.id,
                file_path=event.notes_package_path
            )
            logger.info(f"Persisted notes for meeting {event.meeting_id}")

    async def handle_quiz_completed(self, event: QuizGenerationCompleted):
        async with DBContextManager() as session:
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            q_repo = QuizRepository(session)
            await q_repo.create(
                meeting_id=meeting.id,
                file_path=event.quiz_package_path
            )
            logger.info(f"Persisted quiz for meeting {event.meeting_id}")

    async def handle_flashcards_completed(self, event: FlashcardGenerationCompleted):
        async with DBContextManager() as session:
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            f_repo = FlashcardRepository(session)
            await f_repo.create(
                meeting_id=meeting.id,
                file_path=event.flashcard_package_path
            )
            logger.info(f"Persisted flashcards for meeting {event.meeting_id}")

    async def handle_assignment_completed(self, event: AssignmentGenerationCompleted):
        async with DBContextManager() as session:
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            a_repo = AssignmentRepository(session)
            await a_repo.create(
                meeting_id=meeting.id,
                file_path=event.assignment_package_path
            )
            logger.info(f"Persisted assignment for meeting {event.meeting_id}")

    async def handle_study_pack_completed(self, event: StudyPackGenerationCompleted):
        async with DBContextManager() as session:
            m_repo = MeetingRepository(session)
            meeting = await m_repo.get_by_uuid(event.meeting_id)

            s_repo = StudyPackRepository(session)
            await s_repo.create(
                meeting_id=meeting.id,
                file_path=event.study_pack_package_path
            )
            logger.info(f"Persisted study pack for meeting {event.meeting_id}")

async def setup_persistence_listeners():
    """
    Registers the persistence listeners with the EventDispatcher.
    """
    listener = PersistenceListener()

    dispatcher.subscribe(MeetingStarted, listener.handle_meeting_started)
    dispatcher.subscribe(TranscriptionCompleted, listener.handle_transcription_completed)
    dispatcher.subscribe(NotesGenerationCompleted, listener.handle_notes_completed)
    dispatcher.subscribe(QuizGenerationCompleted, listener.handle_quiz_completed)
    dispatcher.subscribe(FlashcardGenerationCompleted, listener.handle_flashcards_completed)
    dispatcher.subscribe(AssignmentGenerationCompleted, listener.handle_assignment_completed)
    dispatcher.subscribe(StudyPackGenerationCompleted, listener.handle_study_pack_completed)
