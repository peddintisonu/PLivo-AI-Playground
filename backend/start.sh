#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server..."
python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
