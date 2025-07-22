"""Tests for the configuration module."""

import pytest
from pydantic import ValidationError

from simple_chatbot.config import ChatbotConfig


class TestChatbotConfig:
    """Test cases for ChatbotConfig class."""

    def test_default_values(self) -> None:
        """Test that default values are set correctly."""
        config = ChatbotConfig()

        assert config.ollama_base_url == "http://localhost:11434"
        assert config.model_name == "llama2"
        assert config.temperature == 0.3
        assert config.max_tokens == 2000
        assert (
            config.system_prompt
            == "You are a helpful assistant. Respond in a friendly and informative manner."
        )
        assert config.conversation_memory_limit == 10

    def test_custom_values(self) -> None:
        """Test that custom values are set correctly."""
        config = ChatbotConfig(
            ollama_base_url="http://localhost:8080",
            model_name="mistral",
            temperature=0.5,
            max_tokens=1000,
            system_prompt="Custom prompt",
            conversation_memory_limit=20,
        )

        assert config.ollama_base_url == "http://localhost:8080"
        assert config.model_name == "mistral"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000
        assert config.system_prompt == "Custom prompt"
        assert config.conversation_memory_limit == 20

    def test_temperature_validation(self) -> None:
        """Test temperature validation."""
        # Valid temperatures
        ChatbotConfig(temperature=0.0)
        ChatbotConfig(temperature=1.0)
        ChatbotConfig(temperature=0.5)

        # Invalid temperatures
        with pytest.raises(ValidationError):
            ChatbotConfig(temperature=-0.1)

        with pytest.raises(ValidationError):
            ChatbotConfig(temperature=1.1)

    def test_max_tokens_validation(self) -> None:
        """Test max_tokens validation."""
        # Valid max_tokens
        ChatbotConfig(max_tokens=1)
        ChatbotConfig(max_tokens=1000)

        # Invalid max_tokens
        with pytest.raises(ValidationError):
            ChatbotConfig(max_tokens=0)

        with pytest.raises(ValidationError):
            ChatbotConfig(max_tokens=-1)

    def test_memory_limit_validation(self) -> None:
        """Test conversation_memory_limit validation."""
        # Valid memory limits
        ChatbotConfig(conversation_memory_limit=1)
        ChatbotConfig(conversation_memory_limit=100)

        # Invalid memory limits
        with pytest.raises(ValidationError):
            ChatbotConfig(conversation_memory_limit=0)

        with pytest.raises(ValidationError):
            ChatbotConfig(conversation_memory_limit=-1)

    def test_from_env_default_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test creating config from environment variables with defaults."""
        # Clear any existing environment variables
        env_vars = [
            "OLLAMA_BASE_URL",
            "OLLAMA_MODEL",
            "CHATBOT_TEMPERATURE",
            "CHATBOT_MAX_TOKENS",
            "CHATBOT_SYSTEM_PROMPT",
            "CONVERSATION_MEMORY_LIMIT",
        ]
        for var in env_vars:
            monkeypatch.delenv(var, raising=False)

        config = ChatbotConfig.from_env()

        assert config.ollama_base_url == "http://localhost:11434"
        assert config.model_name == "llama2"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.conversation_memory_limit == 10

    def test_from_env_custom_values(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test creating config from environment variables with custom values."""
        monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:8080")
        monkeypatch.setenv("OLLAMA_MODEL", "mistral")
        monkeypatch.setenv("CHATBOT_TEMPERATURE", "0.5")
        monkeypatch.setenv("CHATBOT_MAX_TOKENS", "1000")
        monkeypatch.setenv("CHATBOT_SYSTEM_PROMPT", "Custom system prompt")
        monkeypatch.setenv("CONVERSATION_MEMORY_LIMIT", "20")

        config = ChatbotConfig.from_env()

        assert config.ollama_base_url == "http://localhost:8080"
        assert config.model_name == "mistral"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000
        assert config.system_prompt == "Custom system prompt"
        assert config.conversation_memory_limit == 20
