from typing import List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError

from backend.app.db.models import (
    Transcript, Attendance, Notes, Quiz, Flashcards, Assignment, StudyPack
)
from backend.app.core.exceptions import EntityNotFoundException

class BaseArtifactRepository:
    """
    Generic repository for AI-generated artifacts.
    """
    def __init__(self, session: AsyncSession, model: Any):
        self.session = session
        self.model = model

    async def create(self, meeting_id: int, file_path: str, **kwargs) -> Any:
        """Creates a record for an AI artifact."""
        try:
            instance = self.model(
                meeting_id=meeting_id,
                file_path=file_path,
                **kwargs
            )
            self.session.add(instance)
            await self.session.flush()
            return instance
        except SQLAlchemyError as e:
            raise Exception(f"Error creating {self.model.__tablename__}: {str(e)}")

    async def get_by_meeting(self, meeting_id: int) -> Any:
        """Retrieves the artifact associated with a meeting."""
        result = await self.session.execute(
            select(self.model).where(self.model.meeting_id == meeting_id)
        )
        artifact = result.scalar_one_or_none()
        if not artifact:
            raise EntityNotFoundException(f"{self.model.__name__} not found for meeting {meeting_id}")
        return artifact

class TranscriptRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Transcript)

class AttendanceRepository:
    """
    Specialized repository for Attendance as it handles multiple participants.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_participant(self, participant_data: Dict[str, Any]) -> Attendance:
        try:
            attendance = Attendance(**participant_data)
            self.session.add(attendance)
            await self.session.flush()
            return attendance
        except SQLAlchemyError as e:
            raise Exception(f"Error saving attendance: {str(e)}")

    async def get_by_meeting(self, meeting_id: int) -> List[Attendance]:
        result = await self.session.execute(
            select(Attendance).where(Attendance.meeting_id == meeting_id)
        )
        return result.scalars().all()

class NotesRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Notes)

class QuizRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Quiz)

class FlashcardRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Flashcards)

class AssignmentRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Assignment)

class StudyPackRepository(BaseArtifactRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StudyPack)
