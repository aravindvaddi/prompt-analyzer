#!/usr/bin/env python3
"""
Check .env file configuration
"""

import os
import sys
from pathlib import Path

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_env_file():
    """Check if .env file exists and has required values"""
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    print("Checking .env configuration...\n")
    
    # Check if .env exists
    if not env_path.exists():
        print(f"{RED}✗ .env file not found!{RESET}")
        
        if env_example_path.exists():
            print(f"\n{YELLOW}To fix:{RESET}")
            print("1. Copy the example file:")
            print(f"   {GREEN}cp .env.example .env{RESET}")
            print("2. Edit .env and add your Claude API key")
            print("3. Get a key from: https://console.anthropic.com/")
        return False
    
    print(f"{GREEN}✓ .env file exists{RESET}")
    
    # Read .env file
    with open(env_path) as f:
        env_content = f.read()
    
    # Check for API key
    has_api_key = False
    api_key_set = False
    
    for line in env_content.split('\n'):
        if line.strip().startswith('CLAUDE_API_KEY='):
            has_api_key = True
            value = line.split('=', 1)[1].strip()
            
            if value and value != 'your_claude_api_key_here':
                api_key_set = True
                # Don't print the actual key
                print(f"{GREEN}✓ CLAUDE_API_KEY is set{RESET}")
            else:
                print(f"{RED}✗ CLAUDE_API_KEY not configured{RESET}")
                print(f"\n{YELLOW}To fix:{RESET}")
                print("1. Get an API key from: https://console.anthropic.com/")
                print("2. Edit .env and replace 'your_claude_api_key_here' with your actual key")
    
    if not has_api_key:
        print(f"{RED}✗ CLAUDE_API_KEY not found in .env{RESET}")
        print(f"\n{YELLOW}To fix:{RESET}")
        print("1. Add this line to your .env file:")
        print("   CLAUDE_API_KEY=your_actual_api_key_here")
    
    # Check Redis URL (optional)
    if 'REDIS_URL=' in env_content:
        print(f"{GREEN}✓ REDIS_URL configured{RESET}")
    else:
        print(f"{YELLOW}! REDIS_URL not set (using default: redis://localhost:6379){RESET}")
    
    print("\n" + "="*50)
    
    if api_key_set:
        print(f"{GREEN}Environment is properly configured!{RESET}")
        return True
    else:
        print(f"{RED}Environment needs configuration{RESET}")
        return False

if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent)  # Go to project root
    
    if check_env_file():
        sys.exit(0)
    else:
        sys.exit(1)
