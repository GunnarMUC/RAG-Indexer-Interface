from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def invoke_ai(system_message: str, user_message: str) -> str:
    """
    Generic function to invoke Claude AI model given a system and user message.
    Replace this if you want to use a different AI model.
    """

    client = Anthropic()  # Uses environment variable $ANTHROPIC_API_KEY from .env file
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"{system_message}\n\n{user_message}"}
        ],
    )
    return response.content[0].text
