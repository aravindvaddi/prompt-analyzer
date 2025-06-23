#!/bin/bash

# Navigate to backend directory
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Make test script executable
chmod +x test_backend.py

# Run tests
python test_backend.py
