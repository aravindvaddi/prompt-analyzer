# Prompt Analyzer - VERIFIED WORKING INSTRUCTIONS

A web application that analyzes prompts using Claude AI and provides actionable improvement suggestions.

## Prerequisites

1. **Python 3.8+**
2. **Node.js 18+**
3. **Redis** (install with `brew install redis` on Mac)
4. **Claude API Key** from https://console.anthropic.com/

## Quick Start (Tested & Verified)

### 1. Set up environment

```bash
cd /Users/start/start/lisa/projects/prompt-analyzer

# Create .env file and add your Claude API key
cp .env.example .env
# Edit .env and replace 'your_claude_api_key_here' with your actual key

# Verify environment is configured correctly
cd backend && python check_env.py && cd ..
```

### 2. Start the services (3 terminals needed)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

You should see:
```
INFO - Starting Prompt Analyzer Backend
INFO - Claude API key found
INFO - Connected to Redis at redis://localhost:6379
INFO - Application startup complete
INFO - Uvicorn running on http://127.0.0.1:8000
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

You should see:
```
▲ Next.js 14.0.0
- Local: http://localhost:3000
✓ Ready
```

### 3. Access the application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Testing

### Backend Tests
```bash
cd backend
python test_backend.py
```

This runs comprehensive tests including error scenarios.

### Manual API Test
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about Paris"}'
```

## Troubleshooting

### 500 Internal Server Error

1. **Check the backend logs** - They now show detailed error messages
2. **Verify Claude API key** is set correctly:
   ```bash
   cd backend && python check_env.py
   ```
3. **Common issues:**
   - Missing or invalid CLAUDE_API_KEY
   - Redis not running
   - Port 8000 or 3000 already in use

### Backend won't start

```bash
# Check if dependencies are installed
pip list | grep fastapi

# If missing, reinstall:
pip install -r requirements.txt
```

### Frontend connection issues

1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify NEXT_PUBLIC_API_URL in .env is correct

### See DEBUGGING.md for detailed troubleshooting

## Project Structure

```
prompt-analyzer/
├── backend/
│   ├── main.py           # FastAPI application with logging
│   ├── requirements.txt  # Python dependencies
│   ├── test_backend.py   # Comprehensive test suite
│   └── check_env.py      # Environment checker
├── frontend/
│   ├── app/
│   │   ├── page.tsx      # Main UI component
│   │   └── layout.tsx    # Layout wrapper
│   └── package.json      # Node dependencies
├── .env.example          # Environment template
├── DEBUGGING.md          # Troubleshooting guide
└── verify-startup.sh     # Startup verification script
```

## Features

- ✅ Prompt analysis using Claude AI
- ✅ Score and technique identification
- ✅ Actionable improvement suggestions
- ✅ Clean, responsive UI
- ✅ Redis caching for performance
- ✅ Comprehensive error handling
- ✅ Detailed logging for debugging

## Development Workflow

1. **Make changes**
2. **Run tests**: `python test_backend.py`
3. **Check logs** for any issues
4. **Verify in browser** at http://localhost:3000

## Team Standards

- Always test error cases, not just happy path
- Add logging before claiming "it works"
- Run the verification script before commits
- Document any new dependencies

---

**Built by the team with lessons learned the hard way!**
