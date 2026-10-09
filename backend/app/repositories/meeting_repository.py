from typing import Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from backend.app.db.models import Meeting
from backend.app.core.exceptions import EntityNotFoundException

class MeetingRepository:
    """
    Repository for Meeting metadata.
    Handles all persistence logic for the Meeting aggregate.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, uuid: str, title: Optional[str] = None, platform: str = "google_meet") -> Meeting:
        """Creates a new meeting record."""
        try:
            meeting = Meeting(
                uuid=uuid,
                title=title,
                platform=platform,
                status="scheduled"
            )
            self.session.add(meeting)
            await self.session.flush() # Get the ID without committing
            return meeting
        except SQLAlchemyError as e:
            raise Exception(f"Database error creating meeting: {str(e)}")

    async def get_by_uuid(self, uuid: str) -> Meeting:
        """Retrieves a meeting by its business UUID."""
        result = await self.session.execute(select(Meeting).where(Meeting.uuid == uuid))
        meeting = result.scalar_one_or_none()
        if not meeting:
            raise EntityNotFoundException(f"Meeting with UUID {uuid} not found")
        return meeting

    async def get_by_id(self, meeting_id: int) -> Meeting:
        """Retrieves a meeting by its primary key."""
        result = await self.session.get(Meeting, meeting_id)
        if not result:
            raise EntityNotFoundException(f"Meeting with ID {meeting_id} not found")
        return result

    async def update(self, meeting_id: int, data: Dict[str, Any]) -> Meeting:
        """Updates specific fields of a meeting."""
        meeting = await self.get_by_id(meeting_id)
        for key, value in data.items():
            setattr(meeting, key, value)

        await self.session.flush()
        return meeting

    async def delete(self, meeting_id: int) -> bool:
        """Deletes a meeting and all its cascaded artifacts."""
        meeting = await self.get_by_id(meeting_id)
        await self.session.delete(meeting)
        await self.session.flush()
        return True

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Meeting]:
        """Lists meetings with pagination."""
        result = await self.session.execute(
            select(Meeting).offset(offset).limit(limit)
        )
        return result.scalars().all()
