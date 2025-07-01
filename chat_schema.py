from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Annotated


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: Annotated[str, Field(min_length=1, max_length=2000)] = Field(
        ..., 
        description="User message about SMA",
        example="What are the main types of SMA?"
    )

    @field_validator('message')
    @classmethod
    def validate_message_content(cls, v: str) -> str:
        """Ensure message is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or only whitespace")
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(
        ..., 
        description="AI response about SMA",
        min_length=1
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
        ..., 
        description="Confidence score between 0.0 and 1.0"
    )
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )

    @field_validator('answer')
    @classmethod
    def validate_answer_content(cls, v: str) -> str:
        """Ensure answer is not empty"""
        if not v or not v.strip():
            raise ValueError("Answer cannot be empty")
        return v.strip()

    @field_validator('confidence')
    @classmethod
    def validate_confidence_bounds(cls, v: float) -> float:
        """Ensure confidence is within valid bounds"""
        if not (0.0 <= v <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = "ok"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
