"""Main chatbot implementation using LangChain and Ollama.

This module contains the SimpleChatbot class that orchestrates
the conversation flow, memory management, LLM interactions, and RAG functionality.
"""

import logging
from pathlib import Path

from simple_chatbot.config import ChatbotConfig
from simple_chatbot.knowledge_base import SimpleKnowledgeBase
from simple_chatbot.llm_client import (
    ModelNotFoundError,
    OllamaClient,
    OllamaConnectionError,
)
from simple_chatbot.memory import ConversationMemory

logger = logging.getLogger(__name__)


class SimpleChatbot:
    """A simple chatbot using LangChain and Ollama with RAG capabilities.

    This class orchestrates the conversation flow by managing
    memory, formatting prompts, interfacing with the LLM, and providing
    RAG (Retrieval-Augmented Generation) functionality.

    Attributes:
        config: Configuration object with chatbot settings
        llm_client: Client for interacting with Ollama
        memory: Conversation memory manager
        knowledge_base: Knowledge base for RAG functionality
    """

    def __init__(self, config: ChatbotConfig | None = None) -> None:
        """Initialize the SimpleChatbot.

        Args:
            config: Configuration object. If None, creates from environment variables.

        Raises:
            OllamaConnectionError: If connection to Ollama fails
            FileNotFoundError: If RAG knowledge file doesn't exist and RAG is enabled
        """
        self.config = config or ChatbotConfig.from_env()
        self.llm_client = OllamaClient(self.config)
        self.memory = ConversationMemory(self.config.conversation_memory_limit)

        # Initialize knowledge base for RAG
        self.knowledge_base = self._initialize_knowledge_base()

        # Add system prompt to memory
        if self.config.system_prompt:
            self.memory.add_message("system", self.config.system_prompt)

        logger.info("SimpleChatbot initialized successfully")

    def _initialize_knowledge_base(self) -> SimpleKnowledgeBase | None:
        """Initialize the knowledge base for RAG functionality.

        Returns:
            SimpleKnowledgeBase instance if enabled and file exists, None otherwise

        Raises:
            FileNotFoundError: If RAG is enabled but knowledge file doesn't exist
        """
        if not self.config.rag_enabled:
            logger.info("RAG functionality is disabled")
            return SimpleKnowledgeBase(
                knowledge_file=self.config.knowledge_file, enabled=False
            )

        knowledge_path = Path(self.config.knowledge_file)
        if not knowledge_path.exists():
            # Create default knowledge file if it doesn't exist
            knowledge_path.parent.mkdir(parents=True, exist_ok=True)
            default_knowledge = {
                "welcome": {
                    "keywords": ["hello", "hi", "welcome", "start"],
                    "content": "¡Bienvenido al chatbot con RAG! Puedo ayudarte con preguntas sobre programación, IA y tecnología.",
                    "category": "general"
                }
            }
            with open(knowledge_path, "w", encoding="utf-8") as f:
                import json
                json.dump(default_knowledge, f, ensure_ascii=False, indent=2)
            logger.info(f"Created default knowledge file at {knowledge_path}")

        try:
            kb = SimpleKnowledgeBase(
                knowledge_file=self.config.knowledge_file,
                enabled=self.config.rag_enabled
            )
            logger.info(f"RAG enabled with {kb.get_stats()['total_entries']} knowledge entries")
            return kb
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
            # Return disabled knowledge base as fallback
            return SimpleKnowledgeBase(
                knowledge_file=self.config.knowledge_file, enabled=False
            )

    def _format_prompt(self, user_input: str) -> str:
        """Format the prompt with conversation history, RAG context, and user input.

        Args:
            user_input: The user's input message

        Returns:
            Formatted prompt string for the LLM
        """
        # Get conversation history
        conversation_history = self.memory.format_for_prompt(include_system=True)

        # Get RAG context if enabled
        rag_context = self._get_rag_context(user_input)

        # Build the prompt
        prompt_parts = []
        
        # Add conversation history
        if conversation_history:
            prompt_parts.append(conversation_history)

        # Add RAG context if available
        if rag_context:
            prompt_parts.append(rag_context)

        # Add current user input
        prompt_parts.append(f"User: {user_input}")
        prompt_parts.append("Assistant:")

        return "\n".join(prompt_parts)

    def _get_rag_context(self, user_input: str) -> str:
        """Retrieve relevant context from the knowledge base.

        Args:
            user_input: The user's input message

        Returns:
            Formatted RAG context string, empty if no relevant content found
        """
        if not self.knowledge_base or not self.knowledge_base.enabled:
            return ""

        try:
            # Search for relevant knowledge
            results = self.knowledge_base.search(
                query=user_input,
                max_results=self.config.rag_max_results,
                min_relevance_score=self.config.rag_min_relevance,
            )

            if results:
                logger.debug(f"Found {len(results)} relevant knowledge entries")
                return self.knowledge_base.format_context(results)
            else:
                logger.debug("No relevant knowledge found for query")
                return ""

        except Exception as e:
            logger.error(f"Error during RAG retrieval: {e}")
            return ""

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
        """Get statistics about the current conversation and knowledge base.

        Returns:
            Dictionary with conversation and RAG statistics
        """
        stats = self.memory.get_conversation_summary()
        
        # Add RAG statistics
        if self.knowledge_base:
            kb_stats = self.knowledge_base.get_stats()
            stats.update({
                "rag_enabled": kb_stats.get("enabled", False),
                "knowledge_entries": kb_stats.get("total_entries", 0),
                "knowledge_categories": kb_stats.get("total_categories", 0),
            })
        else:
            stats.update({
                "rag_enabled": False,
                "knowledge_entries": 0,
                "knowledge_categories": 0,
            })
        
        return stats

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

    def search_knowledge(self, query: str) -> list:
        """Search the knowledge base for relevant information.

        Args:
            query: Search query

        Returns:
            List of search results
        """
        if not self.knowledge_base or not self.knowledge_base.enabled:
            return []

        return self.knowledge_base.search(
            query=query,
            max_results=10,  # More results for manual search
            min_relevance_score=0.05,  # Lower threshold for manual search
        )

    def get_knowledge_stats(self) -> dict:
        """Get knowledge base statistics.

        Returns:
            Dictionary with knowledge base statistics
        """
        if not self.knowledge_base:
            return {"enabled": False}
        
        return self.knowledge_base.get_stats()

    def get_knowledge_categories(self) -> list[str]:
        """Get available knowledge categories.

        Returns:
            List of category names
        """
        if not self.knowledge_base or not self.knowledge_base.enabled:
            return []
        
        return self.knowledge_base.get_categories()

    def reload_knowledge(self) -> bool:
        """Reload the knowledge base from file.

        Returns:
            True if reload was successful, False otherwise
        """
        if not self.knowledge_base:
            return False

        try:
            self.knowledge_base.reload()
            logger.info("Knowledge base reloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to reload knowledge base: {e}")
            return False
