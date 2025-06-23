#!/bin/bash

# Startup Verification Script
# This MUST pass before any code is considered ready

set -e  # Exit on any error

echo "🔍 Verifying Prompt Analyzer Startup..."
echo "======================================="

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Run this from the project root directory"
    exit 1
fi

# Backend verification
echo -e "\n📦 Checking Backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install deps
source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Test imports
echo "Testing imports..."
python -c "
try:
    from main import app
    print('✅ Backend imports successful')
except Exception as e:
    print(f'❌ Backend import failed: {e}')
    exit(1)
"

# Check for .env file
if [ ! -f "../.env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env from .env.example and add your CLAUDE_API_KEY"
    exit 1
fi

# Check if API key is set
if grep -q "your_claude_api_key_here" ../.env; then
    echo "⚠️  Warning: Claude API key not set in .env file"
fi

cd ..

# Frontend verification
echo -e "\n📦 Checking Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --silent
fi

# Test build
echo "Testing frontend build..."
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend builds successfully"
else
    echo "❌ Frontend build failed"
    exit 1
fi

cd ..

echo -e "\n======================================="
echo "✅ ALL CHECKS PASSED!"
echo ""
echo "To run the application:"
echo "  1. Terminal 1: redis-server"
echo "  2. Terminal 2: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  3. Terminal 3: cd frontend && npm run dev"
echo ""
echo "API will be at: http://localhost:8000"
echo "UI will be at: http://localhost:3000"
