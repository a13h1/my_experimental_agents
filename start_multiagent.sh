#!/bin/bash

# Multi-Agent Platform Quick Start Script

set -e

PROJECT_DIR="/Users/abhishek/projects/HelloAgent"
cd "$PROJECT_DIR"

echo "🚀 Hello Agent - Multi-Agent Platform"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found at .venv"
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Verify dependencies
echo "✓ Checking dependencies..."
python -m pip install -q -r requirements.txt

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY environment variable not set"
    echo "You will be prompted to enter it in the Streamlit app sidebar"
    echo ""
fi

# Run the app
echo ""
echo "🎯 Launching Streamlit app..."
echo "📋 Open your browser at: http://localhost:8501"
echo ""
echo "Available Agents:"
echo "  • Tab 1: 📤 Upload & Preview (CSV FAQ)"
echo "  • Tab 2: ❓ Ask Questions (CSV FAQ)"
echo "  • Tab 3: 🎯 CRM Lead Qualifier ⭐ NEW"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

streamlit run hello_agent_csv_faq.py
