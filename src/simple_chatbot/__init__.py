"""Simple Chatbot: A LangChain and Ollama learning project.

This package provides a simple chatbot implementation using LangChain
for orchestration and Ollama for local LLM execution.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from simple_chatbot.chatbot import SimpleChatbot
from simple_chatbot.config import ChatbotConfig

__all__ = ["SimpleChatbot", "ChatbotConfig"]
