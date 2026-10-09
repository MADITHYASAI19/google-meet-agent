from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from backend.app.database.base import Base
import enum

class MeetingStatus(str, enum.Enum):
    JOINING = "joining"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class MeetingSession(Base):
    """
    Represents a Google Meet session captured by the AI Assistant.
    """
    __tablename__ = "meeting_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_url = Column(String, nullable=False)
    start_time = Column(DateTime, server_default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(SQLEnum(MeetingStatus), default=MeetingStatus.JOINING, nullable=False)

    def __repr__(self):
        return f"<MeetingSession(id={self.id}, status={self.status})>"
