#!/usr/bin/env python3
"""
Test script to verify API key is working
"""
from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the API key is working"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")
    
    try:
        client = Anthropic()
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Hello, this is a test message."}
            ],
        )
        print("✅ API key is working!")
        print(f"Response: {response.content[0].text}")
        return True
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

if __name__ == "__main__":
    test_api_key() 