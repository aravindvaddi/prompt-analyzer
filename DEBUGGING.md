# Debugging Guide - Prompt Analyzer

## Common Issues and Solutions

### 1. 500 Internal Server Error

**Check the logs first!** The updated backend now logs everything.

#### Missing Claude API Key
```
ERROR - CLAUDE_API_KEY not properly set in .env file!
```
**Solution**: 
- Copy `.env.example` to `.env`
- Add your Claude API key from https://console.anthropic.com/

#### Invalid Claude API Key
```
ERROR - Analysis failed: Invalid Claude API key
```
**Solution**: 
- Verify your API key is correct
- Check if your key has access to claude-3-opus model

#### Redis Connection Failed
```
WARNING - Redis connection failed: Connection refused
```
**Solution**: 
- Start Redis: `redis-server` or `brew services start redis`
- This won't cause 500 errors (cache is optional)

### 2. Testing the Backend

Run the test script to verify everything works:
```bash
cd backend
python test_backend.py
```

This tests:
- Health endpoint
- Various analyze scenarios (valid, invalid, edge cases)
- CORS configuration
- Error handling

### 3. Viewing Logs

The backend now logs everything:
- Every request/response
- Detailed error messages
- Claude API interactions
- Cache operations

Look for these log levels:
- `INFO`: Normal operations
- `WARNING`: Non-critical issues (like cache miss)
- `ERROR`: Problems that need fixing
- `DEBUG`: Detailed diagnostic info

### 4. Manual Testing

Test a simple prompt:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test prompt"}' \
  -v
```

The `-v` flag shows full request/response details.

### 5. Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Analysis service not available" | No Claude API key | Set CLAUDE_API_KEY in .env |
| "Failed to parse analysis response" | Claude returned non-JSON | Check system prompt, retry |
| "Rate limit exceeded" | Too many API calls | Wait, or implement better caching |
| "Network error" | Can't reach Claude API | Check internet connection |

### 6. Frontend Can't Connect

If frontend shows connection errors:
1. Verify backend is running on port 8000
2. Check CORS is configured for http://localhost:3000
3. Look for CORS errors in browser console

### Still Having Issues?

1. Stop all services
2. Run `./verify-startup.sh` from project root
3. Check each service starts properly
4. Run `python test_backend.py` to verify functionality
5. Check logs for specific error messages

Remember: **Always check the logs first!** They now tell you exactly what's wrong.
