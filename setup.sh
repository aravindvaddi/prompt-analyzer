#!/bin/bash

# Quick setup script for Prompt Analyzer

echo "🚀 Setting up Prompt Analyzer..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your CLAUDE_API_KEY"
    echo "   You can get one from: https://console.anthropic.com/"
    exit 1
fi

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "🐍 Installing Python dependencies..."
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cd ..

echo "📦 Installing Node dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Make sure Docker is running (for Redis)"
echo "  2. Run: make dev"
echo ""
echo "Or start services individually:"
echo "  - Redis: docker-compose up -d redis"
echo "  - Backend: cd backend && uv run uvicorn main:app --reload"
echo "  - Frontend: cd frontend && npm run dev"
