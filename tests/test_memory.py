"""Tests for the memory module."""

from simple_chatbot.memory import ConversationMemory


class TestConversationMemory:
    """Test cases for ConversationMemory class."""

    def test_initialization(self) -> None:
        """Test memory initialization."""
        memory = ConversationMemory(memory_limit=5)
        assert memory.memory_limit == 5
        assert memory.is_empty()
        assert memory.get_message_count() == 0

    def test_add_message(self) -> None:
        """Test adding messages to memory."""
        memory = ConversationMemory()

        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there!")

        assert not memory.is_empty()
        assert memory.get_message_count() == 2

        messages = memory.get_messages()
        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[0].content == "Hello"
        assert messages[1].role == "assistant"
        assert messages[1].content == "Hi there!"

    def test_add_user_message(self) -> None:
        """Test adding user messages."""
        memory = ConversationMemory()
        memory.add_user_message("Hello, bot!")

        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Hello, bot!"

    def test_add_assistant_message(self) -> None:
        """Test adding assistant messages."""
        memory = ConversationMemory()
        memory.add_assistant_message("Hello, human!")

        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "assistant"
        assert messages[0].content == "Hello, human!"

    def test_memory_limit(self) -> None:
        """Test that memory limit is respected."""
        memory = ConversationMemory(memory_limit=2)  # 2 pairs = 4 messages max

        # Add more messages than the limit
        for i in range(6):
            memory.add_user_message(f"User message {i}")
            memory.add_assistant_message(f"Assistant message {i}")

        # Should only keep the last 4 messages (2 pairs)
        messages = memory.get_messages()
        assert len(messages) == 4
        assert messages[0].content == "User message 4"
        assert messages[1].content == "Assistant message 4"
        assert messages[2].content == "User message 5"
        assert messages[3].content == "Assistant message 5"

    def test_get_recent_messages(self) -> None:
        """Test getting recent messages."""
        memory = ConversationMemory()

        for i in range(5):
            memory.add_user_message(f"Message {i}")

        # Get last 3 messages
        recent = memory.get_recent_messages(3)
        assert len(recent) == 3
        assert recent[0].content == "Message 2"
        assert recent[1].content == "Message 3"
        assert recent[2].content == "Message 4"

        # Get all messages
        all_messages = memory.get_recent_messages(None)
        assert len(all_messages) == 5

    def test_format_for_prompt(self) -> None:
        """Test formatting messages for prompts."""
        memory = ConversationMemory()

        memory.add_message("system", "You are helpful")
        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi there!")

        # With system messages
        formatted_with_system = memory.format_for_prompt(include_system=True)
        expected_with_system = (
            "System: You are helpful\nUser: Hello\nAssistant: Hi there!"
        )
        assert formatted_with_system == expected_with_system

        # Without system messages
        formatted_without_system = memory.format_for_prompt(include_system=False)
        expected_without_system = "User: Hello\nAssistant: Hi there!"
        assert formatted_without_system == expected_without_system

    def test_clear(self) -> None:
        """Test clearing memory."""
        memory = ConversationMemory()

        memory.add_user_message("Hello")
        memory.add_assistant_message("Hi")

        assert not memory.is_empty()

        memory.clear()

        assert memory.is_empty()
        assert memory.get_message_count() == 0

    def test_conversation_summary(self) -> None:
        """Test conversation statistics."""
        memory = ConversationMemory()

        memory.add_message("system", "System message")
        memory.add_user_message("User message 1")
        memory.add_assistant_message("Assistant message 1")
        memory.add_user_message("User message 2")

        stats = memory.get_conversation_summary()

        assert stats["total_messages"] == 4
        assert stats["system_messages"] == 1
        assert stats["user_messages"] == 2
        assert stats["assistant_messages"] == 1

    def test_empty_memory_format(self) -> None:
        """Test formatting empty memory."""
        memory = ConversationMemory()

        formatted = memory.format_for_prompt()
        assert formatted == ""
