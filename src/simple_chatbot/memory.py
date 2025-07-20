"""Memory module for conversation history management.

This module provides classes for managing conversation memory,
including message storage and retrieval with configurable limits.
"""

import logging
from collections import deque

from simple_chatbot.llm_client import ChatMessage

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manages conversation history with configurable memory limits.

    This class stores conversation messages and provides efficient
    access to recent conversation history.

    Attributes:
        memory_limit: Maximum number of message pairs to store
        messages: Deque containing conversation messages
    """

    def __init__(self, memory_limit: int = 10) -> None:
        """Initialize the conversation memory.

        Args:
            memory_limit: Maximum number of message pairs to keep in memory
        """
        self.memory_limit = memory_limit
        self._messages: deque[ChatMessage] = deque(
            maxlen=memory_limit * 2
        )  # *2 for user+assistant pairs
        logger.info(f"Initialized conversation memory with limit: {memory_limit}")

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation memory.

        Args:
            role: The role of the message sender (user, assistant, system)
            content: The content of the message
        """
        message = ChatMessage(role=role, content=content)
        self._messages.append(message)
        logger.debug(f"Added {role} message to memory")

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation memory.

        Args:
            content: The user's message content
        """
        self.add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation memory.

        Args:
            content: The assistant's message content
        """
        self.add_message("assistant", content)

    def get_messages(self) -> list[ChatMessage]:
        """Get all messages in the conversation memory.

        Returns:
            List of ChatMessage objects in chronological order
        """
        return list(self._messages)

    def get_recent_messages(self, count: int | None = None) -> list[ChatMessage]:
        """Get recent messages from the conversation memory.

        Args:
            count: Number of recent messages to retrieve. If None, returns all.

        Returns:
            List of recent ChatMessage objects
        """
        if count is None:
            return self.get_messages()

        return list(self._messages)[-count:]

    def format_for_prompt(self, include_system: bool = True) -> str:
        """Format conversation history for use in LLM prompts.

        Args:
            include_system: Whether to include system messages

        Returns:
            Formatted conversation history as a string
        """
        formatted_messages = []

        for message in self._messages:
            if not include_system and message.role == "system":
                continue

            formatted_messages.append(f"{message.role.title()}: {message.content}")

        return "\n".join(formatted_messages)

    def clear(self) -> None:
        """Clear all messages from the conversation memory."""
        self._messages.clear()
        logger.info("Cleared conversation memory")

    def get_message_count(self) -> int:
        """Get the total number of messages in memory.

        Returns:
            Number of messages currently stored
        """
        return len(self._messages)

    def is_empty(self) -> bool:
        """Check if the conversation memory is empty.

        Returns:
            True if no messages are stored, False otherwise
        """
        return len(self._messages) == 0

    def get_conversation_summary(self) -> dict[str, int]:
        """Get a summary of the conversation statistics.

        Returns:
            Dictionary with conversation statistics
        """
        stats = {
            "total_messages": 0,
            "user_messages": 0,
            "assistant_messages": 0,
            "system_messages": 0,
        }

        for message in self._messages:
            stats["total_messages"] += 1
            stats[f"{message.role}_messages"] += 1

        return stats
