# SMA Medical Assistant - Developer Guide

Welcome to the SMA Medical Assistant project! This comprehensive guide will help new developers and interns understand the project structure, technologies, and how to contribute effectively.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Development Environment Setup](#development-environment-setup)
5. [Project Structure](#project-structure)
6. [Backend Development](#backend-development)
7. [Frontend Development](#frontend-development)
8. [API Documentation](#api-documentation)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing Guidelines](#contributing-guidelines)
12. [Troubleshooting](#troubleshooting)
13. [Learning Resources](#learning-resources)

## Project Overview

### What is SMA Medical Assistant?

The SMA Medical Assistant is a specialized AI-powered chatbot designed to provide accurate information about Spinal Muscular Atrophy (SMA). It combines modern web technologies with advanced language models to deliver reliable medical information.

### Key Features

- 🏥 **SMA-Specialized**: Focused exclusively on Spinal Muscular Atrophy information
- 🤖 **AI-Powered**: Uses Google Gemini via LangChain for accurate responses
- 🔒 **Validated Responses**: Pydantic validation with confidence scoring
- 🚀 **Production-Ready**: Full error handling, logging, and fallback responses
- 🧪 **Well-Tested**: Comprehensive unit and integration tests
- 📊 **Structured Output**: JSON responses with confidence levels
- 📱 **Modern UI**: Responsive Angular interface with PrimeNG components

### Target Users

- Patients with SMA
- Caregivers and family members
- Healthcare professionals
- Medical students and researchers

## Technology Stack

### Backend Technologies

| Technology | Purpose | Why We Use It |
|------------|---------|---------------|
| **Python 3.11+** | Programming language | Industry standard for AI/ML applications |
| **FastAPI** | Web framework | Fast, modern, auto-documented APIs |
| **LangChain** | LLM orchestration | Simplifies AI model integration |
| **Google Gemini** | Language model | High-quality, cost-effective AI responses |
| **Pydantic** | Data validation | Type-safe data structures |
| **pytest** | Testing framework | Comprehensive testing capabilities |
| **uvicorn** | ASGI server | High-performance async server |

### Frontend Technologies

| Technology | Purpose | Why We Use It |
|------------|---------|---------------|
| **Angular 19** | Frontend framework | Modern, TypeScript-based framework |
| **TypeScript** | Programming language | Type safety and better development experience |
| **PrimeNG 19** | UI component library | Professional, accessible components |
| **RxJS** | Reactive programming | Handle async operations and data streams |
| **CSS3** | Styling | Custom styling and responsive design |

### Development Tools

- **Git** - Version control
- **VS Code** - Recommended IDE
- **Node.js** - JavaScript runtime for frontend
- **npm** - Package manager
- **Python venv** - Virtual environment management

## Project Architecture

### High-Level Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Angular 19    │ ←──────────────→ │    FastAPI      │
│   Frontend      │                 │    Backend      │
│                 │                 │                 │
│ • Chat UI       │                 │ • API Endpoints │
│ • PrimeNG       │                 │ • Validation    │
│ • TypeScript    │                 │ • LangChain     │
└─────────────────┘                 └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  Google Gemini  │
                                    │   AI Model      │
                                    └─────────────────┘
```

### Backend Architecture

```
api/
├── main.py              # FastAPI application entry point
├── __init__.py
chat_schema.py           # Pydantic models for data validation
gemma_client.py          # Google Gemini client wrapper
simple_workflow.py       # Business logic workflow
system_prompt.txt        # AI system instructions
utils/
├── llm.py              # LLM utility functions
└── __init__.py
```

### Frontend Architecture

```
src/
├── app/
│   ├── components/
│   │   ├── chat.component.ts     # Main chat interface
│   │   ├── chat.component.html   # Chat template
│   │   └── chat.component.css    # Chat styles
│   ├── services/
│   │   └── sma-api.service.ts    # API communication service
│   ├── app.component.ts          # Root component
│   ├── app.config.ts             # App configuration
│   └── app.routes.ts             # Routing configuration
├── styles.css                    # Global styles
└── main.ts                       # Application bootstrap
```

## Development Environment Setup

### Prerequisites

Before you start, ensure you have the following installed:

1. **Python 3.11 or higher**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Node.js 18 or higher**
   ```bash
   node --version    # Should be 18+
   npm --version     # Should be 9+
   ```

3. **Git**
   ```bash
   git --version
   ```

### Initial Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd sma-assistant
```

#### 2. Backend Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file with your configuration
# Add your Google API key and other settings
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend/sma-assistant

# Install Node.js dependencies
npm install

# Return to project root
cd ../..
```

#### 4. Environment Configuration

Edit the `.env` file with your configuration:

```env
# Google AI API Key (required)
GOOGLE_API_KEY=your_actual_google_api_key_here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Configuration
CORS_ORIGINS=http://localhost:4200

# Logging
LOG_LEVEL=INFO
```

**Getting a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### Running the Application

#### Start Backend Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the FastAPI server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### Start Frontend Server

```bash
# In a new terminal, navigate to frontend
cd frontend/sma-assistant

# Start Angular development server
npm start
```

The frontend will be available at `http://localhost:4200`

## Project Structure

### Backend Structure Explained

```
sma-assistant/
├── api/                    # API layer
│   ├── __init__.py
│   └── main.py            # FastAPI app, routes, middleware
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── llm.py            # LLM processing utilities
├── tests/                 # Test files
│   ├── test_api.py       # API endpoint tests
│   ├── test_schemas.py   # Data validation tests
│   └── test_utils.py     # Utility function tests
├── chat_schema.py        # Pydantic data models
├── gemma_client.py       # Google Gemini client
├── simple_workflow.py    # Business logic
├── system_prompt.txt     # AI system instructions
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # Project documentation
```

### Frontend Structure Explained

```
frontend/sma-assistant/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── chat.component.ts      # Chat logic and state
│   │   │   ├── chat.component.html    # Chat template/UI
│   │   │   └── chat.component.css     # Chat component styles
│   │   ├── services/
│   │   │   └── sma-api.service.ts     # HTTP client for API
│   │   ├── app.component.ts           # Root component
│   │   ├── app.component.html         # Root template
│   │   ├── app.config.ts              # App configuration
│   │   └── app.routes.ts              # Routing setup
│   ├── styles.css                     # Global styles
│   ├── main.ts                        # App bootstrap
│   └── index.html                     # HTML entry point
├── package.json                       # Node.js dependencies
├── angular.json                       # Angular configuration
├── tsconfig.json                      # TypeScript configuration
└── README.md
```

## Backend Development

### Understanding the Backend Flow

1. **Request Flow:**
   ```
   Client Request → FastAPI → Validation → Workflow → LLM → Response
   ```

2. **Key Components:**

#### FastAPI Application (`api/main.py`)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SMA Medical Assistant API",
    description="AI-powered medical Q&A for Spinal Muscular Atrophy",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Data Models (`chat_schema.py`)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat messages"""
    message: str = Field(..., min_length=1, max_length=1000)
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ChatResponse(BaseModel):
    """Response model for chat responses"""
    answer: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    sources: Optional[list] = None
```

#### LLM Client (`gemma_client.py`)

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

class GemmaClient:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.1
        )
    
    def generate_response(self, message: str, system_prompt: str) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=message)
        ]
        response = self.llm.invoke(messages)
        return response.content
```

### Adding New API Endpoints

1. **Define the endpoint in `api/main.py`:**

```python
@app.post("/api/new-endpoint")
async def new_endpoint(request: NewRequestModel):
    try:
        # Your logic here
        result = process_request(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

2. **Create request/response models in `chat_schema.py`:**

```python
class NewRequestModel(BaseModel):
    field1: str
    field2: Optional[int] = None
```

3. **Add tests in `tests/test_api.py`:**

```python
def test_new_endpoint():
    response = client.post("/api/new-endpoint", json={
        "field1": "test_value"
    })
    assert response.status_code == 200
```

### Error Handling Best Practices

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Validate input
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Process request
        response = workflow.process_message(request.message)
        
        return ChatResponse(
            answer=response.answer,
            confidence=response.confidence,
            timestamp=datetime.now()
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Frontend Development

### Understanding Angular Concepts

#### Components

Components are the building blocks of Angular applications. Each component has:

- **TypeScript Class** (`*.component.ts`) - Logic and data
- **HTML Template** (`*.component.html`) - UI structure
- **CSS Styles** (`*.component.css`) - Component-specific styles

#### Services

Services handle data and business logic that can be shared across components:

```typescript
@Injectable({
  providedIn: 'root'
})
export class SmaApiService {
  private apiUrl = 'http://localhost:8000/api';
  
  constructor(private http: HttpClient) {}
  
  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, { message });
  }
}
```

#### Dependency Injection

Angular's dependency injection system provides services to components:

```typescript
export class ChatComponent {
  constructor(
    private smaApiService: SmaApiService,
    private messageService: MessageService
  ) {}
}
```

### Understanding the Chat Component

#### Component Structure

```typescript
export class ChatComponent implements OnInit, OnDestroy {
  // State management
  messages: ChatMessage[] = [];
  currentMessage = '';
  isLoading = false;
  isConnected = false;
  
  // Lifecycle hooks
  ngOnInit(): void {
    this.initializeChat();
  }
  
  ngOnDestroy(): void {
    // Cleanup subscriptions
  }
  
  // User interactions
  sendMessage(): void {
    // Handle message sending
  }
}
```

#### Template Binding

```html
<!-- Property binding -->
<input [(ngModel)]="currentMessage" [disabled]="isLoading">

<!-- Event binding -->
<button (click)="sendMessage()" [disabled]="!currentMessage.trim()">

<!-- Conditional rendering -->
<div *ngIf="isLoading">Loading...</div>

<!-- List rendering -->
<div *ngFor="let message of messages; trackBy: trackByMessageId">
  {{ message.content }}
</div>
```

### Adding New Frontend Features

#### 1. Create a New Component

```bash
ng generate component components/new-feature
```

#### 2. Define the Component

```typescript
@Component({
  selector: 'app-new-feature',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './new-feature.component.html',
  styleUrls: ['./new-feature.component.css']
})
export class NewFeatureComponent {
  // Component logic
}
```

#### 3. Add to Parent Component

```typescript
// In parent component
import { NewFeatureComponent } from './new-feature/new-feature.component';

@Component({
  imports: [NewFeatureComponent, /* other imports */],
  // ...
})
```

#### 4. Use in Template

```html
<app-new-feature></app-new-feature>
```

### State Management

#### Component State

```typescript
export class ChatComponent {
  // Local state
  private messages: ChatMessage[] = [];
  private isLoading = false;
  
  // Getters for templates
  get messageCount(): number {
    return this.messages.length;
  }
  
  // State updates
  addMessage(message: ChatMessage): void {
    this.messages.push(message);
  }
}
```

#### Service State (Shared State)

```typescript
@Injectable({
  providedIn: 'root'
})
export class ChatStateService {
  private messagesSubject = new BehaviorSubject<ChatMessage[]>([]);
  public messages$ = this.messagesSubject.asObservable();
  
  addMessage(message: ChatMessage): void {
    const currentMessages = this.messagesSubject.value;
    this.messagesSubject.next([...currentMessages, message]);
  }
}
```

### Working with PrimeNG

#### Installing PrimeNG Components

PrimeNG components are modular. Import only what you need:

```typescript
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CardModule } from 'primeng/card';

@Component({
  imports: [ButtonModule, InputTextModule, CardModule],
  // ...
})
```

#### Using PrimeNG Components

```html
<!-- Button -->
<p-button 
  label="Send" 
  icon="pi pi-send" 
  (onClick)="sendMessage()"
  [disabled]="isLoading">
</p-button>

<!-- Input -->
<input 
  pInputText 
  [(ngModel)]="currentMessage" 
  placeholder="Type your message...">

<!-- Card -->
<p-card header="Chat Messages">
  <div *ngFor="let message of messages">
    {{ message.content }}
  </div>
</p-card>
```

## API Documentation

### Endpoints

#### POST `/api/chat`

Send a chat message and receive an AI response.

**Request:**
```json
{
  "message": "What is SMA?"
}
```

**Response:**
```json
{
  "answer": "Spinal Muscular Atrophy (SMA) is a genetic disorder...",
  "confidence": 0.95,
  "timestamp": "2025-07-01T12:00:00Z"
}
```

**Error Responses:**
- `400` - Invalid request (empty message, too long, etc.)
- `500` - Server error

#### GET `/api/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-07-01T12:00:00Z"
}
```

### Request/Response Models

#### ChatRequest
```typescript
interface ChatRequest {
  message: string;  // 1-1000 characters, required
}
```

#### ChatResponse
```typescript
interface ChatResponse {
  answer: string;           // AI response
  confidence: number;       // 0.0-1.0
  timestamp: string;        // ISO datetime
  sources?: string[];       // Optional source references
}
```

### Error Handling

All endpoints return errors in this format:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Testing

### Backend Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

#### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_chat_endpoint():
    """Test the chat endpoint with valid input"""
    response = client.post("/api/chat", json={
        "message": "What is SMA?"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1

def test_chat_endpoint_empty_message():
    """Test the chat endpoint with empty message"""
    response = client.post("/api/chat", json={
        "message": ""
    })
    
    assert response.status_code == 400
```

#### Test Categories

1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test API endpoints
3. **Schema Tests** - Test data validation

### Frontend Testing

#### Running Tests

```bash
# Navigate to frontend directory
cd frontend/sma-assistant

# Run unit tests
npm test

# Run e2e tests
npm run e2e
```

#### Writing Component Tests

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatComponent } from './chat.component';

describe('ChatComponent', () => {
  let component: ChatComponent;
  let fixture: ComponentFixture<ChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ChatComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send message when button clicked', () => {
    spyOn(component, 'sendMessage');
    
    const button = fixture.nativeElement.querySelector('button');
    button.click();
    
    expect(component.sendMessage).toHaveBeenCalled();
  });
});
```

## Deployment

### Development Deployment

#### Backend

```bash
# Using uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Using gunicorn (production-like)
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend

```bash
# Development server
ng serve

# Production build
ng build --configuration production

# Serve production build
npx http-server dist/sma-assistant
```

### Production Deployment

#### Docker Deployment

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/sma-assistant /usr/share/nginx/html
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
  
  frontend:
    build: ./frontend/sma-assistant
    ports:
      - "80:80"
    depends_on:
      - backend
```

## Contributing Guidelines

### Git Workflow

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

3. **Push and create pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add confidence scoring to chat responses
fix: resolve CORS issue with frontend requests
docs: update API documentation
test: add unit tests for gemma client
```

### Code Style Guidelines

#### Python (Backend)

```python
# Use type hints
def process_message(message: str) -> ChatResponse:
    pass

# Use docstrings
def validate_message(message: str) -> bool:
    """
    Validate chat message content.
    
    Args:
        message: The message to validate
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        ValueError: If message is invalid
    """
    pass

# Use meaningful variable names
user_message = request.message
ai_response = llm_client.generate_response(user_message)
```

#### TypeScript (Frontend)

```typescript
// Use interfaces for type safety
interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

// Use meaningful method names
sendMessage(): void {
  // Implementation
}

// Use observables for async operations
sendMessage(): Observable<ChatResponse> {
  return this.http.post<ChatResponse>(this.apiUrl, { message });
}
```

### Pull Request Process

1. **Create descriptive PR title**
2. **Fill out PR template**
3. **Ensure all tests pass**
4. **Request review from team members**
5. **Address review feedback**
6. **Merge after approval**

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue: Import errors**
```bash
ModuleNotFoundError: No module named 'langchain'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

**Issue: Google API key error**
```bash
google.generativeai.types.generation_types.BlockedPromptException
```

**Solution:**
- Check API key is correct in `.env`
- Ensure API key has proper permissions
- Verify billing is enabled on Google Cloud

#### Frontend Issues

**Issue: Module not found**
```bash
Cannot find module 'primeng/button'
```

**Solution:**
```bash
# Install PrimeNG
npm install primeng primeicons
```

**Issue: CORS errors**
```bash
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Ensure backend CORS is configured for `http://localhost:4200`
- Check frontend is making requests to correct backend URL

### Development Tips

1. **Use browser DevTools** - Inspect network requests, console errors
2. **Check server logs** - Backend errors are logged to console
3. **Use TypeScript strict mode** - Catch errors at compile time
4. **Test with different inputs** - Edge cases, empty strings, long messages
5. **Monitor API rate limits** - Google API has usage limits

## Learning Resources

### For New Developers

#### Python/FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

#### Angular/TypeScript
- [Angular Documentation](https://angular.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [RxJS Documentation](https://rxjs.dev/)
- [PrimeNG Documentation](https://primeng.org/)

#### LangChain/AI
- [LangChain Documentation](https://docs.langchain.com/)
- [Google AI Documentation](https://ai.google.dev/)

### Recommended Learning Path

#### Week 1: Fundamentals
1. Python basics and virtual environments
2. TypeScript and Angular basics
3. HTTP and REST APIs
4. Git workflow

#### Week 2: Project Specifics
1. FastAPI framework
2. Angular components and services
3. API integration
4. Testing basics

#### Week 3: Advanced Topics
1. LangChain and AI integration
2. Error handling and validation
3. Production deployment
4. Performance optimization

### Practice Exercises

#### Beginner
1. Add a new API endpoint that returns current time
2. Create a new Angular component that displays user statistics
3. Add input validation for minimum message length
4. Write unit tests for a utility function

#### Intermediate
1. Implement message history persistence
2. Add typing indicators during AI response
3. Create confidence level visualization
4. Add rate limiting to API endpoints

#### Advanced
1. Implement streaming responses
2. Add multi-language support
3. Create admin dashboard
4. Implement caching layer

## Support and Help

### Getting Help

1. **Check this documentation first**
2. **Search existing issues on GitHub**
3. **Ask team members or mentors**
4. **Create detailed issue reports**

### Issue Reporting Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS, Ubuntu]
- Python version: [e.g., 3.11.0]
- Node.js version: [e.g., 18.0.0]
- Browser: [e.g., Chrome 91]

## Additional Context
Any other relevant information
```

---

Welcome to the team! This documentation should help you get started. Don't hesitate to ask questions and contribute to improving this guide.

Happy coding! 🚀
