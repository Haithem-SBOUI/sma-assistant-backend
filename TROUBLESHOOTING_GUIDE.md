# 🔧 Troubleshooting Guide for Newcomers

This guide addresses the most common issues that new developers face when working with the SMA Medical Assistant project. Each section includes symptoms, causes, and step-by-step solutions.

## 📋 Quick Diagnosis

Having an issue? Start here to quickly identify the problem:

| Symptom | Likely Issue | Quick Fix |
|---------|--------------|-----------|
| `pip: command not found` | Python not installed | Install Python 3.11+ |
| `npm: command not found` | Node.js not installed | Install Node.js 18+ |
| Backend won't start | Missing dependencies | Run `pip install -r requirements.txt` |
| Frontend won't start | Missing dependencies | Run `npm install` |
| CORS errors in browser | Backend not running | Start backend server |
| API key errors | Missing environment variables | Check `.env` file |
| Tests failing | Wrong directory | Navigate to correct folder |

## 🐍 Python/Backend Issues

### Issue: Python Command Not Found

**Symptoms:**
```bash
python: command not found
```

**Causes:**
- Python not installed
- Python not in PATH
- Using `python` instead of `python3`

**Solutions:**

1. **Check if Python is installed:**
   ```bash
   python --version
   python3 --version
   which python
   which python3
   ```

2. **Install Python (if missing):**
   - **Windows**: Download from [python.org](https://python.org) and check "Add to PATH"
   - **macOS**: `brew install python3` or download from python.org
   - **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

3. **Use the correct command:**
   - Try `python3` instead of `python`
   - Try `py` instead of `python` (Windows)

### Issue: Virtual Environment Problems

**Symptoms:**
```bash
venv: command not found
# or
'venv' is not recognized as an internal or external command
```

**Causes:**
- Virtual environment module not available
- Wrong Python version

**Solutions:**

1. **Create virtual environment:**
   ```bash
   # Try these in order:
   python -m venv venv
   python3 -m venv venv
   py -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Verify activation:**
   ```bash
   which python  # Should point to venv directory
   pip list      # Should show limited packages
   ```

### Issue: Pip Install Fails

**Symptoms:**
```bash
ERROR: Could not find a version that satisfies the requirement
pip: command not found
Permission denied when installing packages
```

**Solutions:**

1. **Ensure pip is available:**
   ```bash
   python -m pip --version
   ```

2. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Install in virtual environment:**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

4. **Handle permission issues:**
   ```bash
   # Use --user flag if not in virtual environment
   pip install --user package-name
   ```

### Issue: FastAPI Server Won't Start

**Symptoms:**
```bash
uvicorn: command not found
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'api'
```

**Solutions:**

1. **Check virtual environment:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   
   # Verify it's activated (should show venv path)
   which python
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run from correct directory:**
   ```bash
   # Make sure you're in the project root
   pwd  # Should show .../sma-assistant
   
   # Run the server
   python -m uvicorn api.main:app --reload
   ```

4. **Check for import errors:**
   ```bash
   # Test Python imports
   python -c "import fastapi; print('FastAPI OK')"
   python -c "from api.main import app; print('App import OK')"
   ```

### Issue: Google API Key Errors

**Symptoms:**
```bash
google.api_core.exceptions.Unauthenticated: 401 Request had invalid authentication credentials
KeyError: 'GOOGLE_API_KEY'
```

**Solutions:**

1. **Check .env file exists:**
   ```bash
   ls -la .env
   cat .env  # Should show GOOGLE_API_KEY=...
   ```

2. **Create .env file from example:**
   ```bash
   cp .env.example .env
   # Then edit .env and add your API key
   ```

3. **Verify API key format:**
   ```bash
   # .env file should contain:
   GOOGLE_API_KEY=AIzaSyC...your_actual_key_here
   # No quotes, no spaces around =
   ```

4. **Test API key:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GOOGLE_API_KEY')[:10] + '...')"
   ```

## 🅰️ Angular/Frontend Issues

### Issue: Node.js or npm Not Found

**Symptoms:**
```bash
node: command not found
npm: command not found
```

**Solutions:**

1. **Install Node.js:**
   - Download from [nodejs.org](https://nodejs.org) (LTS version)
   - **macOS**: `brew install node`
   - **Linux**: `sudo apt install nodejs npm`

2. **Verify installation:**
   ```bash
   node --version  # Should be 18+
   npm --version   # Should be 9+
   ```

3. **Update npm if needed:**
   ```bash
   npm install -g npm@latest
   ```

### Issue: npm install Fails

**Symptoms:**
```bash
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path .../package.json
EACCES: permission denied
```

**Solutions:**

1. **Navigate to correct directory:**
   ```bash
   cd frontend/sma-assistant
   ls package.json  # Should exist
   ```

2. **Clear npm cache:**
   ```bash
   npm cache clean --force
   ```

3. **Delete node_modules and reinstall:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Fix permissions (macOS/Linux):**
   ```bash
   sudo chown -R $(whoami) ~/.npm
   ```

### Issue: Angular CLI Not Found

**Symptoms:**
```bash
ng: command not found
'ng' is not recognized as an internal or external command
```

**Solutions:**

1. **Install Angular CLI globally:**
   ```bash
   npm install -g @angular/cli
   ```

2. **Use npx instead:**
   ```bash
   npx ng serve
   npx ng build
   ```

3. **Check PATH (if installed but not found):**
   ```bash
   # Find where npm installs global packages
   npm config get prefix
   
   # Add to PATH in ~/.bashrc or ~/.zshrc
   export PATH=$PATH:/usr/local/bin
   ```

### Issue: Angular Development Server Won't Start

**Symptoms:**
```bash
Port 4200 is already in use
Error: Cannot find module '@angular/core'
webpack: Failed to compile
```

**Solutions:**

1. **Kill existing process on port 4200:**
   ```bash
   # Find process using port 4200
   lsof -ti:4200
   
   # Kill the process
   kill -9 $(lsof -ti:4200)
   
   # Or use different port
   ng serve --port 4201
   ```

2. **Reinstall Angular dependencies:**
   ```bash
   cd frontend/sma-assistant
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Check for compilation errors:**
   ```bash
   # Look for detailed error messages
   ng serve --verbose
   ```

### Issue: TypeScript Compilation Errors

**Symptoms:**
```
TS2307: Cannot find module 'primeng/button'
TS2339: Property 'xyz' does not exist on type 'Object'
TS2345: Argument of type 'string' is not assignable to parameter of type 'number'
```

**Solutions:**

1. **Check imports:**
   ```typescript
   // Correct PrimeNG import
   import { ButtonModule } from 'primeng/button';
   
   // Not this:
   import { Button } from 'primeng/button';
   ```

2. **Add type annotations:**
   ```typescript
   // Instead of:
   let data = response;
   
   // Use:
   let data: ChatResponse = response;
   // or
   let data: any = response;
   ```

3. **Check package installation:**
   ```bash
   npm list primeng
   npm install primeng@19 primeicons
   ```

## 🌐 CORS and Network Issues

### Issue: CORS Errors in Browser

**Symptoms:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/chat' from origin 'http://localhost:4200' has been blocked by CORS policy
```

**Causes:**
- Backend server not running
- CORS not configured properly
- Wrong URLs

**Solutions:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/api/health
   # Should return JSON response
   ```

2. **Check CORS configuration in `api/main.py`:**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:4200"],  # Frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Verify URLs match:**
   - Frontend: `http://localhost:4200`
   - Backend: `http://localhost:8000`
   - API Service URL in Angular should match backend

### Issue: Network Connection Failed

**Symptoms:**
```
HttpErrorResponse: Http failure response for http://localhost:8000/api/chat: 0 Unknown Error
net::ERR_CONNECTION_REFUSED
```

**Solutions:**

1. **Check if backend is running:**
   ```bash
   # Should show uvicorn process
   ps aux | grep uvicorn
   
   # Or check if port is in use
   lsof -i :8000
   ```

2. **Restart backend server:**
   ```bash
   # Stop any existing process
   pkill -f uvicorn
   
   # Start fresh
   python -m uvicorn api.main:app --reload
   ```

3. **Check firewall/antivirus:**
   - Temporarily disable to test
   - Add exceptions for localhost ports 4200 and 8000

## 🧪 Testing Issues

### Issue: Tests Won't Run

**Symptoms:**
```bash
pytest: command not found
No tests ran
ModuleNotFoundError in tests
```

**Solutions:**

1. **Install pytest:**
   ```bash
   pip install pytest
   # or
   pip install -r requirements.txt
   ```

2. **Run from correct directory:**
   ```bash
   # Backend tests - run from project root
   pwd  # Should be .../sma-assistant
   pytest
   
   # Frontend tests - run from Angular directory
   cd frontend/sma-assistant
   npm test
   ```

3. **Check test file imports:**
   ```python
   # Make sure imports are correct
   from api.main import app
   from chat_schema import ChatRequest
   ```

### Issue: Import Errors in Tests

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'api'
ImportError: attempted relative import with no known parent package
```

**Solutions:**

1. **Add `__init__.py` files:**
   ```bash
   touch api/__init__.py
   touch utils/__init__.py
   ```

2. **Run tests as module:**
   ```bash
   python -m pytest
   ```

3. **Use absolute imports:**
   ```python
   # Instead of:
   from .main import app
   
   # Use:
   from api.main import app
   ```

## 🛠️ Development Environment Issues

### Issue: VS Code Extensions Not Working

**Symptoms:**
- No Python IntelliSense
- TypeScript errors not showing
- No auto-completion

**Solutions:**

1. **Install required extensions:**
   - Python (Microsoft)
   - Angular Language Service
   - TypeScript and JavaScript Language Features

2. **Select correct Python interpreter:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose the one from your virtual environment

3. **Reload VS Code:**
   - Press `Ctrl+Shift+P`
   - Type "Developer: Reload Window"

### Issue: Git Issues

**Symptoms:**
```bash
git: command not found
Permission denied (publickey)
fatal: not a git repository
```

**Solutions:**

1. **Install Git:**
   - **Windows**: Download from [git-scm.com](https://git-scm.com)
   - **macOS**: `brew install git` or install Xcode Command Line Tools
   - **Linux**: `sudo apt install git`

2. **Configure Git:**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

3. **Initialize repository (if needed):**
   ```bash
   git init
   git remote add origin [repository-url]
   ```

## 🔍 Debugging Techniques

### Finding More Information

1. **Check logs:**
   ```bash
   # Backend logs (in terminal where uvicorn is running)
   # Look for error tracebacks
   
   # Frontend logs (browser console)
   # Press F12, check Console tab
   ```

2. **Use verbose modes:**
   ```bash
   # Backend
   python -m uvicorn api.main:app --reload --log-level debug
   
   # Frontend
   ng serve --verbose
   
   # Tests
   pytest -v -s
   ```

3. **Test individual components:**
   ```bash
   # Test Python imports
   python -c "from api.main import app; print('OK')"
   
   # Test API endpoints
   curl http://localhost:8000/api/health
   
   # Test frontend compilation
   ng build --dry-run
   ```

### Using Browser Developer Tools

1. **Open Developer Tools:**
   - Press `F12` or right-click → "Inspect"

2. **Check Console tab:**
   - Look for JavaScript errors (red text)
   - Check for network request failures

3. **Check Network tab:**
   - See if API requests are being made
   - Check response status codes and content

4. **Check Application tab:**
   - Verify local storage/session storage
   - Check if service worker is registered

## 📞 When to Ask for Help

### Try These First (15-30 minutes)

1. **Read the error message carefully**
2. **Check this troubleshooting guide**
3. **Search the error online with project context**
4. **Try a simple restart** (terminal, VS Code, computer)

### Ask for Help When

1. **You've been stuck for more than 30 minutes on setup**
2. **Error messages don't make sense after research**
3. **Multiple things are broken at once**
4. **You need clarification on project requirements**

### How to Ask for Help Effectively

**❌ Bad:**
"My code doesn't work"

**✅ Good:**
```
I'm trying to start the backend server but getting this error:

[paste exact error message]

Here's what I've tried:
1. Activated virtual environment
2. Installed requirements.txt
3. Created .env file with API key

My environment:
- OS: Windows 10
- Python version: 3.11.2
- Current directory: /path/to/sma-assistant

The error happens when I run: python -m uvicorn api.main:app --reload
```

## 📚 Additional Resources

### Official Documentation
- [Python Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Angular Documentation](https://angular.io/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Common Error Databases
- [Stack Overflow](https://stackoverflow.com/) - Search your exact error
- [GitHub Issues](https://github.com/) - Check project repositories for known issues
- [MDN Web Docs](https://developer.mozilla.org/) - Frontend web technologies

### Learning Resources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Angular Tutorial](https://angular.io/tutorial)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

## 🎯 Quick Reference Commands

### Backend
```bash
# Setup
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Run
python -m uvicorn api.main:app --reload

# Test
pytest
pytest -v
pytest test_api.py
```

### Frontend
```bash
# Setup
cd frontend/sma-assistant
npm install

# Run
npm start
ng serve

# Test
npm test
ng test

# Build
ng build
```

### Git
```bash
# Basic workflow
git status
git add .
git commit -m "description"
git push origin branch-name

# Branching
git checkout -b new-branch
git checkout main
git merge branch-name
```

---

Remember: Every developer faces these issues when starting. Don't get discouraged - it's part of the learning process! 🚀
