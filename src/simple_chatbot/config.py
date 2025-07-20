"""Configuration module for the Simple Chatbot.

This module contains configuration classes and settings for the chatbot,
including Ollama connection settings and model parameters.
"""

import os

from pydantic import BaseModel, Field


class ChatbotConfig(BaseModel):
    """Configuration class for the Simple Chatbot.

    This class handles all configuration parameters for the chatbot,
    including Ollama connection settings and model parameters.

    Attributes:
        ollama_base_url: Base URL for Ollama API (default: http://localhost:11434)
        model_name: Name of the model to use (default: llama2)
        temperature: Temperature for text generation (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        system_prompt: System prompt to set chatbot behavior
        conversation_memory_limit: Maximum number of messages to keep in memory
    """

    ollama_base_url: str = Field(
        default="http://localhost:11434", description="Base URL for Ollama API"
    )

    model_name: str = Field(
        default="llama2", description="Name of the Ollama model to use"
    )

    temperature: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Temperature for text generation"
    )

    max_tokens: int = Field(
        default=2000, gt=0, description="Maximum number of tokens to generate"
    )

    system_prompt: str = Field(
        default="You are a helpful assistant. "
        "Respond in a friendly and informative manner.",
        description="System prompt to set chatbot behavior",
    )

    conversation_memory_limit: int = Field(
        default=10,
        gt=0,
        description="Maximum number of message pairs to keep in conversation memory",
    )

    @classmethod
    def from_env(cls) -> "ChatbotConfig":
        """Create configuration from environment variables.

        Returns:
            ChatbotConfig: Configuration instance with values from environment
        """
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model_name=os.getenv("OLLAMA_MODEL", "llama2"),
            temperature=float(os.getenv("CHATBOT_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("CHATBOT_MAX_TOKENS", "2000")),
            system_prompt=os.getenv(
                "CHATBOT_SYSTEM_PROMPT",
                "You are a helpful assistant. "
                "Respond in a friendly and informative manner.",
            ),
            conversation_memory_limit=int(os.getenv("CONVERSATION_MEMORY_LIMIT", "10")),
        )
