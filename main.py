#!/usr/bin/env python3
"""
SMA Medical Assistant - Entry Point

A production-ready medical Q&A chatbot for Spinal Muscular Atrophy (SMA) disease.
Built with FastAPI, LangChain, and Google Gemma.
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print("🏥 Starting SMA Medical Assistant API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Health: http://{host}:{port}/api/health")
    print()
    
    # Check for Google API key
    if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your_google_api_key_here":
        print("⚠️  WARNING: GOOGLE_API_KEY not set or using placeholder value!")
        print("   Please edit .env file and add your Google API key")
        print("   Get one at: https://makersuite.google.com/app/apikey")
        print()
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=log_level
    )
