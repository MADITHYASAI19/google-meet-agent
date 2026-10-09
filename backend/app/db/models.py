from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Float, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

class Meeting(Base):
    """
    Central entity for a lecture session.
    All other study artifacts relate back to a Meeting.
    """
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    platform: Mapped[str] = mapped_column(String(50), default="google_meet")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50), default="scheduled") # scheduled, active, completed, failed

    # Relationships with cascade delete to ensure metadata cleanup
    transcripts: Mapped[List["Transcript"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    attendance: Mapped[List["Attendance"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    notes: Mapped[Optional["Notes"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    quizzes: Mapped[List["Quiz"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    flashcards: Mapped[List["Flashcards"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    assignments: Mapped[List["Assignment"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )
    study_packs: Mapped[List["StudyPack"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )

class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en")
    duration: Mapped[float] = mapped_column(Float, default=0.0)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meeting: Mapped["Meeting"] = relationship(back_populates="transcripts")

class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    participant_id: Mapped[str] = mapped_column(String(128), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    join_count: Mapped[int] = mapped_column(Integer, default=1)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0)

    meeting: Mapped["Meeting"] = relationship(back_populates="attendance")

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meeting: Mapped["Meeting"] = relationship(back_populates="notes")

class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    question_count: Mapped[int] = mapped_column(Integer, default=0)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meeting: Mapped["Meeting"] = relationship(back_populates="quizzes")

class Flashcards(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    card_count: Mapped[int] = mapped_column(Integer, default=0)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meeting: Mapped["Meeting"] = relationship(back_populates="flashcards")

class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    total_marks: Mapped[int] = mapped_column(Integer, default=0)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meeting: Mapped["Meeting"] = relationship(back_populates="assignments")

class StudyPack(Base):
    __tablename__ = "study_packs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), unique=True, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    package_path: Mapped[str] = mapped_column(String(512), nullable=False)

    meeting: Mapped["Meeting"] = relationship(back_populates="study_packs")
