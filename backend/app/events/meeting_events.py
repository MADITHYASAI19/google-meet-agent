from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class MeetingEvent:
    """Base class for all meeting-related events."""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MeetingStarted(MeetingEvent):
    meeting_id: str = ""
    url: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MeetingJoined(MeetingEvent):
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MeetingDisconnected(MeetingEvent):
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MeetingEnded(MeetingEvent):
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class BrowserClosed(MeetingEvent):
    meeting_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MeetingFailed(MeetingEvent):
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AudioCaptureStarted(MeetingEvent):
    meeting_id: str = ""
    file_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AudioCaptureStopped(MeetingEvent):
    meeting_id: str = ""
    file_path: str = ""
    duration_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AudioCaptureFailed(MeetingEvent):
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TranscriptionQueued(MeetingEvent):
    meeting_id: str = ""
    audio_file_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TranscriptionStarted(MeetingEvent):
    meeting_id: str = ""
    audio_file_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TranscriptionProgress(MeetingEvent):
    meeting_id: str = ""
    progress_percentage: float = 0.0
    current_segment: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TranscriptionCompleted(MeetingEvent):
    meeting_id: str = ""
    transcript_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TranscriptionFailed(MeetingEvent):
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Attendance Events ---

@dataclass
class ParticipantJoined(MeetingEvent):
    """Triggered when a participant joins the meeting."""
    meeting_id: str = ""
    participant_id: str = ""
    display_name: str = ""
    email: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ParticipantLeft(MeetingEvent):
    """Triggered when a participant leaves the meeting."""
    meeting_id: str = ""
    participant_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AttendanceStarted(MeetingEvent):
    """Published when attendance tracking begins for a meeting."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AttendanceUpdated(MeetingEvent):
    """Published when a participant's attendance status changes."""
    meeting_id: str = ""
    participant_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AttendanceCompleted(MeetingEvent):
    """Published when attendance tracking ends and files are written."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AttendanceFailed(MeetingEvent):
    """Published if attendance tracking fails."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Notes Generation Events ---

@dataclass
class NotesGenerationStarted(MeetingEvent):
    """Published when the notes generation pipeline starts."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class NotesGenerationProgress(MeetingEvent):
    """Published as each chunk of the transcript is processed."""
    meeting_id: str = ""
    chunk_index: int = 0
    total_chunks: int = 0
    progress_percentage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class NotesGenerationCompleted(MeetingEvent):
    """Published when final notes are generated and saved."""
    meeting_id: str = ""
    notes_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class NotesGenerationFailed(MeetingEvent):
    """Published if notes generation fails at any stage."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Quiz Generation Events ---

@dataclass
class QuizGenerationStarted(MeetingEvent):
    """Published when the quiz generation pipeline starts."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class QuizGenerationProgress(MeetingEvent):
    """Published as different stages of quiz generation complete."""
    meeting_id: str = ""
    stage: str = ""
    progress_percentage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class QuizGenerationCompleted(MeetingEvent):
    """Published when final quiz package is generated and saved."""
    meeting_id: str = ""
    quiz_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class QuizGenerationFailed(MeetingEvent):
    """Published if quiz generation fails at any stage."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Flashcard Generation Events ---

@dataclass
class FlashcardGenerationStarted(MeetingEvent):
    """Published when the flashcard generation pipeline starts."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FlashcardGenerationProgress(MeetingEvent):
    """Published as different stages of flashcard generation complete."""
    meeting_id: str = ""
    stage: str = ""
    progress_percentage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FlashcardGenerationCompleted(MeetingEvent):
    """Published when final flashcard package is generated and saved."""
    meeting_id: str = ""
    flashcard_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class FlashcardGenerationFailed(MeetingEvent):
    """Published if quiz generation fails at any stage."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Study Pack Generation Events ---

@dataclass
class StudyPackGenerationStarted(MeetingEvent):
    """Published when the study pack generation pipeline starts."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class StudyPackGenerationProgress(MeetingEvent):
    """Published as different stages of study pack generation complete."""
    meeting_id: str = ""
    stage: str = ""
    progress_percentage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class StudyPackGenerationCompleted(MeetingEvent):
    """Published when final study pack package is generated and saved."""
    meeting_id: str = ""
    study_pack_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class StudyPackGenerationFailed(MeetingEvent):
    """Published if study pack generation fails at any stage."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

# --- Assignment Generation Events ---

@dataclass
class AssignmentGenerationStarted(MeetingEvent):
    """Published when the assignment generation pipeline starts."""
    meeting_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AssignmentGenerationProgress(MeetingEvent):
    """Published as different stages of assignment generation complete."""
    meeting_id: str = ""
    stage: str = ""
    progress_percentage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AssignmentGenerationCompleted(MeetingEvent):
    """Published when final assignment package is generated and saved."""
    meeting_id: str = ""
    assignment_package_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AssignmentGenerationFailed(MeetingEvent):
    """Published if assignment generation fails at any stage."""
    meeting_id: str = ""
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
