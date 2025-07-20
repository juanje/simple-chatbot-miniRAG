# Simple Chatbot

A simple chatbot implementation using **LangChain** and **Ollama** for learning purposes. This project demonstrates how to build a conversational AI application with local LLM models.

## Features

- 🤖 **Local LLM Integration**: Uses Ollama for running models locally
- 💬 **Conversation Memory**: Maintains conversation history with configurable limits
- ⚙️ **Configurable**: Easy configuration via environment variables or direct parameters
- 🎨 **Beautiful CLI**: Rich terminal interface with colors and formatting
- 🧪 **Well Tested**: Comprehensive test suite with >90% coverage
- 📝 **Type Safe**: Full type annotations with mypy support
- 🛠️ **Modern Python**: Built with Python 3.10+ and modern tools

## Prerequisites

- **Python 3.10+**
- **Ollama** installed and running locally
- At least one Ollama model downloaded (e.g., `llama2`, `mistral`)

### Installing Ollama

1. Install Ollama from [https://ollama.ai](https://ollama.ai)
2. Start the Ollama service:
   ```bash
   ollama serve
   ```
3. Download a model:
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd simple-chatbot
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Install uv if you haven't already
   pip install uv
   
   # Create virtual environment
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies:**
   ```bash
   # Install project dependencies
   uv pip install -e .
   
   # Install development dependencies (optional)
   uv pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   uv run chatbot --help
   ```

## Usage

### Basic Usage

Start the chatbot with default settings:

```bash
uv run chatbot
```

### Custom Model and Settings

```bash
# Standard usage with custom model
uv run chatbot --model mistral --temperature 0.5 --max-tokens 3000

# For detailed analysis and long responses
uv run chatbot --model mistral --long-responses

# For debugging connection issues
uv run chatbot --debug
```

### All Available Options

```bash
uv run chatbot --help
```

Available options:
- `--model`: Ollama model to use (default: llama2)
- `--temperature`: Temperature for text generation (0.0 to 1.0, default: 0.7)
- `--max-tokens`: Maximum tokens to generate (default: 2000)
- `--long-responses`: Allow very long responses (sets max-tokens to 4000)
- `--ollama-url`: Ollama base URL (default: http://localhost:11434)
- `--memory-limit`: Conversation memory limit (default: 10 message pairs)
- `--debug`: Enable debug logging

### Interactive Commands

Once the chatbot is running, you can use these commands (all commands require a `/` prefix):

- `/quit`, `/exit`, or `/bye`: End the conversation
- `/reset`: Clear conversation history
- `/stats`: Show conversation statistics
- `/history`: Display conversation history
- `/help`: Show help message

### Navigation Features

- **↑↓ Arrow Keys**: Navigate through command history
- **Ctrl+L**: Clear screen
- **Ctrl+C**: Interrupt current operation
- **Ctrl+A/E**: Move to beginning/end of line

**Note:** Commands require a `/` prefix to avoid accidental activation during normal conversation.

### Environment Variables

You can configure the chatbot using environment variables:

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="mistral"
export CHATBOT_TEMPERATURE="0.5"
export CHATBOT_MAX_TOKENS="3000"
export CHATBOT_SYSTEM_PROMPT="You are a helpful coding assistant."
export CONVERSATION_MEMORY_LIMIT="20"
```

Create a `.env` file for persistent configuration:

```env
OLLAMA_MODEL=mistral
CHATBOT_TEMPERATURE=0.5
CHATBOT_SYSTEM_PROMPT=You are a helpful and knowledgeable assistant.
```

## Project Structure

```
simple-chatbot/
├── src/simple_chatbot/          # Main package
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration management
│   ├── llm_client.py           # Ollama client wrapper
│   ├── memory.py               # Conversation memory
│   ├── chatbot.py              # Main chatbot logic
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
│   ├── test_config.py          # Configuration tests
│   ├── test_memory.py          # Memory tests
│   └── test_chatbot.py         # Chatbot tests
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Development

### Setting Up Development Environment

1. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment (if not already created)
   uv venv
   
   # Activate virtual environment
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate   # On Windows
   ```

2. **Install development dependencies:**
   ```bash
   uv pip install -e ".[dev]"
   ```

3. **Run tests:**
   ```bash
   uv run pytest
   ```

4. **Run tests with coverage:**
   ```bash
   uv run pytest --cov=simple_chatbot --cov-report=html
   ```

5. **Code formatting and linting:**
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

6. **Type checking:**
   ```bash
   uv run mypy src/simple_chatbot
   ```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_chatbot.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=simple_chatbot
```

## Programming and Learning Examples

### Basic Programmatic Usage

```python
from simple_chatbot import SimpleChatbot, ChatbotConfig

# Create custom configuration
config = ChatbotConfig(
    model_name="mistral",
    temperature=0.5,
    system_prompt="You are a helpful coding assistant."
)

# Initialize chatbot
chatbot = SimpleChatbot(config)

# Have a conversation
response = chatbot.chat("Hello! Can you help me with Python?")
print(response)

response = chatbot.chat("What are list comprehensions?")
print(response)

# Check conversation stats
stats = chatbot.get_conversation_stats()
print(f"Total messages: {stats['total_messages']}")
```

### Custom Memory Management

```python
from simple_chatbot.memory import ConversationMemory

# Create memory with custom limit
memory = ConversationMemory(memory_limit=5)

# Add messages
memory.add_user_message("Hello")
memory.add_assistant_message("Hi there!")

# Get formatted conversation
history = memory.format_for_prompt()
print(history)
```

### Error Handling

```python
from simple_chatbot import SimpleChatbot
from simple_chatbot.llm_client import OllamaConnectionError, ModelNotFoundError

try:
    chatbot = SimpleChatbot()
    response = chatbot.chat("Hello")
except OllamaConnectionError as e:
    print(f"Connection error: {e}")
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
```

## Architecture

The project follows a modular architecture:

1. **Configuration Layer** (`config.py`): Handles all configuration with validation
2. **LLM Client Layer** (`llm_client.py`): Abstracts Ollama integration
3. **Memory Layer** (`memory.py`): Manages conversation history
4. **Core Logic** (`chatbot.py`): Orchestrates the conversation flow
5. **Interface Layer** (`cli.py`): Provides user interaction

## Quick Reference

### Essential Commands

```bash
# Setup (one time)
uv venv                              # Create virtual environment
source .venv/bin/activate            # Activate virtual environment (macOS/Linux)
# .venv\Scripts\activate             # Activate virtual environment (Windows)
uv pip install -e ".[dev]"          # Install project with dev dependencies

# Daily development
uv run pytest tests/ -v             # Run tests with verbose output
uv run pytest --cov=simple_chatbot  # Run tests with coverage
uv run chatbot                       # Run the chatbot (now with history!)
uv run chatbot --long-responses      # Run with extended responses
uv run ruff check .                  # Check code formatting
uv run ruff format .                 # Format code
uv run mypy src/simple_chatbot       # Type checking
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code is formatted
6. Submit a pull request

## Development Methodology

This project was developed using **"vibe coding"** methodology with AI assistance:

### 🤖 AI-Assisted Development
- **IDE**: [Cursor](https://cursor.sh/) - AI-powered code editor
- **LLM Model**: Claude-4-Sonnet (Anthropic)
- **Human Developer**: Juanje Ojeda (juanje@redhat.com)

### 🔄 Development Process
1. **Specification**: Initial requirements and technical specifications defined by the human developer
2. **AI Generation**: Core code structure and implementation generated by Claude-4-Sonnet
3. **Human Review**: Code review, architectural decisions, and quality assessment
4. **Manual Testing**: Real-world testing and validation by the human developer
5. **Iterative Refinement**: Continuous feedback loop between human insights and AI capabilities
6. **Final Polish**: Manual adjustments and optimizations

### 🎯 Methodology Benefits
- **Rapid Prototyping**: Fast initial implementation and iteration cycles
- **Code Quality**: AI ensures consistent coding standards and best practices
- **Human Oversight**: Critical thinking and domain expertise guide the development
- **Learning Tool**: Demonstrates practical AI-human collaboration in software development

### 📝 Transparency
This approach represents a modern software development workflow where AI tools augment human creativity and expertise rather than replace it. The final code quality results from the synergy between AI capabilities and human judgment.

## Troubleshooting

### Common Issues

**"Connection refused" error:**
- Ensure Ollama is running: `ollama serve`
- Check if the service is accessible: `curl http://localhost:11434`

**"Model not found" error:**
- Download the model: `ollama pull llama2`
- List available models: `ollama list`

**Performance issues:**
- Reduce max_tokens for faster responses
- Use smaller models (e.g., `orca-mini` instead of `llama2`)
- Adjust temperature for more focused responses

**Incomplete or cut-off responses:**
- Increase max_tokens: `chatbot --max-tokens 4000`
- Use long responses flag: `chatbot --long-responses`
- Set environment variable: `export CHATBOT_MAX_TOKENS=4000`

## License

This project is intended for educational purposes. Please refer to the licenses of the underlying dependencies (LangChain, Ollama) for their respective terms.

## Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Modern Python Packaging](https://packaging.python.org/) 