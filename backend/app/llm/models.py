from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class LLMUsage(BaseModel):
    """Token usage statistics for an LLM request."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class LLMRequest(BaseModel):
    """Standardized request model for all LLM providers."""
    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LLMResponse(BaseModel):
    """Standardized response model for all LLM providers."""
    text: str
    provider: str
    model: str
    usage: LLMUsage
    latency: float
    finish_reason: str
    timestamp: datetime = Field(default_factory=datetime.now)
