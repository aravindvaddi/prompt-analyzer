"""
Prompt Analyzer Backend - Core Application
Built with FastAPI and Claude SDK
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List, Optional
import hashlib
import json
import logging
import sys
import traceback
from anthropic import Anthropic
import redis.asyncio as redis
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Log startup
logger.info("Starting Prompt Analyzer Backend")
logger.info(f"Python version: {sys.version}")

# Check for required environment variables
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY or CLAUDE_API_KEY == "your_claude_api_key_here":
    logger.error("CLAUDE_API_KEY not properly set in .env file!")
    logger.error("Please set a valid Claude API key to continue")
else:
    logger.info("Claude API key found")

# Initialize FastAPI app
app = FastAPI(
    title="Prompt Analyzer API",
    description="Analyze and improve your prompts with AI",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        # Log response
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response: {response.status_code} - Duration: {duration:.3f}s")
        
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Initialize clients
try:
    claude_client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None
    if claude_client:
        logger.info("Claude client initialized successfully")
    else:
        logger.error("Claude client not initialized - missing API key")
except Exception as e:
    logger.error(f"Failed to initialize Claude client: {str(e)}")
    claude_client = None

redis_client = None

# Request/Response models
class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., max_length=2000, description="The prompt to analyze")

class Suggestion(BaseModel):
    issue: str
    suggestion: str
    example: Optional[str] = None

class AnalysisResponse(BaseModel):
    score: int = Field(..., ge=1, le=10)
    technique: str
    strengths: List[str]
    issues: List[str]
    suggestions: List[Suggestion]

# System prompt (loaded from knowledge base)
ANALYSIS_SYSTEM_PROMPT = """You are an expert prompt engineering analyst trained on best practices from promptingguide.ai. Your task is to analyze user prompts and provide actionable feedback.

For each prompt, evaluate:

1. **Structure Analysis**
   - Clarity of instructions
   - Presence of context
   - Use of examples
   - Overall organization

2. **Technique Identification**
   - Zero-shot: Direct instruction without examples
   - Few-shot: Instruction with examples
   - Chain-of-thought: Step-by-step reasoning request
   - Other patterns

3. **Common Issues**
   - Ambiguous instructions
   - Missing context
   - Overly complex phrasing
   - Lack of output format specification

4. **Scoring Rubric** (1-10)
   - 1-3: Major issues, unclear intent
   - 4-6: Functional but needs improvement  
   - 7-9: Good prompt with minor improvements
   - 10: Excellent, follows best practices

Provide your analysis in this JSON format and ONLY JSON, no other text:
{
  "score": <number 1-10>,
  "technique": "<identified technique>",
  "strengths": ["<strength1>", "<strength2>"],
  "issues": ["<issue1>", "<issue2>"],
  "suggestions": [
    {
      "issue": "<what to fix>",
      "suggestion": "<how to fix it>",
      "example": "<improved version>"
    }
  ]
}

Focus on actionable feedback. Be encouraging but honest. Output ONLY valid JSON."""

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection on startup"""
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    try:
        redis_client = await redis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info(f"Connected to Redis at {redis_url}")
    except Exception as e:
        logger.warning(f"Redis connection failed: {str(e)}")
        logger.warning("Continuing without cache")
        redis_client = None

@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    if redis_client:
        try:
            await redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "redis": "disconnected",
        "claude": "not configured",
        "version": "0.1.0"
    }
    
    # Check Redis
    if redis_client:
        try:
            await redis_client.ping()
            health_status["redis"] = "connected"
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
    
    # Check Claude
    if claude_client:
        health_status["claude"] = "configured"
    
    logger.debug(f"Health check: {health_status}")
    return health_status

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_prompt(request: AnalyzeRequest):
    """Analyze a prompt and return improvement suggestions"""
    
    logger.info(f"Analyzing prompt: '{request.prompt[:50]}...' (length: {len(request.prompt)})")
    
    # Validate Claude client
    if not claude_client:
        logger.error("Claude client not initialized - missing API key")
        raise HTTPException(
            status_code=503,
            detail="Analysis service not available. Please check API key configuration."
        )
    
    # Generate cache key
    cache_key = f"analysis:{hashlib.sha256(request.prompt.encode()).hexdigest()}"
    logger.debug(f"Cache key: {cache_key}")
    
    # Check cache first
    if redis_client:
        try:
            cached = await redis_client.get(cache_key)
            if cached:
                logger.info("Cache hit - returning cached analysis")
                return AnalysisResponse(**json.loads(cached))
            else:
                logger.debug("Cache miss - will call Claude")
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
    
    # Call Claude for analysis
    try:
        logger.info("Calling Claude API for analysis")
        
        message = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system=ANALYSIS_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this prompt: {request.prompt}"
                }
            ]
        )
        
        # Log raw response
        response_text = message.content[0].text
        logger.debug(f"Claude response (first 200 chars): {response_text[:200]}...")
        
        # Try to extract JSON if there's extra text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_text = response_text[json_start:json_end]
            logger.debug(f"Extracted JSON: {json_text[:200]}...")
        else:
            logger.error("No JSON found in Claude response")
            raise ValueError("Claude response did not contain valid JSON")
        
        # Parse response
        try:
            analysis_data = json.loads(json_text)
            logger.info("Successfully parsed Claude response")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            logger.error(f"Failed JSON: {json_text}")
            raise
        
        # Create response object
        try:
            response = AnalysisResponse(**analysis_data)
            logger.info(f"Analysis complete - Score: {response.score}/10, Technique: {response.technique}")
        except ValidationError as e:
            logger.error(f"Response validation failed: {str(e)}")
            logger.error(f"Invalid data: {analysis_data}")
            raise
        
        # Cache the result
        if redis_client:
            try:
                await redis_client.setex(
                    cache_key,
                    86400,  # 24 hour TTL
                    response.json()
                )
                logger.debug("Cached analysis result")
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
        
        return response
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse analysis response. The AI returned invalid JSON."
        )
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis response format invalid: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Analysis failed: {type(e).__name__}: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Provide helpful error messages
        if "api_key" in str(e).lower():
            detail = "Invalid Claude API key. Please check your configuration."
        elif "rate" in str(e).lower():
            detail = "Rate limit exceeded. Please try again later."
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            detail = "Network error connecting to Claude API."
        else:
            detail = f"Analysis failed: {str(e)}"
        
        raise HTTPException(
            status_code=500,
            detail=detail
        )

@app.get("/examples")
async def get_examples():
    """Get example prompts with their analyses"""
    logger.debug("Returning example prompts")
    
    return {
        "examples": [
            {
                "title": "Too Vague",
                "prompt": "Tell me about Paris",
                "expected_score": 4
            },
            {
                "title": "Better",
                "prompt": "Write a 500-word travel guide for Paris focusing on must-see attractions for first-time visitors",
                "expected_score": 7
            },
            {
                "title": "Excellent",
                "prompt": "You are a travel guide writer. Create a 500-word guide for first-time visitors to Paris. Include: 1) Top 5 must-see attractions with brief descriptions, 2) Best time to visit, 3) Getting around the city tips. Use an engaging, friendly tone.",
                "expected_score": 9
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
