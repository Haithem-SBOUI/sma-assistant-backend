# Frontend Development Guide

## Overview

This guide covers frontend development for the SMA Medical Assistant using Angular 19, TypeScript, and PrimeNG 19.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Angular Architecture](#angular-architecture)
3. [Component Development](#component-development)
4. [Service Development](#service-development)
5. [State Management](#state-management)
6. [Styling and UI](#styling-and-ui)
7. [Testing](#testing)
8. [Best Practices](#best-practices)

## Project Structure

```
src/
├── app/
│   ├── components/                 # UI Components
│   │   ├── chat/
│   │   │   ├── chat.component.ts   # Chat logic
│   │   │   ├── chat.component.html # Chat template
│   │   │   └── chat.component.css  # Chat styles
│   │   └── shared/                 # Shared components
│   ├── services/                   # Business logic services
│   │   ├── sma-api.service.ts     # API communication
│   │   └── chat-state.service.ts  # State management
│   ├── models/                     # TypeScript interfaces
│   │   ├── chat.model.ts          # Chat-related types
│   │   └── api.model.ts           # API response types
│   ├── utils/                      # Utility functions
│   │   ├── validators.ts          # Input validation
│   │   └── formatters.ts          # Data formatting
│   ├── app.component.ts           # Root component
│   ├── app.config.ts              # App configuration
│   └── app.routes.ts              # Routing setup
├── assets/                         # Static assets
├── styles.css                      # Global styles
└── main.ts                         # App bootstrap
```

## Angular Architecture

### Standalone Components

Angular 19 uses standalone components by default, eliminating the need for NgModules:

```typescript
@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, ButtonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  // Component logic
}
```

### Dependency Injection

Services are provided using the new `inject()` function or constructor injection:

```typescript
// Modern approach with inject()
import { inject } from '@angular/core';

export class ChatComponent {
  private apiService = inject(SmaApiService);
  private router = inject(Router);
}

// Traditional constructor injection
export class ChatComponent {
  constructor(
    private apiService: SmaApiService,
    private router: Router
  ) {}
}
```

### Signals (Angular 19 Feature)

Use signals for reactive state management:

```typescript
import { signal, computed } from '@angular/core';

export class ChatComponent {
  // Signal for reactive state
  messages = signal<ChatMessage[]>([]);
  currentMessage = signal('');
  
  // Computed values
  messageCount = computed(() => this.messages().length);
  hasMessages = computed(() => this.messages().length > 0);
  
  // Update signals
  addMessage(message: ChatMessage) {
    this.messages.update(messages => [...messages, message]);
  }
}
```

## Component Development

### Chat Component Example

```typescript
import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';

interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  confidence?: number;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    InputTextModule
  ],
  template: `
    <div class="chat-container">
      <!-- Messages -->
      <div class="messages">
        @for (message of messages(); track message.id) {
          <div class="message" [class.user]="message.isUser">
            <div class="content">{{ message.content }}</div>
            @if (!message.isUser && message.confidence) {
              <div class="confidence">
                Confidence: {{ formatConfidence(message.confidence) }}
              </div>
            }
          </div>
        }
      </div>
      
      <!-- Input -->
      <div class="input-area">
        <input 
          pInputText
          [(ngModel)]="currentMessage"
          (keydown.enter)="sendMessage()"
          placeholder="Ask about SMA..."
          [disabled]="isLoading()">
        
        <p-button 
          label="Send"
          icon="pi pi-send"
          (onClick)="sendMessage()"
          [disabled]="!canSend()">
        </p-button>
      </div>
    </div>
  `,
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  // Signals for reactive state
  messages = signal<ChatMessage[]>([]);
  currentMessage = signal('');
  isLoading = signal(false);
  
  // Computed properties
  canSend = computed(() => 
    this.currentMessage().trim().length > 0 && !this.isLoading()
  );
  
  constructor(private apiService: SmaApiService) {}
  
  ngOnInit() {
    this.addWelcomeMessage();
  }
  
  sendMessage() {
    if (!this.canSend()) return;
    
    const message = this.currentMessage();
    this.addUserMessage(message);
    this.currentMessage.set('');
    this.isLoading.set(true);
    
    this.apiService.sendMessage(message).subscribe({
      next: (response) => this.handleResponse(response),
      error: (error) => this.handleError(error),
      complete: () => this.isLoading.set(false)
    });
  }
  
  private addUserMessage(content: string) {
    const message: ChatMessage = {
      id: this.generateId(),
      content,
      isUser: true,
      timestamp: new Date()
    };
    this.messages.update(messages => [...messages, message]);
  }
  
  private addWelcomeMessage() {
    const welcome: ChatMessage = {
      id: this.generateId(),
      content: 'Hello! I\'m here to help answer questions about Spinal Muscular Atrophy (SMA). What would you like to know?',
      isUser: false,
      timestamp: new Date(),
      confidence: 1.0
    };
    this.messages.update(messages => [...messages, welcome]);
  }
  
  private generateId(): string {
    return Date.now().toString() + Math.random().toString(36).substr(2, 9);
  }
  
  formatConfidence(confidence: number): string {
    return `${Math.round(confidence * 100)}%`;
  }
}
```

### Component Lifecycle

```typescript
export class ChatComponent implements OnInit, OnDestroy, AfterViewInit {
  ngOnInit() {
    // Component initialization
    this.loadInitialData();
  }
  
  ngAfterViewInit() {
    // View initialization complete
    this.scrollToBottom();
  }
  
  ngOnDestroy() {
    // Cleanup subscriptions
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }
}
```

## Service Development

### API Service

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, tap, retry } from 'rxjs/operators';

interface ChatRequest {
  message: string;
}

interface ChatResponse {
  answer: string;
  confidence: number;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class SmaApiService {
  private http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api';
  
  // Connection status
  private connectionStatus = new BehaviorSubject<boolean>(true);
  public connectionStatus$ = this.connectionStatus.asObservable();
  
  sendMessage(message: string): Observable<ChatResponse> {
    const request: ChatRequest = { message };
    
    return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, request)
      .pipe(
        retry(2), // Retry failed requests
        tap(() => this.connectionStatus.next(true)),
        catchError(error => this.handleError(error))
      );
  }
  
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`)
      .pipe(
        tap(() => this.connectionStatus.next(true)),
        catchError(error => {
          this.connectionStatus.next(false);
          return throwError(() => error);
        })
      );
  }
  
  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    this.connectionStatus.next(false);
    
    let errorMessage = 'An unexpected error occurred';
    
    if (error.status === 400) {
      errorMessage = error.error?.detail || 'Invalid request';
    } else if (error.status === 429) {
      errorMessage = 'Too many requests. Please wait a moment.';
    } else if (error.status === 500) {
      errorMessage = 'Server error. Please try again later.';
    } else if (error.status === 0) {
      errorMessage = 'Unable to connect to server';
    }
    
    return throwError(() => new Error(errorMessage));
  }
}
```

### State Management Service

```typescript
import { Injectable, signal, computed } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatStateService {
  // Private signals
  private _messages = signal<ChatMessage[]>([]);
  private _isLoading = signal(false);
  private _connectionStatus = signal(true);
  
  // Public read-only access
  readonly messages = this._messages.asReadonly();
  readonly isLoading = this._isLoading.asReadonly();
  readonly connectionStatus = this._connectionStatus.asReadonly();
  
  // Computed values
  readonly messageCount = computed(() => this._messages().length);
  readonly userMessages = computed(() => 
    this._messages().filter(m => m.isUser)
  );
  readonly assistantMessages = computed(() => 
    this._messages().filter(m => !m.isUser)
  );
  
  // Actions
  addMessage(message: ChatMessage) {
    this._messages.update(messages => [...messages, message]);
  }
  
  clearMessages() {
    this._messages.set([]);
  }
  
  setLoading(loading: boolean) {
    this._isLoading.set(loading);
  }
  
  setConnectionStatus(connected: boolean) {
    this._connectionStatus.set(connected);
  }
}
```

## State Management

### Using Signals vs Observables

**Signals** - For synchronous state:
```typescript
export class ChatComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);
  
  increment() {
    this.count.update(value => value + 1);
  }
}
```

**Observables** - For asynchronous operations:
```typescript
export class ChatComponent {
  messages$ = this.apiService.getMessages();
  
  ngOnInit() {
    this.messages$.subscribe(messages => {
      // Handle async data
    });
  }
}
```

### Form State Management

```typescript
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

export class ChatFormComponent {
  chatForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.chatForm = this.fb.group({
      message: ['', [
        Validators.required,
        Validators.minLength(1),
        Validators.maxLength(1000)
      ]]
    });
  }
  
  get message() {
    return this.chatForm.get('message');
  }
  
  onSubmit() {
    if (this.chatForm.valid) {
      const message = this.chatForm.value.message;
      this.sendMessage(message);
      this.chatForm.reset();
    }
  }
}
```

## Styling and UI

### Component Styles

```css
/* chat.component.css */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.message {
  display: flex;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-in;
}

.message.user {
  justify-content: flex-end;
}

.message.user .content {
  background-color: var(--primary-color);
  color: white;
  margin-left: 2rem;
}

.message:not(.user) .content {
  background-color: var(--surface-color);
  color: var(--text-primary);
  margin-right: 2rem;
}

.content {
  padding: 0.75rem 1rem;
  border-radius: 18px;
  max-width: 70%;
  word-wrap: break-word;
}

.confidence {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.input-area input {
  flex: 1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .chat-container {
    height: 100dvh; /* Use dynamic viewport height */
    padding: 0.5rem;
  }
  
  .content {
    max-width: 85%;
  }
  
  .input-area {
    flex-direction: column;
    align-items: stretch;
  }
}
```

### Global Styles

```css
/* styles.css */
:root {
  /* Color Variables */
  --primary-color: #3b82f6;
  --primary-light: #60a5fa;
  --primary-dark: #1d4ed8;
  --secondary-color: #10b981;
  --accent-color: #f59e0b;
  --error-color: #ef4444;
  --warning-color: #f97316;
  --success-color: #22c55e;
  
  /* Background Colors */
  --background-color: #f8fafc;
  --surface-color: #ffffff;
  --surface-hover: #f1f5f9;
  
  /* Text Colors */
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  
  /* Border and Shadows */
  --border-color: #e2e8f0;
  --border-radius: 8px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --background-color: #0f172a;
    --surface-color: #1e293b;
    --surface-hover: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --border-color: #334155;
  }
}

/* Global styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--background-color);
  color: var(--text-primary);
  line-height: 1.6;
}

/* Utility classes */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-2 {
  gap: var(--spacing-sm);
}

.p-2 {
  padding: var(--spacing-sm);
}

.m-2 {
  margin: var(--spacing-sm);
}

.rounded {
  border-radius: var(--border-radius);
}

.shadow {
  box-shadow: var(--shadow-md);
}
```

### PrimeNG Theming

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    // ... other providers
    providePrimeNG({
      theme: 'none', // Use custom theme
      options: {
        ripple: true,
        inputStyle: 'outlined'
      }
    })
  ]
};
```

## Testing

### Component Testing

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ChatComponent } from './chat.component';
import { SmaApiService } from '../services/sma-api.service';
import { of } from 'rxjs';

describe('ChatComponent', () => {
  let component: ChatComponent;
  let fixture: ComponentFixture<ChatComponent>;
  let apiService: jasmine.SpyObj<SmaApiService>;

  beforeEach(async () => {
    const apiServiceSpy = jasmine.createSpyObj('SmaApiService', ['sendMessage']);

    await TestBed.configureTestingModule({
      imports: [ChatComponent, HttpClientTestingModule],
      providers: [
        { provide: SmaApiService, useValue: apiServiceSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ChatComponent);
    component = fixture.componentInstance;
    apiService = TestBed.inject(SmaApiService) as jasmine.SpyObj<SmaApiService>;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send message when form is submitted', () => {
    const mockResponse = {
      answer: 'Test response',
      confidence: 0.9,
      timestamp: new Date().toISOString()
    };
    
    apiService.sendMessage.and.returnValue(of(mockResponse));
    
    component.currentMessage.set('Test message');
    component.sendMessage();
    
    expect(apiService.sendMessage).toHaveBeenCalledWith('Test message');
    expect(component.messages().length).toBe(3); // Welcome + user + AI
  });

  it('should disable send button when message is empty', () => {
    component.currentMessage.set('');
    expect(component.canSend()).toBeFalse();
    
    component.currentMessage.set('Test message');
    expect(component.canSend()).toBeTrue();
  });
});
```

### Service Testing

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SmaApiService } from './sma-api.service';

describe('SmaApiService', () => {
  let service: SmaApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(SmaApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should send chat message', () => {
    const mockResponse = {
      answer: 'Test response',
      confidence: 0.9,
      timestamp: '2025-07-01T12:00:00Z'
    };

    service.sendMessage('Test message').subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne('http://localhost:8000/api/chat');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ message: 'Test message' });
    req.flush(mockResponse);
  });

  it('should handle error responses', () => {
    service.sendMessage('Test message').subscribe({
      next: () => fail('Should have failed'),
      error: (error) => {
        expect(error.message).toContain('Server error');
      }
    });

    const req = httpMock.expectOne('http://localhost:8000/api/chat');
    req.flush('Error', { status: 500, statusText: 'Internal Server Error' });
  });
});
```

## Best Practices

### Code Organization

1. **Single Responsibility** - Each component/service has one clear purpose
2. **Separation of Concerns** - Logic, presentation, and data are separated
3. **Consistent Naming** - Use clear, descriptive names
4. **Type Safety** - Use TypeScript interfaces and types

### Performance

1. **OnPush Change Detection**:
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ChatComponent {}
```

2. **Track By Functions**:
```typescript
trackByMessageId(index: number, message: ChatMessage): string {
  return message.id;
}
```

3. **Lazy Loading**:
```typescript
const routes: Routes = [
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.component').then(m => m.AdminComponent)
  }
];
```

### Error Handling

```typescript
export class ChatComponent {
  private handleError(error: Error) {
    console.error('Chat error:', error);
    
    // Show user-friendly message
    this.messageService.add({
      severity: 'error',
      summary: 'Error',
      detail: this.getErrorMessage(error)
    });
  }
  
  private getErrorMessage(error: Error): string {
    if (error.message.includes('network')) {
      return 'Please check your internet connection';
    }
    if (error.message.includes('rate limit')) {
      return 'Please wait a moment before sending another message';
    }
    return 'Something went wrong. Please try again.';
  }
}
```

### Accessibility

```html
<!-- Use semantic HTML -->
<main role="main" aria-label="Chat interface">
  <section aria-label="Chat messages">
    <div *ngFor="let message of messages()" 
         role="log" 
         [attr.aria-label]="getAriaLabel(message)">
      {{ message.content }}
    </div>
  </section>
  
  <form (ngSubmit)="sendMessage()" aria-label="Send message">
    <input 
      type="text"
      [(ngModel)]="currentMessage"
      aria-label="Type your message"
      [attr.aria-describedby]="'message-help'">
    
    <div id="message-help" class="sr-only">
      Ask questions about Spinal Muscular Atrophy
    </div>
    
    <button type="submit" 
            [disabled]="!canSend()"
            aria-label="Send message">
      Send
    </button>
  </form>
</main>
```

This comprehensive frontend guide should help new developers understand and contribute to the Angular application effectively.
