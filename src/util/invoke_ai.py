from anthropic import Anthropic
from dotenv import load_dotenv
import os
from enum import Enum

# Load environment variables from .env file
load_dotenv()

class ModelType(Enum):
    """Enum for different model types based on task."""
    THINKING = "claude-3-5-sonnet-20241022"  # Using Sonnet for thinking (Opus not available)
    PROGRAMMING = "claude-3-5-sonnet-20241022"  # Good for programming, cost-effective
    DEFAULT = "claude-3-5-sonnet-20241022"  # Fallback model

def invoke_ai(system_message: str, user_message: str, model_type: ModelType = ModelType.DEFAULT) -> str:
    """
    Generic function to invoke Claude AI model given a system and user message.
    
    Args:
        system_message: The system prompt/instructions
        user_message: The user's question or request
        model_type: Which model to use (THINKING, PROGRAMMING, or DEFAULT)
    
    Returns:
        The AI's response as a string
    """
    # Force reload environment variables and clear any cached values
    load_dotenv(override=True)
    
    # Get API key and verify it's loaded
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    print(f"🔑 Using API key: {api_key[:20]}...")
    
    client = Anthropic(api_key=api_key)  # Explicitly pass the API key
    
    # Adjust max_tokens based on model type
    max_tokens = 2000 if model_type == ModelType.THINKING else 1000
    
    try:
        response = client.messages.create(
            model=model_type.value,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": f"{system_message}\n\n{user_message}"}
            ],
        )
        return response.content[0].text
    except Exception as e:
        print(f"⚠️  Model invocation failed: {e}")
        raise e

def invoke_ai_thinking(system_message: str, user_message: str) -> str:
    """
    Invoke Claude for complex thinking, analysis, and reasoning tasks.
    Best for: complex analysis, creative thinking, detailed explanations
    """
    return invoke_ai(system_message, user_message, ModelType.THINKING)

def invoke_ai_programming(system_message: str, user_message: str) -> str:
    """
    Invoke Claude for programming and technical tasks.
    Best for: code generation, debugging, technical explanations
    """
    return invoke_ai(system_message, user_message, ModelType.PROGRAMMING)

def invoke_ai_default(system_message: str, user_message: str) -> str:
    """
    Invoke the default model for general tasks.
    """
    return invoke_ai(system_message, user_message, ModelType.DEFAULT)
