from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from datetime import datetime

class WebSocketEvent(BaseModel):
    """Unified JSON schema for all WebSocket messages."""
    event: str = Field(..., description="The type of event (e.g., 'transcription_progress')")
    meeting_id: Optional[str] = Field(None, description="The ID of the meeting this event relates to")
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = Field("info", description="Event status: info, success, warning, error")
    progress: float = Field(0.0, description="Progress percentage (0-100)")
    message: Optional[str] = Field(None, description="Human-readable message")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event-specific data")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
