# Quick note from Quinn!

Hey team, noticed we forgot the Dockerfiles 😅 Just added them!

If Docker is being finicky, here's the quickest way to get running:

## Super Quick Start (No Docker)

1. **Terminal 1 - Start Redis:**
```bash
brew install redis  # If you don't have it
redis-server
```

2. **Terminal 2 - Start Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

3. **Terminal 3 - Start Frontend:**
```bash
cd frontend
npm install
npm run dev
```

That's it! Backend runs on http://localhost:8000, frontend on http://localhost:3000

Don't forget to create your .env file with your Claude API key first!
