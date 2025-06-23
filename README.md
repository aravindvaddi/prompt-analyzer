# Prompt Analyzer

[![CI/CD Pipeline](https://github.com/aravindvaddi/prompt-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/aravindvaddi/prompt-analyzer/actions/workflows/ci.yml)

A web application that analyzes prompts using Claude AI and provides actionable improvement suggestions with scoring and technique identification.

## Features

- 🔍 **Prompt Analysis**: Deep analysis of prompts using Claude AI
- 📊 **Scoring System**: Get quality scores for your prompts
- 💡 **Improvement Suggestions**: Actionable recommendations to enhance your prompts
- 🎯 **Technique Identification**: Understand which prompting techniques are being used
- ⚡ **Redis Caching**: Fast performance with intelligent caching
- 🎨 **Modern UI**: Clean, responsive interface built with Next.js
- 📚 **API Documentation**: Interactive API docs with Swagger UI

## Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **Redis** (or use Docker)
- **Claude API Key** from [Anthropic Console](https://console.anthropic.com/)

## Quick Start

### Option 1: Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/aravindvaddi/prompt-analyzer.git
cd prompt-analyzer
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY
```

3. Start all services:
```bash
docker-compose up
```

4. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/aravindvaddi/prompt-analyzer.git
cd prompt-analyzer
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY
```

3. Install and start Redis:
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Or use Docker
docker run -d -p 6379:6379 redis:7-alpine
```

4. Set up backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

5. Set up frontend:
```bash
cd ../frontend
npm install
```

6. Start the services:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

7. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest -v --cov=.
```

**Frontend:**
```bash
cd frontend
npm test
```

### Linting

**Backend:**
```bash
cd backend
ruff check .
ruff format .
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Project Structure

```
prompt-analyzer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── pyproject.toml       # Python project configuration
│   ├── tests/               # Backend tests
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── app/                 # Next.js app directory
│   ├── package.json         # Node dependencies
│   └── Dockerfile           # Frontend container
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── docker-compose.yml       # Docker composition
├── .env.example             # Environment template
└── README.md                # This file
```

## API Usage

### Analyze a Prompt

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about the history of artificial intelligence"}'
```

### Response Format

```json
{
  "score": 7.5,
  "techniques": ["Direct Question", "Open-ended"],
  "suggestions": [
    "Add specific context or time period",
    "Include desired format or length",
    "Specify particular aspects of interest"
  ],
  "improved_prompt": "Provide a comprehensive overview of artificial intelligence history from 1950 to present..."
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_API_KEY` | Your Anthropic API key | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `REDIS_TTL` | Cache TTL in seconds | `86400` (24 hours) |
| `API_PORT` | Backend API port | `8000` |
| `NEXT_PUBLIC_API_URL` | Frontend API URL | `http://localhost:8000` |

## Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check backend logs for detailed error messages
   - Verify your Claude API key is set correctly
   - Ensure Redis is running

2. **Connection Refused**
   - Ensure all services are running
   - Check if ports 3000, 8000, and 6379 are available
   - Verify environment variables are set correctly

3. **Module Not Found**
   - Backend: Run `pip install -e ".[dev]"`
   - Frontend: Run `npm install`

### Debug Mode

Enable debug logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/)
- Powered by [Claude AI](https://www.anthropic.com/claude) from Anthropic
- Caching with [Redis](https://redis.io/)

---

**Built with ❤️ by the team**