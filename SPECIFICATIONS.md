# Simple Chatbot - Technical Specifications

## 📋 Project Overview

**Simple Chatbot** is a command-line application that implements a conversational chatbot using LangChain and Ollama. The project is designed for educational purposes and to demonstrate best practices in developing modern Python applications with local LLMs.

## 🎯 Objectives

- **Educational**: Demonstrate chatbot implementation using modern technologies
- **Modular**: Clean architecture with separation of concerns
- **User-friendly**: Intuitive CLI interface with special commands
- **Configurable**: Adjustable parameters for different use cases
- **Robust**: Complete error handling and validations

## 🏗️ Architecture

### Project Structure

```
simple-chatbot/
├── src/simple_chatbot/
│   ├── __init__.py          # Main module
│   ├── chatbot.py           # Core chatbot logic
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Centralized configuration
│   ├── llm_client.py        # Ollama client
│   └── memory.py            # Conversational memory management
├── tests/                   # Unit tests
├── pyproject.toml          # Project configuration
├── README.md               # User documentation
└── SPECIFICATIONS.md       # This file
```

### Main Components

#### 1. **SimpleChatbot** (`chatbot.py`)
- **Responsibility**: Conversation orchestration
- **Features**:
  - Conversation flow management
  - Integration with memory and LLM client
  - Prompt formatting
  - Conversation statistics
  - Health checks

#### 2. **CLI Interface** (`cli.py`)
- **Responsibility**: User interface
- **Features**:
  - Rich interface with panels and colors
  - Command history navigation (↑↓)
  - Special commands with `/` prefix
  - Keyboard shortcuts (Ctrl+L to clear)
  - User-friendly error handling

#### 3. **OllamaClient** (`llm_client.py`)
- **Responsibility**: Communication with Ollama
- **Features**:
  - Ollama connection via HTTP
  - Available model validation
  - Generation parameter configuration
  - Connection error handling

#### 4. **ConversationMemory** (`memory.py`)
- **Responsibility**: Conversational memory management
- **Features**:
  - Configurable message limit
  - Prompt formatting
  - Conversation statistics
  - History reset

#### 5. **ChatbotConfig** (`config.py`)
- **Responsibility**: Centralized configuration
- **Features**:
  - Model parameters (temperature, max_tokens)
  - Connection URLs
  - Memory limits
  - System prompt

## 🛠️ Technology Stack

### Core Dependencies
- **Python**: 3.10+ (modern type hints)
- **LangChain**: Framework for LLM applications
- **LangChain-Ollama**: Specific Ollama integration
- **Pydantic**: Data validation and configuration

### CLI & UX
- **Rich**: Advanced terminal interface
- **Click**: CLI framework
- **prompt-toolkit**: Advanced input with history

### Development Tools
- **uv**: Dependency and virtual environment management
- **ruff**: Code linting and formatting
- **pytest**: Testing framework
- **mypy**: Static type checking

## 📋 Implemented Features

### Core Features
- ✅ **Basic conversation**: Interactive chat with local LLMs
- ✅ **Conversational memory**: Maintains conversation context
- ✅ **Flexible configuration**: Multiple adjustable parameters
- ✅ **Multiple models**: Support for any Ollama model

### Special Commands
- ✅ `/quit`, `/exit`, `/bye`: End conversation
- ✅ `/reset`: Clear conversation history
- ✅ `/stats`: Show conversation statistics
- ✅ `/history`: View complete history
- ✅ `/help`: Show help

### UX Features
- ✅ **Rich Interface**: Colored panels and improved formatting
- ✅ **Command history**: ↑↓ navigation
- ✅ **Shortcuts**: Ctrl+L to clear screen
- ✅ **Loading indicators**: Spinners during processing
- ✅ **Error handling**: Informative messages

### CLI Options
- ✅ `--model`: Ollama model selection
- ✅ `--temperature`: Creativity control (0.0-1.0)
- ✅ `--max-tokens`: Response token limit
- ✅ `--long-responses`: Long response mode (4000 tokens)
- ✅ `--ollama-url`: Custom Ollama URL
- ✅ `--memory-limit`: Message limit in memory
- ✅ `--debug`: Detailed logging

## 🔧 Configuration

### Environment Variables
```bash
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama2
TEMPERATURE=0.7
MAX_TOKENS=2000
CONVERSATION_MEMORY_LIMIT=10
```

### Programmatic Configuration
```python
config = ChatbotConfig(
    ollama_base_url="http://localhost:11434",
    model_name="mistral",
    temperature=0.5,
    max_tokens=3000,
    conversation_memory_limit=15
)
```

## 🚀 Installation and Usage

### Local Installation
```bash
# Clone and enter directory
git clone <repo-url>
cd simple-chatbot

# Install dependencies
uv sync

# Verify installation
uv run chatbot --help
```

### Global Installation
```bash
# Option 1: pipx (recommended)
pipx install .

# Option 2: uv tool
uv tool install .
```

### Basic Usage
```bash
# Run with default configuration
uv run chatbot

# Use specific model
uv run chatbot --model mistral --temperature 0.5

# Debug mode for development
uv run chatbot --debug
```

## 🧪 Testing

### Test Structure
```
tests/
├── test_chatbot.py     # Main component tests
├── test_config.py      # Configuration tests
└── test_memory.py      # Conversational memory tests
```

### Running Tests
```bash
# Complete tests
uv run pytest

# With coverage
uv run pytest --cov=src/simple_chatbot
```

## 📊 Metrics and Statistics

The chatbot provides the following metrics:
- **Total messages**: Total number of exchanged messages
- **User messages**: User messages
- **Bot messages**: Bot responses
- **Average message length**: Average message length
- **Conversation duration**: Session duration

## 🔐 Security and Considerations

### Security
- **Local data**: All data remains on the local system
- **No telemetry**: No data sent to external services
- **Input validation**: Basic input sanitization

### Limitations
- **Ollama dependency**: Requires Ollama running locally
- **Volatile memory**: History is lost when closing the application
- **No persistence**: No permanent conversation storage

## 📈 Possible Future Improvements

### Features
- [ ] **Persistence**: Save conversations to database
- [ ] **Multiple sessions**: Manage multiple conversations
- [ ] **Export/Import**: Export conversations to files
- [ ] **File configuration**: TOML/YAML configuration files
- [ ] **Plugins**: Extension system

### Technical
- [ ] **Async/await**: Improve concurrency
- [ ] **Streaming**: Real-time responses
- [ ] **Rate limiting**: Usage limits
- [ ] **Metrics**: Advanced metrics with Prometheus
- [ ] **Web UI**: Optional web interface

## 🤝 Contributions

### Code Standards
- **Type hints**: Mandatory in all functions
- **Docstrings**: Google style for all public functions
- **Ruff**: Automatic linting and formatting
- **Tests**: Minimum 90% coverage

### Development Process
1. **Fork** the repository
2. **Branch** for new feature
3. **Tests** for any change
4. **PR** with detailed description

## 📝 Versioning

The project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Compatible new features
- **PATCH**: Compatible bug fixes

**Current version**: 0.1.0

---

## 📄 License

This project is designed for educational and demonstration purposes.

**Author**: Juanje Ojeda (juanje@redhat.com)
**Date**: July 2025