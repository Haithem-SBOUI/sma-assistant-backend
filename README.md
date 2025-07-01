# SMA Medical Assistant API

A production-ready medical Q&A chatbot specifically designed for Spinal Muscular Atrophy (SMA) disease, built with FastAPI, LangChain, and Google Gemma.

## Features

- 🏥 **SMA-Specialized**: Focused exclusively on Spinal Muscular Atrophy information
- 🤖 **AI-Powered**: Uses Google Gemma via LangChain for accurate responses
- 🔒 **Validated Responses**: Pydantic validation with confidence scoring
- 🚀 **Production-Ready**: Full error handling, logging, and fallback responses
- 🧪 **Well-Tested**: Comprehensive unit and integration tests
- 📊 **Structured Output**: JSON responses with confidence levels

## Quick Start

### 1. Environment Setup

```bash
# Clone or create the project directory
cd sma-assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:

```env
GOOGLE_API_KEY=your_actual_google_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:4200
LOG_LEVEL=INFO
```

**Getting a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Run the API

```bash
# Start the development server
python -m api.main

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Test the API

#### Health Check
```bash
curl http://localhost:8000/api/health
```

#### Chat with the SMA Assistant
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the main types of SMA?"}'
```

Expected response:
```json
{
  "answer": "There are several types of SMA classified by age of onset and severity...",
  "confidence": 0.92,
  "timestamp": "2025-07-01T10:30:00.123456"
}
```

## API Endpoints

### POST `/api/chat`
Main chat endpoint for SMA-related questions.

**Request:**
```json
{
  "message": "What is SMA?"
}
```

**Response:**
```json
{
  "answer": "Detailed SMA information...",
  "confidence": 0.95,
  "timestamp": "2025-07-01T10:30:00.123456"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-07-01T10:30:00.123456"
}
```

## Testing

Run the test suite:

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test files
pytest test_schemas.py
pytest test_utils.py  
pytest test_api.py
```

## Architecture

### Core Components

1. **`chat_schema.py`**: Pydantic models for request/response validation
2. **`gemma_client.py`**: LangChain client with retry logic and error handling
3. **`utils/llm.py`**: JSON extraction and response validation utilities
4. **`simple_workflow.py`**: Simplified workflow without LangGraph complexity
5. **`api/main.py`**: FastAPI application with endpoints and middleware

### Response Flow

1. **Request Validation**: Pydantic validates incoming chat requests
2. **LLM Processing**: Gemma generates SMA-specific responses
3. **JSON Extraction**: Utils parse structured responses from raw text
4. **Validation**: Response validated against schema with confidence scoring
5. **Fallback Handling**: Robust error handling with meaningful fallback responses

### Confidence Scoring

- **0.9-1.0**: Well-established medical facts
- **0.7-0.9**: Generally accepted information
- **0.5-0.7**: Emerging research or less certain
- **0.3-0.5**: Limited evidence
- **0.0-0.3**: Highly uncertain or error fallback

## Development

### Project Structure

```
sma-assistant/
├── api/
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── graph/
│   ├── __init__.py
│   └── chat_flow.py      # LangGraph workflow (advanced)
├── utils/
│   ├── __init__.py
│   └── llm.py           # LLM response utilities
├── chat_schema.py        # Pydantic models
├── gemma_client.py       # LangChain Gemma client
├── simple_workflow.py   # Simple workflow for MVP
├── system_prompt.txt     # System prompt for SMA specialization
├── test_*.py            # Test files
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

### Adding Features

1. **New Validation**: Add to `chat_schema.py`
2. **LLM Improvements**: Modify `gemma_client.py` or `system_prompt.txt`
3. **Response Processing**: Update `utils/llm.py`
4. **API Endpoints**: Add to `api/main.py`
5. **Tests**: Create corresponding test files

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google API key for Gemma access | Required |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:4200` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Production Deployment

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Security Considerations

1. **API Key Security**: Store Google API key securely (environment variables, secrets management)
2. **CORS Configuration**: Limit CORS origins to trusted domains
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Input Validation**: All inputs are validated via Pydantic
5. **Error Handling**: No sensitive information exposed in error responses

## Troubleshooting

### Common Issues

1. **"Import could not be resolved"**: Install dependencies with `pip install -r requirements.txt`
2. **"GOOGLE_API_KEY not found"**: Set the environment variable in `.env`
3. **"Connection timeout"**: Check internet connection and API key validity
4. **"Invalid JSON response"**: LLM response parsing failed, fallback response returned

### Logs

Check logs for detailed error information:
- API errors logged with full context
- LLM request/response logging
- Validation errors with specific field information

## License

This project is for educational and medical assistance purposes. Always consult healthcare professionals for medical advice.

## Support

For issues related to:
- **SMA Information**: Consult healthcare professionals
- **API Technical Issues**: Check logs and troubleshooting section
- **Development**: Review test files for examples
