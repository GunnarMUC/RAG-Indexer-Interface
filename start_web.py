#!/usr/bin/env python3
"""
Simple startup script for the RAG Pipeline Web Interface
"""

import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    print("🚀 Starting RAG Pipeline Web Interface...")
    print("📝 Make sure your .env file contains your ANTHROPIC_API_KEY")
    print("🌐 The web interface will be available at: http://localhost:3000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    from app import app
    app.run(debug=True, host='0.0.0.0', port=3000) 