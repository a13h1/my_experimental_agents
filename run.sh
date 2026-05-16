#!/bin/bash

# Hello Agent - Launch Script

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if requirements are installed
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Start the app
echo ""
echo "🤖 Starting Hello Agent..."
echo "📍 The app will open at http://localhost:8501"
echo "💡 Press Ctrl+C to stop the server"
echo ""

streamlit run hello_agent_csv_faq.py
