from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional, List, Any, Dict
from datetime import datetime

T = TypeVar("T")

# --- Generic API Wrappers ---

class APIResponse(BaseModel, Generic[T]):
    """Standard wrapper for all successful API responses."""
    success: bool = True
    data: T
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Standard wrapper for all API error responses."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# --- Meeting Schemas ---

class MeetingBase(BaseModel):
    meeting_id: str
    url: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingRead(MeetingBase):
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# --- Transcription Schemas ---

class TranscriptionSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker: Optional[str] = "Unknown"

class TranscriptionRead(BaseModel):
    meeting_id: str
    full_text: str
    segments: List[TranscriptionSegment]
    status: str

# --- Attendance Schemas ---

class ParticipantRead(BaseModel):
    participant_id: str
    display_name: str
    email: Optional[str] = None
    joined_at: datetime
    left_at: Optional[datetime] = None

class AttendanceRead(BaseModel):
    meeting_id: str
    participants: List[ParticipantRead]
    total_count: int

# --- AI Artifact Schemas (Notes, Quiz, etc.) ---

class ArtifactResponse(BaseModel):
    """Generic response for JSON-based AI artifacts."""
    meeting_id: str
    content: Dict[str, Any]
    generated_at: datetime
    provider: str
    model: str

class NotesRead(BaseModel):
    meeting_id: str
    title: str
    summary: str
    key_takeaways: List[str]
    detailed_notes: str
    generated_at: datetime

class QuizRead(BaseModel):
    meeting_id: str
    title: str
    mcqs: List[Dict[str, Any]]
    true_false: List[Dict[str, Any]]
    fill_blanks: List[Dict[str, Any]]
    subjective: List[Dict[str, Any]]
    answer_key: Dict[str, Any]

class FlashcardRead(BaseModel):
    meeting_id: str
    cards: List[Dict[str, Any]] # [{ "front": "...", "back": "..." }]

class AssignmentRead(BaseModel):
    meeting_id: str
    title: str
    instructions: str
    questions: List[Dict[str, Any]]
    rubric: Dict[str, Any]

class StudyPackRead(BaseModel):
    meeting_id: str
    package_path: str
    artifacts: List[str]
    stats: Dict[str, Any]

# --- Health Schemas ---

class HealthDetail(BaseModel):
    status: str # "healthy" | "unhealthy" | "degraded"
    latency_ms: Optional[float] = None
    message: Optional[str] = None

class HealthStatus(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, HealthDetail]
