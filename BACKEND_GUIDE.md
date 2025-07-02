# Backend Development Guide

## Overview

This guide covers backend development for the SMA Medical Assistant using FastAPI, LangChain, and Google Gemini.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [FastAPI Fundamentals](#fastapi-fundamentals)
3. [LangChain Integration](#langchain-integration)
4. [Data Models & Validation](#data-models--validation)
5. [Error Handling](#error-handling)
6. [Testing Strategy](#testing-strategy)
7. [Security Considerations](#security-considerations)
8. [Performance Optimization](#performance-optimization)

## Architecture Overview

### Backend Architecture Diagram

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└─────────┬───────┘
          │
    ┌─────▼─────┐
    │  Router   │
    │ Endpoints │
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │  Schema   │
    │Validation │
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │ Workflow  │
    │ Business  │
    │  Logic    │
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │ LangChain │
    │   Client  │
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │  Gemini   │
    │ AI Model  │
    └───────────┘
```

### Key Components

1. **FastAPI Application** - HTTP server and routing
2. **Pydantic Models** - Data validation and serialization
3. **LangChain Client** - AI model integration
4. **Workflow Engine** - Business logic processing
5. **Utility Functions** - Helper functions and validation

## FastAPI Fundamentals

### Application Setup

```python
# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting SMA Medical Assistant API")
    
    # Startup logic
    await initialize_ai_client()
    
    yield
    
    # Shutdown logic
    logger.info("Shutting down SMA Medical Assistant API")
    await cleanup_resources()

app = FastAPI(
    title="SMA Medical Assistant API",
    description="AI-powered medical Q&A for Spinal Muscular Atrophy",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:4200").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

async def initialize_ai_client():
    """Initialize AI client on startup"""
    try:
        from gemma_client import GemmaClient
        global ai_client
        ai_client = GemmaClient(api_key=os.getenv("GOOGLE_API_KEY"))
        logger.info("AI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI client: {e}")
        raise

async def cleanup_resources():
    """Cleanup resources on shutdown"""
    # Close database connections, cleanup caches, etc.
    pass
```

### Route Handlers

```python
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import ValidationError
from typing import List, Optional
import time

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks
) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    Args:
        request: Chat request containing user message
        background_tasks: Background task queue
        
    Returns:
        ChatResponse with AI answer and metadata
        
    Raises:
        HTTPException: For validation or processing errors
    """
    start_time = time.time()
    
    try:
        # Log request (without sensitive data)
        logger.info(f"Processing chat request: {len(request.message)} chars")
        
        # Validate message content
        if not is_sma_related(request.message):
            raise HTTPException(
                status_code=400,
                detail="I can only provide information about Spinal Muscular Atrophy (SMA)"
            )
        
        # Process through workflow
        workflow_result = await process_chat_message(request.message)
        
        # Create response
        response = ChatResponse(
            answer=workflow_result.answer,
            confidence=workflow_result.confidence,
            timestamp=datetime.utcnow(),
            response_time_ms=int((time.time() - start_time) * 1000)
        )
        
        # Log metrics in background
        background_tasks.add_task(
            log_metrics,
            request.message,
            response.confidence,
            response.response_time_ms
        )
        
        return response
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        )

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring.
    
    Returns:
        HealthResponse with system status
    """
    try:
        # Check AI client health
        ai_status = await check_ai_client_health()
        
        return HealthResponse(
            status="healthy" if ai_status else "degraded",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            dependencies={
                "ai_model": "available" if ai_status else "unavailable",
                "memory_usage": get_memory_usage(),
                "uptime_seconds": get_uptime()
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            error=str(e)
        )

# Include router in main app
app.include_router(router)
```

### Dependency Injection

```python
from functools import lru_cache
from typing import Annotated

@lru_cache()
def get_settings():
    """Get application settings (cached)"""
    return Settings()

@lru_cache()
def get_ai_client():
    """Get AI client instance (cached)"""
    settings = get_settings()
    return GemmaClient(api_key=settings.google_api_key)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user (future feature)"""
    # User authentication logic
    pass

# Use in endpoints
@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    ai_client: Annotated[GemmaClient, Depends(get_ai_client)],
    settings: Annotated[Settings, Depends(get_settings)]
):
    # Endpoint logic with injected dependencies
    pass
```

## LangChain Integration

### LangChain Client Implementation

```python
# gemma_client.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Optional, List, Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

class GemmaClient:
    """Google Gemini client with LangChain integration"""
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-pro",
        temperature: float = 0.1,
        max_tokens: Optional[int] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        
        # Initialize LangChain LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
            callback_manager=CallbackManager([
                StreamingStdOutCallbackHandler()
            ]) if logger.level <= logging.DEBUG else None
        )
        
        # Load system prompt
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("System prompt file not found, using default")
            return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Default system prompt if file not found"""
        return """
        You are a medical assistant specialized in Spinal Muscular Atrophy (SMA).
        Provide accurate, helpful information about SMA while being clear that
        you cannot replace professional medical advice.
        
        Always respond in JSON format with 'answer' and 'confidence' fields.
        Confidence should be between 0.0 and 1.0.
        """
    
    async def generate_response(
        self,
        message: str,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response for user message.
        
        Args:
            message: User's question about SMA
            context: Optional conversation context
            
        Returns:
            Dictionary with answer and confidence score
            
        Raises:
            Exception: If AI generation fails
        """
        try:
            # Prepare messages
            messages = [SystemMessage(content=self.system_prompt)]
            
            # Add context if provided
            if context:
                for ctx in context[-3:]:  # Last 3 messages for context
                    if ctx.get("role") == "user":
                        messages.append(HumanMessage(content=ctx["content"]))
                    # Note: Add AssistantMessage when available in LangChain
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Generate response
            logger.debug(f"Generating response for message: {message[:50]}...")
            
            response = await asyncio.to_thread(
                self.llm.invoke,
                messages
            )
            
            # Parse response
            return self._parse_response(response.content)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def _parse_response(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        
        Args:
            raw_response: Raw response from LLM
            
        Returns:
            Parsed response with answer and confidence
        """
        try:
            import json
            import re
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                parsed = json.loads(json_str)
                
                return {
                    "answer": parsed.get("answer", raw_response),
                    "confidence": float(parsed.get("confidence", 0.8))
                }
            else:
                # Fallback: treat entire response as answer
                return {
                    "answer": raw_response,
                    "confidence": 0.7  # Lower confidence for non-JSON
                }
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return {
                "answer": raw_response,
                "confidence": 0.6  # Even lower confidence for parse errors
            }
    
    async def check_health(self) -> bool:
        """
        Check if AI client is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            test_response = await self.generate_response(
                "What is SMA? Please respond briefly."
            )
            return bool(test_response.get("answer"))
        except Exception:
            return False

class EnhancedGemmaClient(GemmaClient):
    """Enhanced client with additional features"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_memory = []
        self.rate_limiter = RateLimiter(max_calls=60, time_window=60)
    
    async def generate_response_with_memory(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate response with conversation memory"""
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # Get conversation context
        context = self._get_conversation_context(conversation_id)
        
        # Generate response
        response = await self.generate_response(message, context)
        
        # Update memory
        self._update_conversation_memory(
            conversation_id, message, response["answer"]
        )
        
        return response
    
    def _get_conversation_context(
        self, conversation_id: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Get conversation context from memory"""
        if not conversation_id:
            return []
        
        # Filter messages for this conversation
        return [
            msg for msg in self.conversation_memory
            if msg.get("conversation_id") == conversation_id
        ]
    
    def _update_conversation_memory(
        self,
        conversation_id: Optional[str],
        user_message: str,
        ai_response: str
    ):
        """Update conversation memory"""
        if not conversation_id:
            return
        
        timestamp = datetime.utcnow()
        
        # Add user message
        self.conversation_memory.append({
            "conversation_id": conversation_id,
            "role": "user",
            "content": user_message,
            "timestamp": timestamp
        })
        
        # Add AI response
        self.conversation_memory.append({
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response,
            "timestamp": timestamp
        })
        
        # Keep only recent messages (memory management)
        max_messages = 100
        if len(self.conversation_memory) > max_messages:
            self.conversation_memory = self.conversation_memory[-max_messages:]

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    async def acquire(self):
        """Acquire rate limit permission"""
        now = time.time()
        
        # Remove old calls outside time window
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < self.time_window]
        
        # Check if we can make a call
        if len(self.calls) >= self.max_calls:
            wait_time = self.time_window - (now - self.calls[0])
            await asyncio.sleep(wait_time)
        
        # Record this call
        self.calls.append(now)
```

### LangChain Chains and Prompts

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

class SMAQAChain:
    """Specialized chain for SMA Q&A"""
    
    def __init__(self, llm):
        self.llm = llm
        self.chain = self._create_chain()
    
    def _create_chain(self):
        """Create LangChain chain for SMA Q&A"""
        
        # Define prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a specialized medical assistant for Spinal Muscular Atrophy (SMA).
            
            Guidelines:
            1. Only answer questions related to SMA
            2. Provide accurate, evidence-based information
            3. Always clarify that you cannot replace professional medical advice
            4. If unsure, recommend consulting healthcare professionals
            5. Respond in JSON format with 'answer' and 'confidence' fields
            
            Confidence scoring:
            - 0.9-1.0: Well-established medical facts
            - 0.7-0.9: Generally accepted information
            - 0.5-0.7: Contextual or nuanced information
            - 0.3-0.5: Uncertain or limited information
            - 0.0-0.3: Highly uncertain
            """),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create memory for conversation
        memory = ConversationBufferWindowMemory(
            k=5,  # Remember last 5 exchanges
            memory_key="history",
            return_messages=True
        )
        
        # Create chain
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=memory,
            verbose=True
        )
    
    async def ask(self, question: str) -> Dict[str, Any]:
        """Ask a question about SMA"""
        try:
            response = await self.chain.arun(input=question)
            return self._parse_json_response(response)
        except Exception as e:
            logger.error(f"Chain execution failed: {e}")
            return {
                "answer": "I apologize, but I'm having trouble processing your question right now. Please try again or consult a healthcare professional.",
                "confidence": 0.0
            }
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM"""
        try:
            import json
            import re
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {
                    "answer": response,
                    "confidence": 0.7
                }
        except:
            return {
                "answer": response,
                "confidence": 0.6
            }
```

## Data Models & Validation

### Pydantic Models

```python
# chat_schema.py
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import re

class MessageType(str, Enum):
    """Types of messages in the system"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ConfidenceLevel(str, Enum):
    """Confidence level categories"""
    VERY_HIGH = "very_high"  # 0.9-1.0
    HIGH = "high"            # 0.7-0.9
    MEDIUM = "medium"        # 0.5-0.7
    LOW = "low"              # 0.3-0.5
    VERY_LOW = "very_low"    # 0.0-0.3

class ChatRequest(BaseModel):
    """Request model for chat messages"""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question about SMA"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation identifier"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional context information"
    )
    
    @validator('message')
    def validate_message_content(cls, v):
        """Validate message content"""
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        
        # Check for potentially harmful content
        if cls._contains_harmful_content(v):
            raise ValueError('Message contains inappropriate content')
        
        return v.strip()
    
    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation ID format"""
        if v is not None:
            if not re.match(r'^[a-zA-Z0-9_-]+$', v):
                raise ValueError('Invalid conversation ID format')
        return v
    
    @staticmethod
    def _contains_harmful_content(text: str) -> bool:
        """Check for harmful content (basic implementation)"""
        harmful_patterns = [
            r'\b(suicide|kill|harm|hurt)\b',
            r'\b(drug|medication)\s+(dealer|buy|sell)\b'
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, text.lower()):
                return True
        return False

class ChatResponse(BaseModel):
    """Response model for chat responses"""
    
    answer: str = Field(
        ...,
        description="AI-generated response about SMA"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0-1.0)"
    )
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Categorical confidence level"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    sources: Optional[List[str]] = Field(
        None,
        description="Information sources"
    )
    response_time_ms: Optional[int] = Field(
        None,
        description="Response generation time in milliseconds"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Conversation identifier"
    )
    
    @validator('confidence_level', pre=True, always=True)
    def set_confidence_level(cls, v, values):
        """Automatically set confidence level based on score"""
        confidence = values.get('confidence', 0.0)
        
        if confidence >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 0.7:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif confidence >= 0.3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    class Config:
        """Pydantic configuration"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "answer": "Spinal Muscular Atrophy (SMA) is a genetic disorder...",
                "confidence": 0.95,
                "confidence_level": "very_high",
                "timestamp": "2025-07-01T12:00:00.000Z",
                "sources": ["Medical literature", "Clinical guidelines"],
                "response_time_ms": 1250
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Health check timestamp"
    )
    dependencies: Optional[Dict[str, Any]] = Field(
        None,
        description="Status of external dependencies"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if unhealthy"
    )

class ValidationError(BaseModel):
    """Custom validation error model"""
    
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    
class APIError(BaseModel):
    """API error response model"""
    
    detail: str = Field(..., description="Error details")
    status_code: int = Field(..., description="HTTP status code")
    error_type: str = Field(..., description="Error type")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
    request_id: Optional[str] = Field(
        None,
        description="Request identifier for tracking"
    )

# Input validation utilities
class MessageValidator:
    """Utility class for message validation"""
    
    SMA_KEYWORDS = [
        'sma', 'spinal muscular atrophy', 'motor neuron',
        'nusinersen', 'spinraza', 'zolgensma', 'risdiplam',
        'muscle weakness', 'respiratory', 'scoliosis'
    ]
    
    @classmethod
    def is_sma_related(cls, message: str) -> bool:
        """Check if message is related to SMA"""
        message_lower = message.lower()
        
        # Check for SMA keywords
        for keyword in cls.SMA_KEYWORDS:
            if keyword in message_lower:
                return True
        
        # Check for general medical terms that might be SMA-related
        medical_terms = ['treatment', 'symptom', 'diagnosis', 'therapy']
        sma_mentioned = any(sma in message_lower for sma in ['sma', 'spinal muscular'])
        
        if sma_mentioned and any(term in message_lower for term in medical_terms):
            return True
        
        return False
    
    @classmethod
    def extract_intent(cls, message: str) -> str:
        """Extract user intent from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['what is', 'define', 'explain']):
            return 'definition'
        elif any(word in message_lower for word in ['symptom', 'signs']):
            return 'symptoms'
        elif any(word in message_lower for word in ['treatment', 'therapy', 'medication']):
            return 'treatment'
        elif any(word in message_lower for word in ['cause', 'genetic', 'inherit']):
            return 'causes'
        elif any(word in message_lower for word in ['diagnose', 'test', 'detection']):
            return 'diagnosis'
        else:
            return 'general'
```

## Error Handling

### Custom Exception Classes

```python
# exceptions.py
from typing import Optional, Dict, Any

class SMAAssistantException(Exception):
    """Base exception for SMA Assistant"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)

class ValidationException(SMAAssistantException):
    """Exception for validation errors"""
    
    def __init__(self, message: str, field: str = None, **kwargs):
        super().__init__(message, "VALIDATION_ERROR", **kwargs)
        self.field = field

class AIServiceException(SMAAssistantException):
    """Exception for AI service errors"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, "AI_SERVICE_ERROR", **kwargs)

class RateLimitException(SMAAssistantException):
    """Exception for rate limiting"""
    
    def __init__(self, message: str = "Rate limit exceeded", **kwargs):
        super().__init__(message, "RATE_LIMIT_ERROR", **kwargs)

class ContentFilterException(SMAAssistantException):
    """Exception for content filtering"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, "CONTENT_FILTER_ERROR", **kwargs)
```

### Error Handler Middleware

```python
# middleware/error_handler.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback
import uuid

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Generate request ID for tracking
            request_id = str(uuid.uuid4())
            request.state.request_id = request_id
            
            response = await call_next(request)
            return response
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
            
        except ValidationException as e:
            logger.warning(f"Validation error: {e.message}", extra={
                "request_id": request_id,
                "field": e.field
            })
            
            return JSONResponse(
                status_code=400,
                content={
                    "detail": e.message,
                    "error_type": "validation_error",
                    "field": e.field,
                    "request_id": request_id
                }
            )
            
        except RateLimitException as e:
            logger.warning(f"Rate limit exceeded: {e.message}", extra={
                "request_id": request_id
            })
            
            return JSONResponse(
                status_code=429,
                content={
                    "detail": e.message,
                    "error_type": "rate_limit_error",
                    "request_id": request_id
                }
            )
            
        except AIServiceException as e:
            logger.error(f"AI service error: {e.message}", extra={
                "request_id": request_id,
                "details": e.details
            })
            
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "AI service temporarily unavailable",
                    "error_type": "service_unavailable",
                    "request_id": request_id
                }
            )
            
        except Exception as e:
            # Log unexpected errors with full traceback
            logger.error(f"Unexpected error: {str(e)}", extra={
                "request_id": request_id,
                "traceback": traceback.format_exc()
            })
            
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_type": "internal_error",
                    "request_id": request_id
                }
            )

# Add to FastAPI app
app.add_middleware(ErrorHandlerMiddleware)
```

## Testing Strategy

### Test Structure

```python
# tests/conftest.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from api.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_ai_client(monkeypatch):
    """Mock AI client for testing"""
    class MockAIClient:
        async def generate_response(self, message: str) -> dict:
            return {
                "answer": "This is a mock response about SMA.",
                "confidence": 0.9
            }
        
        async def check_health(self) -> bool:
            return True
    
    mock_client = MockAIClient()
    monkeypatch.setattr("api.main.ai_client", mock_client)
    return mock_client

@pytest.fixture
def sample_chat_request():
    """Sample chat request data"""
    return {
        "message": "What is Spinal Muscular Atrophy?",
        "conversation_id": "test-conv-123"
    }
```

### Unit Tests

```python
# tests/test_models.py
import pytest
from pydantic import ValidationError
from chat_schema import ChatRequest, ChatResponse

class TestChatRequest:
    """Test ChatRequest model"""
    
    def test_valid_request(self):
        """Test valid chat request"""
        request = ChatRequest(message="What is SMA?")
        assert request.message == "What is SMA?"
        assert request.conversation_id is None
    
    def test_empty_message_validation(self):
        """Test empty message validation"""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message="")
        
        assert "Message cannot be empty" in str(exc_info.value)
    
    def test_whitespace_message_validation(self):
        """Test whitespace-only message validation"""
        with pytest.raises(ValidationError):
            ChatRequest(message="   ")
    
    def test_message_too_long(self):
        """Test message length validation"""
        long_message = "x" * 1001
        with pytest.raises(ValidationError):
            ChatRequest(message=long_message)
    
    def test_message_trimming(self):
        """Test message trimming"""
        request = ChatRequest(message="  What is SMA?  ")
        assert request.message == "What is SMA?"
    
    def test_conversation_id_validation(self):
        """Test conversation ID validation"""
        # Valid IDs
        ChatRequest(message="Test", conversation_id="valid-id_123")
        
        # Invalid IDs
        with pytest.raises(ValidationError):
            ChatRequest(message="Test", conversation_id="invalid id with spaces")

class TestChatResponse:
    """Test ChatResponse model"""
    
    def test_valid_response(self):
        """Test valid chat response"""
        response = ChatResponse(
            answer="SMA is a genetic disorder...",
            confidence=0.95
        )
        
        assert response.answer == "SMA is a genetic disorder..."
        assert response.confidence == 0.95
        assert response.confidence_level == "very_high"
    
    def test_confidence_level_assignment(self):
        """Test automatic confidence level assignment"""
        test_cases = [
            (0.95, "very_high"),
            (0.8, "high"),
            (0.6, "medium"),
            (0.4, "low"),
            (0.2, "very_low")
        ]
        
        for confidence, expected_level in test_cases:
            response = ChatResponse(
                answer="Test answer",
                confidence=confidence
            )
            assert response.confidence_level == expected_level
    
    def test_confidence_bounds(self):
        """Test confidence score bounds"""
        # Valid bounds
        ChatResponse(answer="Test", confidence=0.0)
        ChatResponse(answer="Test", confidence=1.0)
        
        # Invalid bounds
        with pytest.raises(ValidationError):
            ChatResponse(answer="Test", confidence=-0.1)
        
        with pytest.raises(ValidationError):
            ChatResponse(answer="Test", confidence=1.1)
```

### Integration Tests

```python
# tests/test_api.py
import pytest
from httpx import AsyncClient

class TestChatEndpoint:
    """Test chat API endpoint"""
    
    @pytest.mark.asyncio
    async def test_successful_chat(self, async_client: AsyncClient, mock_ai_client):
        """Test successful chat interaction"""
        response = await async_client.post("/api/chat", json={
            "message": "What is Spinal Muscular Atrophy?"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "confidence" in data
        assert "timestamp" in data
        assert 0 <= data["confidence"] <= 1
    
    @pytest.mark.asyncio
    async def test_empty_message_error(self, async_client: AsyncClient):
        """Test empty message validation"""
        response = await async_client.post("/api/chat", json={
            "message": ""
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "empty" in data["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_non_sma_message_filter(self, async_client: AsyncClient):
        """Test content filtering for non-SMA messages"""
        response = await async_client.post("/api/chat", json={
            "message": "What is the weather today?"
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "SMA" in data["detail"]
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, async_client: AsyncClient):
        """Test rate limiting functionality"""
        # This test would require implementing rate limiting
        # and might need to be marked as slow/integration test
        pass

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, async_client: AsyncClient, mock_ai_client):
        """Test successful health check"""
        response = await async_client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
        assert "dependencies" in data
    
    @pytest.mark.asyncio
    async def test_health_check_with_ai_failure(self, async_client: AsyncClient, monkeypatch):
        """Test health check when AI service is down"""
        # Mock failing AI client
        class FailingAIClient:
            async def check_health(self):
                return False
        
        monkeypatch.setattr("api.main.ai_client", FailingAIClient())
        
        response = await async_client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] in ["degraded", "unhealthy"]
```

This comprehensive backend guide provides detailed information about FastAPI development, LangChain integration, data validation, error handling, and testing strategies for the SMA Medical Assistant project.
