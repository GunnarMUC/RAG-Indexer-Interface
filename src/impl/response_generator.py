from typing import List
from interface.base_response_generator import BaseResponseGenerator
from util.invoke_ai import invoke_ai, invoke_ai_thinking, invoke_ai_programming
import re

SYSTEM_PROMPT = """
Use the provided context to provide a concise answer to the user's question.
If you cannot find the answer in the context, say so. Do not make up information.
"""

SYSTEM_PROMPT_THINKING = """
You are an expert analyst. Use the provided context to provide a comprehensive, well-reasoned answer to the user's question.
Consider multiple perspectives, provide detailed explanations, and show your reasoning process.
If you cannot find the answer in the context, say so. Do not make up information.
"""

SYSTEM_PROMPT_PROGRAMMING = """
You are a technical expert. Use the provided context to provide a clear, accurate answer to the user's question.
Focus on technical accuracy and practical solutions. If you cannot find the answer in the context, say so.
"""

class ResponseGenerator(BaseResponseGenerator):
    def _is_thinking_query(self, query: str) -> bool:
        """Determine if this is a complex thinking/analysis query."""
        thinking_keywords = [
            'why', 'how', 'explain', 'analyze', 'compare', 'contrast', 'evaluate',
            'discuss', 'interpret', 'reason', 'logic', 'think', 'consider',
            'what do you think', 'what is your opinion', 'what are the implications',
            'complex', 'detailed', 'thorough', 'comprehensive'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in thinking_keywords)
    
    def _is_programming_query(self, query: str) -> bool:
        """Determine if this is a programming/technical query."""
        programming_keywords = [
            'code', 'program', 'script', 'function', 'class', 'method', 'api',
            'database', 'algorithm', 'bug', 'error', 'debug', 'test', 'deploy',
            'install', 'configure', 'setup', 'technical', 'implementation',
            'syntax', 'compiler', 'runtime', 'framework', 'library'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in programming_keywords)
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate a response using the appropriate AI model based on query type."""
        # Combine context into a single string
        context_text = "\n".join(context)
        user_message = (
            f"<context>\n{context_text}\n</context>\n"
            f"<question>\n{query}\n</question>"
        )

        # Choose the appropriate model based on query type
        if self._is_thinking_query(query):
            print("🧠 Using Claude Opus for complex thinking query")
            return invoke_ai_thinking(system_message=SYSTEM_PROMPT_THINKING, user_message=user_message)
        elif self._is_programming_query(query):
            print("💻 Using Claude Sonnet for programming query")
            return invoke_ai_programming(system_message=SYSTEM_PROMPT_PROGRAMMING, user_message=user_message)
        else:
            print("🤖 Using Claude Sonnet for general query")
            return invoke_ai(system_message=SYSTEM_PROMPT, user_message=user_message)
