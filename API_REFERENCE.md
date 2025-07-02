# API Reference Documentation

## Overview

The SMA Medical Assistant API provides endpoints for AI-powered medical Q&A specifically focused on Spinal Muscular Atrophy (SMA).

**Base URL:** `http://localhost:8000`

**Content Type:** `application/json`

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Rate Limiting

- 100 requests per minute per IP address
- Rate limit headers are included in responses

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error description",
  "status_code": 400,
  "type": "validation_error"
}
```

## Endpoints

### Health Check

Check the API health status and version.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-07-01T12:00:00.000Z",
  "dependencies": {
    "ai_model": "available",
    "database": "connected"
  }
}
```

**Status Codes:**
- `200` - API is healthy
- `503` - API is unhealthy

### Chat Message

Send a message and receive an AI-generated response about SMA.

**Endpoint:** `POST /api/chat`

**Request Body:**
```json
{
  "message": "What is Spinal Muscular Atrophy?"
}
```

**Response:**
```json
{
  "answer": "Spinal Muscular Atrophy (SMA) is a genetic neuromuscular disorder that affects the motor neurons in the spinal cord...",
  "confidence": 0.95,
  "timestamp": "2025-07-01T12:00:00.000Z",
  "sources": [
    "Medical literature review",
    "Clinical guidelines"
  ],
  "response_time_ms": 1250
}
```

**Request Validation:**
- `message`: Required, string, 1-1000 characters
- Message must contain SMA-related content
- No empty or whitespace-only messages

**Status Codes:**
- `200` - Successful response
- `400` - Invalid request (validation errors)
- `429` - Rate limit exceeded
- `500` - Internal server error

**Error Examples:**

*Empty message:*
```json
{
  "detail": "Message cannot be empty",
  "status_code": 400,
  "type": "validation_error"
}
```

*Message too long:*
```json
{
  "detail": "Message must be 1000 characters or less",
  "status_code": 400,
  "type": "validation_error"
}
```

*Non-SMA related:*
```json
{
  "detail": "I can only provide information about Spinal Muscular Atrophy (SMA). Please ask questions related to SMA.",
  "status_code": 400,
  "type": "content_filter"
}
```

### Suggested Questions

Get a list of suggested questions for users.

**Endpoint:** `GET /api/suggestions`

**Response:**
```json
{
  "questions": [
    "What is Spinal Muscular Atrophy?",
    "What are the types of SMA?",
    "What are the symptoms of SMA?",
    "How is SMA diagnosed?",
    "What treatments are available for SMA?"
  ],
  "category": "general",
  "updated_at": "2025-07-01T12:00:00.000Z"
}
```

**Status Codes:**
- `200` - Successful response

## Response Models

### ChatResponse

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | AI-generated response about SMA |
| `confidence` | number | Confidence score (0.0-1.0) |
| `timestamp` | string | ISO 8601 timestamp |
| `sources` | array | Optional source references |
| `response_time_ms` | number | Response generation time |

### HealthResponse

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Health status ("healthy" or "unhealthy") |
| `version` | string | API version |
| `timestamp` | string | Current server time |
| `dependencies` | object | Status of external dependencies |

## SDKs and Examples

### Python Example

```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health')
print(response.json())

# Send chat message
chat_data = {"message": "What is SMA?"}
response = requests.post('http://localhost:8000/api/chat', json=chat_data)
print(response.json())
```

### JavaScript/TypeScript Example

```typescript
// Health check
const healthResponse = await fetch('http://localhost:8000/api/health');
const health = await healthResponse.json();
console.log(health);

// Send chat message
const chatResponse = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What are the symptoms of SMA?'
  })
});
const chat = await chatResponse.json();
console.log(chat);
```

### curl Examples

```bash
# Health check
curl -X GET http://localhost:8000/api/health

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is SMA?"}'
```

## Confidence Scoring

The API returns a confidence score (0.0-1.0) indicating how confident the AI is about its response:

- **0.9-1.0**: Very High Confidence - Well-established medical facts
- **0.7-0.9**: High Confidence - Generally accepted information
- **0.5-0.7**: Medium Confidence - Contextual or nuanced information
- **0.3-0.5**: Low Confidence - Uncertain or limited information
- **0.0-0.3**: Very Low Confidence - Highly uncertain response

## Content Filtering

The API implements content filtering to ensure responses are:

1. **SMA-Related**: Only responds to questions about Spinal Muscular Atrophy
2. **Medically Appropriate**: Avoids providing specific medical advice
3. **Safe**: Filters out harmful or inappropriate content
4. **Accurate**: Responses are based on current medical knowledge

## Monitoring and Logging

All API requests are logged for monitoring and improvement purposes:

- Request/response times
- Error rates
- Content filtering triggers
- Confidence score distributions

## Changelog

### Version 1.0.0 (Current)
- Initial API release
- Chat endpoint with confidence scoring
- Health check endpoint
- Content filtering for SMA-only responses
- Rate limiting implementation

## Support

For API support or questions:

1. Check this documentation
2. Review error messages and status codes
3. Contact the development team
4. Report issues through the project repository
