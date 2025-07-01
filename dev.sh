#!/bin/bash

# SMA Assistant Development Commands

set -e

case "$1" in
    "start")
        echo "🚀 Starting SMA Assistant API..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
        python -m api.main
        ;;
    "test")
        echo "🧪 Running tests..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
        pytest -v
        ;;
    "test-cov")
        echo "🧪 Running tests with coverage..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
        pytest --cov=. --cov-report=html --cov-report=term
        echo "📊 Coverage report generated in htmlcov/"
        ;;
    "install")
        echo "📦 Installing dependencies..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
        pip install -r requirements.txt
        ;;
    "health")
        echo "🏥 Checking API health..."
        curl -s http://localhost:8000/api/health | python -m json.tool
        ;;
    "chat")
        if [ -z "$2" ]; then
            echo "💬 Usage: ./dev.sh chat \"Your SMA question here\""
            exit 1
        fi
        echo "💬 Asking: $2"
        curl -s -X POST "http://localhost:8000/api/chat" \
            -H "Content-Type: application/json" \
            -d "{\"message\": \"$2\"}" | python -m json.tool
        ;;
    "docs")
        echo "📖 Opening API documentation..."
        echo "Visit: http://localhost:8000/docs"
        ;;
    *)
        echo "🏥 SMA Medical Assistant - Development Commands"
        echo "=============================================="
        echo ""
        echo "Available commands:"
        echo "  start     - Start the API server"
        echo "  test      - Run tests"
        echo "  test-cov  - Run tests with coverage"
        echo "  install   - Install/update dependencies"
        echo "  health    - Check API health"
        echo "  chat      - Send a chat message to API"
        echo "  docs      - Show API documentation URL"
        echo ""
        echo "Examples:"
        echo "  ./dev.sh start"
        echo "  ./dev.sh test"
        echo "  ./dev.sh chat \"What is SMA?\""
        echo "  ./dev.sh health"
        ;;
esac
