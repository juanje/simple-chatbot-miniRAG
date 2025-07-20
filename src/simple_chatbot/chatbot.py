"""Main chatbot implementation using LangChain and Ollama.

This module contains the SimpleChatbot class that orchestrates
the conversation flow, memory management, and LLM interactions.
"""

import logging

from simple_chatbot.config import ChatbotConfig
from simple_chatbot.llm_client import (
    ModelNotFoundError,
    OllamaClient,
    OllamaConnectionError,
)
from simple_chatbot.memory import ConversationMemory

logger = logging.getLogger(__name__)


class SimpleChatbot:
    """A simple chatbot using LangChain and Ollama.

    This class orchestrates the conversation flow by managing
    memory, formatting prompts, and interfacing with the LLM.

    Attributes:
        config: Configuration object with chatbot settings
        llm_client: Client for interacting with Ollama
        memory: Conversation memory manager
    """

    def __init__(self, config: ChatbotConfig | None = None) -> None:
        """Initialize the SimpleChatbot.

        Args:
            config: Configuration object. If None, creates from environment variables.

        Raises:
            OllamaConnectionError: If connection to Ollama fails
        """
        self.config = config or ChatbotConfig.from_env()
        self.llm_client = OllamaClient(self.config)
        self.memory = ConversationMemory(self.config.conversation_memory_limit)

        # Add system prompt to memory
        if self.config.system_prompt:
            self.memory.add_message("system", self.config.system_prompt)

        logger.info("SimpleChatbot initialized successfully")

    def _format_prompt(self, user_input: str) -> str:
        """Format the prompt with conversation history and user input.

        Args:
            user_input: The user's input message

        Returns:
            Formatted prompt string for the LLM
        """
        # Get conversation history
        conversation_history = self.memory.format_for_prompt(include_system=True)

        # Append current user input
        if conversation_history:
            full_prompt = f"{conversation_history}\nUser: {user_input}\nAssistant:"
        else:
            full_prompt = f"User: {user_input}\nAssistant:"

        return full_prompt

    def chat(self, user_input: str) -> str:
        """Process user input and generate a response.

        Args:
            user_input: The user's message

        Returns:
            The chatbot's response

        Raises:
            OllamaConnectionError: If there's an issue with the LLM connection
            ModelNotFoundError: If the specified model is not available
        """
        if not user_input.strip():
            return "I didn't receive any input. Could you please say something?"

        logger.info(f"Processing user input: {user_input[:50]}...")

        # Add user message to memory
        self.memory.add_user_message(user_input)

        # Format prompt with conversation history
        formatted_prompt = self._format_prompt(user_input)

        try:
            # Generate response from LLM
            response = self.llm_client.generate_response(formatted_prompt)

            # Clean up response (remove any role prefixes if present)
            cleaned_response = self._clean_response(response)

            # Add assistant response to memory
            self.memory.add_assistant_message(cleaned_response)

            logger.info(f"Generated response: {cleaned_response[:50]}...")
            return cleaned_response

        except (OllamaConnectionError, ModelNotFoundError) as e:
            logger.error(f"Error during chat: {e}")
            # Don't add the error to memory, but return a user-friendly message
            return f"I'm sorry, I encountered an error: {e}"

    def _clean_response(self, response: str) -> str:
        """Clean the LLM response by removing role prefixes and extra whitespace.

        Args:
            response: Raw response from the LLM

        Returns:
            Cleaned response string
        """
        # Remove common role prefixes that might appear in responses
        prefixes_to_remove = ["Assistant:", "assistant:", "AI:", "ai:", "Bot:", "bot:"]

        cleaned = response.strip()
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix) :].strip()
                break

        return cleaned

    def reset_conversation(self) -> None:
        """Reset the conversation by clearing memory and re-adding system prompt."""
        self.memory.clear()

        # Re-add system prompt
        if self.config.system_prompt:
            self.memory.add_message("system", self.config.system_prompt)

        logger.info("Conversation reset")

    def get_conversation_stats(self) -> dict:
        """Get statistics about the current conversation.

        Returns:
            Dictionary with conversation statistics
        """
        return self.memory.get_conversation_summary()

    def is_healthy(self) -> bool:
        """Check if the chatbot is healthy and ready to respond.

        Returns:
            True if the chatbot is healthy, False otherwise
        """
        return self.llm_client.is_healthy()

    def get_conversation_history(self, format_for_display: bool = True) -> str:
        """Get the conversation history.

        Args:
            format_for_display: Whether to format for user-friendly display

        Returns:
            Formatted conversation history
        """
        if format_for_display:
            messages = self.memory.get_messages()
            formatted_history = []

            for message in messages:
                if message.role == "system":
                    continue  # Skip system messages in display
                elif message.role == "user":
                    formatted_history.append(f"You: {message.content}")
                elif message.role == "assistant":
                    formatted_history.append(f"Bot: {message.content}")

            return (
                "\n".join(formatted_history)
                if formatted_history
                else "No conversation history yet."
            )
        else:
            return self.memory.format_for_prompt(include_system=False)
