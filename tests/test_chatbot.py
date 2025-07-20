"""Tests for the main chatbot module."""

from simple_chatbot.chatbot import SimpleChatbot
from simple_chatbot.config import ChatbotConfig
from simple_chatbot.llm_client import OllamaConnectionError, ModelNotFoundError


class TestSimpleChatbot:
    """Test cases for SimpleChatbot class."""

    def test_initialization(self, mocker) -> None:
        """Test chatbot initialization."""
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        config = ChatbotConfig(system_prompt="Test system prompt")

        chatbot = SimpleChatbot(config)

        assert chatbot.config == config
        assert mock_ollama_client.called
        assert not chatbot.memory.is_empty()  # Should have system prompt

        # Check system prompt was added
        messages = chatbot.memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "system"
        assert messages[0].content == "Test system prompt"

    def test_initialization_from_env(self, mocker) -> None:
        """Test chatbot initialization from environment."""
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        chatbot = SimpleChatbot()

        assert chatbot.config is not None
        assert mock_ollama_client.called

    def test_chat_basic(self, mocker) -> None:
        """Test basic chat functionality."""
        mock_client = mocker.Mock()
        mock_client.generate_response.return_value = "Hello! How can I help you?"
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()
        response = chatbot.chat("Hello")

        assert response == "Hello! How can I help you?"
        assert mock_client.generate_response.called

        # Check messages were added to memory
        messages = chatbot.memory.get_messages()
        # Should have system prompt + user message + assistant message
        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        assert len(user_messages) == 1
        assert len(assistant_messages) == 1
        assert user_messages[0].content == "Hello"
        assert assistant_messages[0].content == "Hello! How can I help you?"

    def test_chat_empty_input(self, mocker) -> None:
        """Test chat with empty input."""
        mocker.patch("simple_chatbot.chatbot.OllamaClient")
        chatbot = SimpleChatbot()

        response = chatbot.chat("")
        assert "didn't receive any input" in response

        response = chatbot.chat("   ")
        assert "didn't receive any input" in response

    def test_chat_with_conversation_history(self, mocker) -> None:
        """Test chat with conversation history."""
        mock_client = mocker.Mock()
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()

        # First exchange
        mock_client.generate_response.return_value = "Hi there!"
        chatbot.chat("Hello")

        # Second exchange
        mock_client.generate_response.return_value = "I'm doing well, thanks!"
        chatbot.chat("How are you?")

        # Check that the prompt includes conversation history
        call_args = mock_client.generate_response.call_args_list
        assert len(call_args) == 2

        # Second call should include the first exchange in the prompt
        second_prompt = call_args[1][0][0]
        assert "Hello" in second_prompt
        assert "Hi there!" in second_prompt
        assert "How are you?" in second_prompt

    def test_clean_response(self, mocker) -> None:
        """Test response cleaning functionality."""
        mock_client = mocker.Mock()
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()

        # Test cleaning various prefixes
        test_cases = [
            ("Assistant: Hello there!", "Hello there!"),
            ("assistant: How can I help?", "How can I help?"),
            ("AI: I'm here to assist.", "I'm here to assist."),
            ("Bot: Welcome!", "Welcome!"),
            ("Regular response", "Regular response"),
        ]

        for raw_response, expected_clean in test_cases:
            mock_client.generate_response.return_value = raw_response
            response = chatbot.chat("Test")
            assert response == expected_clean

    def test_reset_conversation(self, mocker) -> None:
        """Test conversation reset functionality."""
        # Setup mock before creating chatbot
        mock_client = mocker.Mock()
        mock_client.generate_response.return_value = "Response"
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        config = ChatbotConfig(system_prompt="Test system")
        chatbot = SimpleChatbot(config)

        chatbot.chat("Hello")

        # Should have system + user + assistant messages
        assert chatbot.memory.get_message_count() == 3

        # Reset conversation
        chatbot.reset_conversation()

        # Should only have system message
        messages = chatbot.memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "system"
        assert messages[0].content == "Test system"

    def test_conversation_stats(self, mocker) -> None:
        """Test conversation statistics."""
        mock_client = mocker.Mock()
        mock_client.generate_response.return_value = "Response"
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()
        chatbot.chat("Hello")

        stats = chatbot.get_conversation_stats()

        assert "total_messages" in stats
        assert "user_messages" in stats
        assert "assistant_messages" in stats
        assert stats["user_messages"] >= 1
        assert stats["assistant_messages"] >= 1

    def test_is_healthy(self, mocker) -> None:
        """Test health check."""
        mock_client = mocker.Mock()
        mock_client.is_healthy.return_value = True
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()

        assert chatbot.is_healthy() is True
        assert mock_client.is_healthy.called

    def test_get_conversation_history(self, mocker) -> None:
        """Test getting conversation history."""
        mock_client = mocker.Mock()
        mock_client.generate_response.return_value = "Hi there!"
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()
        chatbot.chat("Hello")

        # Get formatted history
        history = chatbot.get_conversation_history(format_for_display=True)
        assert "You: Hello" in history
        assert "Bot: Hi there!" in history
        assert "System:" not in history  # System messages should be excluded

        # Get raw history
        raw_history = chatbot.get_conversation_history(format_for_display=False)
        assert isinstance(raw_history, str)

    def test_chat_connection_error(self, mocker) -> None:
        """Test chat with connection error."""
        mock_client = mocker.Mock()
        mock_client.generate_response.side_effect = OllamaConnectionError(
            "Connection failed"
        )
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()
        response = chatbot.chat("Hello")

        assert "I'm sorry, I encountered an error" in response
        assert "Connection failed" in response

    def test_chat_model_not_found_error(self, mocker) -> None:
        """Test chat with model not found error."""
        mock_client = mocker.Mock()
        mock_client.generate_response.side_effect = ModelNotFoundError(
            "Model not found"
        )
        mock_ollama_client = mocker.patch("simple_chatbot.chatbot.OllamaClient")
        mock_ollama_client.return_value = mock_client

        chatbot = SimpleChatbot()
        response = chatbot.chat("Hello")

        assert "I'm sorry, I encountered an error" in response
        assert "Model not found" in response
