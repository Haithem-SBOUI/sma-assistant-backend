# 📋 Onboarding Checklist for New Developers

Welcome to the SMA Medical Assistant project! This checklist will guide you through your first week and ensure you have everything set up correctly.

## 🎯 Pre-Onboarding (Before Your First Day)

### Account Setup
- [ ] GitHub account created
- [ ] Added to project repository with appropriate permissions
- [ ] Google Cloud account setup (for AI API access)
- [ ] Team communication channels (Slack, Teams, etc.)

### Software Installation
- [ ] **Git** installed and configured
  ```bash
  git --version
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

- [ ] **Python 3.11+** installed
  ```bash
  python --version  # Should show 3.11 or higher
  ```

- [ ] **Node.js 18+** and npm installed
  ```bash
  node --version   # Should show 18 or higher
  npm --version    # Should show 9 or higher
  ```

- [ ] **VS Code** (recommended IDE) with extensions:
  - [ ] Python extension
  - [ ] Angular Language Service
  - [ ] TypeScript and JavaScript Language Features
  - [ ] GitLens
  - [ ] Prettier - Code formatter
  - [ ] ES7+ React/Redux/React-Native snippets

## 🚀 Day 1: Project Setup

### Repository Setup
- [ ] Clone the repository
  ```bash
  git clone [repository-url]
  cd sma-assistant
  ```

- [ ] Create and activate Python virtual environment
  ```bash
  python -m venv venv
  # On Windows:
  venv\Scripts\activate
  # On macOS/Linux:
  source venv/bin/activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Install frontend dependencies
  ```bash
  cd frontend/sma-assistant
  npm install
  cd ../..
  ```

### Environment Configuration
- [ ] Copy `.env.example` to `.env`
  ```bash
  cp .env.example .env
  ```

- [ ] Get Google API key from team lead
- [ ] Add API key to `.env` file
  ```
  GOOGLE_API_KEY=your_actual_api_key_here
  ```

### First Run Test
- [ ] Start the backend server
  ```bash
  # From project root
  python -m uvicorn api.main:app --reload
  ```

- [ ] Verify backend is running by visiting `http://localhost:8000/docs`

- [ ] Start the frontend (in a new terminal)
  ```bash
  cd frontend/sma-assistant
  npm start
  ```

- [ ] Verify frontend is running by visiting `http://localhost:4200`

- [ ] Test the chat functionality by sending a simple message

### Documentation Review
- [ ] Read `README.md` for project overview
- [ ] Review `NEWCOMER_GUIDE.md` for technology explanations
- [ ] Skim through `DEVELOPER_GUIDE.md` for comprehensive information

## 📚 Day 2: Understanding the Codebase

### Backend Exploration
- [ ] Open and understand `api/main.py`
  - [ ] Identify the main FastAPI app creation
  - [ ] Find the CORS middleware setup
  - [ ] Locate the `/api/chat` endpoint

- [ ] Review `chat_schema.py`
  - [ ] Understand `ChatRequest` and `ChatResponse` models
  - [ ] See how Pydantic validation works

- [ ] Examine `gemma_client.py`
  - [ ] Understand how LangChain connects to Google Gemini
  - [ ] See the retry logic and error handling

- [ ] Look at `system_prompt.txt`
  - [ ] Understand how we constrain AI responses to SMA topics

### Frontend Exploration
- [ ] Open `src/app/components/chat.component.ts`
  - [ ] Understand the component structure
  - [ ] Find the `sendMessage()` method
  - [ ] See how messages are stored and displayed

- [ ] Review `src/app/services/sma-api.service.ts`
  - [ ] Understand how HTTP requests are made
  - [ ] See error handling implementation

- [ ] Examine `src/app/components/chat.component.html`
  - [ ] Understand Angular template syntax
  - [ ] See how PrimeNG components are used

### Run Tests
- [ ] Run backend tests
  ```bash
  pytest
  ```

- [ ] Run frontend tests
  ```bash
  cd frontend/sma-assistant
  npm test
  ```

- [ ] Understand test structure and what's being tested

## 🔧 Day 3: Making Your First Changes

### Small Backend Change
- [ ] Add a new endpoint in `api/main.py`:
  ```python
  @app.get("/api/status")
  async def get_status():
      return {"status": "running", "developer": "Your Name"}
  ```

- [ ] Test the endpoint at `http://localhost:8000/api/status`

- [ ] Write a test for your new endpoint in `test_api.py`

### Small Frontend Change
- [ ] Modify the welcome message in `chat.component.html`
- [ ] Add your name or a personal touch to the interface
- [ ] Ensure the change appears in the browser

### Git Workflow Practice
- [ ] Create a new branch for your changes
  ```bash
  git checkout -b feature/onboarding-changes
  ```

- [ ] Commit your changes
  ```bash
  git add .
  git commit -m "feat: add personal touches for onboarding"
  ```

- [ ] Push the branch (don't merge yet - this is just practice)
  ```bash
  git push origin feature/onboarding-changes
  ```

## 🧪 Day 4: Testing and Quality

### Understanding Testing
- [ ] Run individual test files:
  ```bash
  pytest test_schemas.py -v
  pytest test_api.py -v
  pytest test_utils.py -v
  ```

- [ ] Understand what each test is checking

### Code Quality Tools
- [ ] Run Python linting:
  ```bash
  flake8 .
  ```

- [ ] Run type checking:
  ```bash
  mypy .
  ```

- [ ] Format code:
  ```bash
  black .
  ```

### Frontend Testing
- [ ] Run Angular tests in watch mode:
  ```bash
  cd frontend/sma-assistant
  npm test
  ```

- [ ] Understand component testing basics

### Write Your First Test
- [ ] Add a simple test to the backend
- [ ] Add a simple test to the frontend
- [ ] Ensure all tests pass

## 🏗️ Day 5: Advanced Understanding

### Architecture Deep Dive
- [ ] Draw a diagram of how data flows through the application
- [ ] Understand the request/response cycle
- [ ] Map out the file dependencies

### Error Handling
- [ ] Trigger a backend error and see how it's handled
- [ ] Trigger a frontend error and see the user experience
- [ ] Understand the logging system

### Performance Monitoring
- [ ] Use browser dev tools to monitor network requests
- [ ] Check response times for API calls
- [ ] Understand async/await patterns

### Documentation Updates
- [ ] Find something in the documentation that could be clearer
- [ ] Suggest an improvement or make a small update
- [ ] Practice the documentation contribution workflow

## 📋 End of Week 1: Review and Assessment

### Self-Assessment
Rate your understanding (1-5 scale):

- [ ] Project structure and organization: ___/5
- [ ] Python/FastAPI backend concepts: ___/5
- [ ] Angular/TypeScript frontend concepts: ___/5
- [ ] How frontend and backend communicate: ___/5
- [ ] Testing practices: ___/5
- [ ] Git workflow: ___/5
- [ ] Development environment: ___/5

### Knowledge Check
Can you explain:

- [ ] How a user message gets from the frontend to the AI and back?
- [ ] What happens when validation fails in Pydantic?
- [ ] How Angular components communicate with services?
- [ ] Why we use CORS and how it's configured?
- [ ] The difference between development and production builds?

### Practical Skills
Can you:

- [ ] Add a new API endpoint with proper validation?
- [ ] Create a new Angular component?
- [ ] Write and run tests for both frontend and backend?
- [ ] Debug common errors using browser/terminal tools?
- [ ] Use Git to create branches, commit, and push changes?

## 🎯 Week 2 Goals

### Learning Objectives
- [ ] Implement a small feature end-to-end
- [ ] Contribute to team code reviews
- [ ] Write comprehensive tests for new features
- [ ] Understand deployment process

### Suggested First Feature
Pick one to implement:

- [ ] **Message History**: Save and display previous conversations
- [ ] **Typing Indicator**: Show when AI is "thinking"
- [ ] **Message Timestamps**: Add time display to messages
- [ ] **Input Validation**: Add client-side message validation
- [ ] **Confidence Visualization**: Display confidence as progress bar

### Team Integration
- [ ] Attend team meetings and understand contribution workflow
- [ ] Start participating in code reviews
- [ ] Ask questions about architectural decisions
- [ ] Suggest improvements based on fresh perspective

## 🆘 Getting Help

### When to Ask for Help
- After 30 minutes of being stuck on a setup issue
- After 1 hour of debugging the same problem
- When error messages don't make sense
- When you need clarification on project requirements

### How to Ask for Help
1. **Describe what you're trying to do**
2. **Share the exact error message**
3. **Explain what you've already tried**
4. **Include relevant code snippets**

### Resources
- Team members and mentors
- Project documentation (this guide, DEVELOPER_GUIDE.md, etc.)
- Official documentation for technologies
- Stack Overflow (search before asking)

## 📝 Notes Section

Use this space to jot down:
- Important insights you discover
- Common error solutions
- Personal reminders
- Questions to ask in team meetings

---

## ✅ Completion Sign-off

Once you've completed Week 1:

- [ ] I can successfully run both frontend and backend
- [ ] I understand the basic project structure
- [ ] I can make small changes to both codebases
- [ ] I can run and write simple tests
- [ ] I'm comfortable with the Git workflow
- [ ] I know how to get help when stuck

**Your name**: ________________
**Date completed**: ________________
**Mentor/Team Lead approval**: ________________

---

**Welcome to the team! 🎉**

This checklist should give you a solid foundation. Remember, learning is a continuous process, and it's okay not to understand everything immediately. Focus on building a strong foundation, and the advanced concepts will become clearer over time.

*Have suggestions for improving this onboarding process? Please share them with the team!*
