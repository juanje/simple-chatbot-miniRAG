"""LLM Client module for Ollama integration.

This module provides a client class to interact with Ollama models
using LangChain's Ollama integration.
"""

import logging

from langchain_ollama import OllamaLLM
from pydantic import BaseModel

from simple_chatbot.config import ChatbotConfig

logger = logging.getLogger(__name__)


class OllamaConnectionError(Exception):
    """Raised when connection to Ollama fails."""

    pass


class ModelNotFoundError(Exception):
    """Raised when the specified model is not available."""

    pass


class ChatMessage(BaseModel):
    """Represents a chat message.

    Attributes:
        role: The role of the message sender (user, assistant, system)
        content: The content of the message
    """

    role: str
    content: str


class OllamaClient:
    """Client for interacting with Ollama LLM models.

    This class handles the connection to Ollama and provides methods
    for generating responses from LLM models.

    Attributes:
        config: Configuration object with Ollama settings
        llm: LangChain Ollama LLM instance
    """

    def __init__(self, config: ChatbotConfig) -> None:
        """Initialize the Ollama client.

        Args:
            config: Configuration object with Ollama settings

        Raises:
            OllamaConnectionError: If connection to Ollama fails
        """
        self.config = config
        self._llm: OllamaLLM | None = None
        self._initialize_llm()

    def _initialize_llm(self) -> None:
        """Initialize the LangChain Ollama LLM instance.

        Raises:
            OllamaConnectionError: If connection to Ollama fails
        """
        try:
            self._llm = OllamaLLM(
                base_url=self.config.ollama_base_url,
                model=self.config.model_name,
                temperature=self.config.temperature,
                num_predict=self.config.max_tokens,
            )
            logger.info(
                f"Initialized Ollama client with model: {self.config.model_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {e}")
            raise OllamaConnectionError(f"Could not connect to Ollama: {e}") from e

    def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt for the LLM

        Returns:
            The generated response from the LLM

        Raises:
            OllamaConnectionError: If the LLM is not properly initialized
            ModelNotFoundError: If the model is not available
        """
        if self._llm is None:
            raise OllamaConnectionError("LLM not initialized")

        try:
            logger.debug(f"Generating response for prompt: {prompt[:100]}...")
            response = self._llm.invoke(prompt)
            logger.debug(f"Generated response: {response[:100]}...")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            if "model not found" in str(e).lower():
                raise ModelNotFoundError(
                    f"Model '{self.config.model_name}' not found. "
                    f"Make sure it's available in Ollama."
                ) from e
            raise OllamaConnectionError(f"Error generating response: {e}") from e

    def is_healthy(self) -> bool:
        """Check if the Ollama connection is healthy.

        Returns:
            True if the connection is healthy, False otherwise
        """
        try:
            if self._llm is None:
                return False
            # Simple health check with a minimal prompt
            self._llm.invoke("Hello")
            return True
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False

    def get_available_models(self) -> list[str]:
        """Get list of available models from Ollama.

        Returns:
            List of available model names

        Note:
            This is a placeholder implementation. In a real scenario,
            you would call Ollama's API to get the actual model list.
        """
        # This would require direct API calls to Ollama
        # For now, return common models
        return ["llama2", "mistral", "codellama", "neural-chat"]
