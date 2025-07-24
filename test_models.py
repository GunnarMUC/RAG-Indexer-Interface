#!/usr/bin/env python3
"""
Test script to demonstrate different AI models for different tasks.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from util.invoke_ai import invoke_ai_thinking, invoke_ai_programming, invoke_ai_default

def test_model_selection():
    """Test different models for different types of queries."""
    
    print("🧪 Testing Model Selection Strategy")
    print("=" * 50)
    
    # Test thinking query (should use Opus)
    thinking_query = "Why did Goldlake View become a tourist destination? Explain the historical factors and economic implications."
    
    print(f"\n🧠 THINKING QUERY (Opus):")
    print(f"Query: {thinking_query}")
    print("-" * 40)
    
    try:
        response = invoke_ai_thinking(
            system_message="You are an expert historian and economist. Provide a detailed analysis.",
            user_message=thinking_query
        )
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test programming query (should use Sonnet)
    programming_query = "How can I implement a function to search through the database and return relevant results?"
    
    print(f"\n💻 PROGRAMMING QUERY (Sonnet):")
    print(f"Query: {programming_query}")
    print("-" * 40)
    
    try:
        response = invoke_ai_programming(
            system_message="You are a software engineer. Provide practical code solutions.",
            user_message=programming_query
        )
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test general query (should use Sonnet)
    general_query = "What is the Golden Lake?"
    
    print(f"\n🤖 GENERAL QUERY (Sonnet):")
    print(f"Query: {general_query}")
    print("-" * 40)
    
    try:
        response = invoke_ai_default(
            system_message="Provide a clear and concise answer.",
            user_message=general_query
        )
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ Model selection test complete!")
    print("=" * 50)

def test_cost_comparison():
    """Show cost comparison between models."""
    
    print("\n💰 COST COMPARISON")
    print("=" * 30)
    print("Claude Opus (Thinking):")
    print("  - Input: $15.00 per 1M tokens")
    print("  - Output: $75.00 per 1M tokens")
    print("  - Best for: Complex analysis, reasoning")
    print()
    print("Claude Sonnet 3.7 (Programming/General):")
    print("  - Input: $3.00 per 1M tokens")
    print("  - Output: $15.00 per 1M tokens")
    print("  - Best for: Programming, general queries")
    print()
    print("💡 Strategy: Use Opus only for complex thinking tasks")
    print("   Use Sonnet for everything else to save costs")

if __name__ == "__main__":
    test_model_selection()
    test_cost_comparison() 