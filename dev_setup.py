#!/usr/bin/env python3
"""
Development setup script for RAG Indexer Interface
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🚀 RAG Indexer Interface - Development Setup")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'uploads', 'logs', 'sample_data/source', 'sample_data/eval']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# RAG Indexer Interface Configuration
# API Keys (Required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional API Keys
CO_API_KEY=your_cohere_api_key_here

# Flask Settings
SECRET_KEY=your-secret-key-change-in-production
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=8080

# Rate Limiting
RATE_LIMIT_DEFAULT=200 per day, 50 per hour
RATE_LIMIT_ASK=10 per minute
RATE_LIMIT_UPLOAD=5 per minute

# Database Settings
LANCEDB_PATH=./data/rag_database

# File Upload Settings
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Model Settings
EMBEDDING_MODEL=all-mpnet-base-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Search Settings
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Sample Data
SAMPLE_DATA_PATH=./sample_data/source
EVAL_DATA_PATH=./sample_data/eval/sample_questions.json
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please update ANTHROPIC_API_KEY in .env file")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def create_sample_data():
    """Create sample data files"""
    sample_source = Path('sample_data/source')
    sample_eval = Path('sample_data/eval')
    
    # Create sample text file
    sample_text = """# Welcome to RAG Indexer Interface

This is a sample document that demonstrates the capabilities of the RAG (Retrieval Augmented Generation) system.

## Features

- **Document Processing**: Upload and process various document formats
- **AI-Powered Search**: Ask questions and get intelligent answers
- **Vector Storage**: Efficient storage and retrieval of document embeddings
- **Modern Interface**: Clean, responsive web interface with dark/light mode

## Getting Started

1. Upload your documents using the file upload interface
2. Ask questions about your documents
3. Get AI-powered responses based on your content

## Supported Formats

- PDF files
- Text files (.txt)
- Word documents (.doc, .docx)
- Markdown files (.md)

This sample document will help you test the system functionality.
"""
    
    with open(sample_source / 'sample_document.txt', 'w') as f:
        f.write(sample_text)
    
    # Create sample evaluation questions
    eval_questions = {
        "questions": [
            {
                "question": "What is RAG Indexer Interface?",
                "expected_answer": "A system for document processing and AI-powered search"
            },
            {
                "question": "What document formats are supported?",
                "expected_answer": "PDF, TXT, DOC, DOCX, and MD files"
            },
            {
                "question": "How do I get started with the system?",
                "expected_answer": "Upload documents and ask questions about them"
            }
        ]
    }
    
    import json
    with open(sample_eval / 'sample_questions.json', 'w') as f:
        json.dump(eval_questions, f, indent=2)
    
    print("✅ Created sample data files")

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    try:
        # Test configuration
        from config import validate_config, get_config_summary
        config_valid = validate_config()
        config_summary = get_config_summary()
        
        print("📊 Configuration Summary:")
        for key, value in config_summary.items():
            print(f"  - {key}: {value}")
        
        if not config_valid:
            print("⚠️  Configuration validation failed - please check your .env file")
        else:
            print("✅ Configuration is valid")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next Steps:")
    print("1. Update your API keys in the .env file")
    print("2. Run the application: python app.py")
    print("3. Open your browser to: http://localhost:8080")
    print("\n🐳 For Docker deployment:")
    print("1. docker-compose up --build")
    print("2. Open: http://localhost:8080")
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    print("\n📁 Creating directories...")
    create_directories()
    
    print("\n🔧 Creating configuration...")
    create_env_file()
    
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        sys.exit(1)
    
    print("\n📄 Creating sample data...")
    create_sample_data()
    
    print("\n🧪 Running tests...")
    run_tests()
    
    print_next_steps()

if __name__ == '__main__':
    main() 