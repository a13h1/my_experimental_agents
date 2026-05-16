#!/usr/bin/env python3
"""
Quick verification script to check if all dependencies are properly installed
"""

import sys
import os

def check_imports():
    """Check if all required imports work"""
    
    required_packages = {
        'streamlit': 'Streamlit (Web UI framework)',
        'pandas': 'Pandas (Data manipulation)',
        'langchain': 'LangChain (AI framework)',
        'langchain_openai': 'LangChain OpenAI',
        'langchain_experimental': 'LangChain Experimental',
        'openai': 'OpenAI (LLM)',
    }
    
    print("🔍 Checking dependencies...\n")
    
    all_good = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package:<25} - {description}")
        except ImportError as e:
            print(f"✗ {package:<25} - MISSING")
            all_good = False
    
    print()
    
    if all_good:
        print("✅ All dependencies are installed!")
        print("\n📝 Next steps:")
        print("1. Set your OpenAI API key in the app (via sidebar)")
        print("2. Run: streamlit run app.py")
        print("3. Upload CSV files and start asking questions!\n")
        return 0
    else:
        print("❌ Some dependencies are missing!")
        print("\n📝 To install them, run:")
        print("pip install -r requirements.txt\n")
        return 1

if __name__ == "__main__":
    sys.exit(check_imports())
