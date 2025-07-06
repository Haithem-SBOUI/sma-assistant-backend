import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from chat_schema import ChatRequest, ChatResponse, HealthResponse
from simple_workflow import get_chat_workflow
from utils.llm import create_fallback_response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SMA Medical Assistant API",
    description="AI-powered medical assistant for Spinal Muscular Atrophy (SMA) questions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Get workflow instance
chat_workflow = get_chat_workflow()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to ensure JSON responses"""
    logger.error(f"Unhandled exception: {exc}")
    
    fallback_response = create_fallback_response(
        "An unexpected error occurred while processing your request."
    )
    
    return JSONResponse(
        status_code=500,
        content=fallback_response.dict()
    )


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, http_request: Request):
    """
    Main chat endpoint for SMA-related questions
    
    Args:
        request: ChatRequest containing user message
        http_request: FastAPI Request object for client info
        
    Returns:
        ChatResponse with AI answer and confidence score
    """
    try:
        # Extract client information
        client_ip = http_request.client.host if http_request.client else "unknown"
        server_name = http_request.headers.get("host", "unknown")
        user_agent = http_request.headers.get("user-agent", "unknown")
        
        logger.info(f"Chat request from client IP: {client_ip}, server: {server_name}, user-agent: {user_agent[:50]}...")
        logger.info(f"Received chat request: {request.message[:100]}...")
        
        # Process the request through the workflow
        response = await chat_workflow.process_chat(request)
        
        logger.info(f"Generated response with confidence: {response.confidence} for client: {client_ip}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Return fallback response instead of raising exception
        return create_fallback_response()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SMA Medical Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "chat": "/api/chat"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
