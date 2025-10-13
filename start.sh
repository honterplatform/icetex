#!/bin/bash

# ICETEX Petition Classifier - Start Script
# Quick script to start the application

echo "🎓 Starting ICETEX Petition Classifier..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run './setup.sh' first to set up the project."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your OpenAI API key."
    echo "See README.md for instructions."
    exit 1
fi

# Start the server
echo "🚀 Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

