# Simple Chatbot with RAG

An educational extension of the [Simple Chatbot](https://github.com/juanje/simple-chatbot) project that demonstrates **RAG (Retrieval-Augmented Generation)** implementation for learning purposes.

> **📚 For basic chatbot functionality**, refer to the [original project](https://github.com/juanje/simple-chatbot). This repository focuses specifically on **adding RAG capabilities** to enhance responses with relevant knowledge retrieval.

## 🎯 What's New: RAG Features

This project extends the base chatbot with:

- 📖 **Simple RAG Implementation**: JSON-based knowledge base with keyword matching
- 🔍 **Knowledge Retrieval**: Automatic context injection based on user queries  
- 🎭 **Fictional Universe**: Custom knowledge base with original content (Aethelgard universe)
- 🧪 **Educational Focus**: Learn RAG concepts without complex vector databases
- 🛠️ **CLI Extensions**: New commands for knowledge exploration (`/search`, `/knowledge`)
- 📊 **RAG Analytics**: Statistics and insights into knowledge retrieval

## 🔬 RAG Learning Objectives

This implementation helps you understand:

- **How RAG works**: Retrieval + Augmentation + Generation pipeline
- **Context injection**: Adding relevant information to LLM prompts
- **Knowledge management**: Organizing and searching structured data
- **Simple vs Complex RAG**: Building foundations before advanced implementations
- **Testing RAG systems**: Ensuring retrieval quality and relevance

## Prerequisites

- **Python 3.10+**
- **Ollama** installed and running locally
- At least one Ollama model downloaded (e.g., `llama2`, `mistral`)

> **📋 For detailed Ollama setup**, see the [original project documentation](https://github.com/juanje/simple-chatbot#prerequisites).

## Installation

1. **Clone this repository:**
   ```bash
   git clone <this-repository-url>
   cd simple-chatbot-miniRAG
   ```

2. **Setup environment** (same as original project):
   ```bash
   pip install uv
   uv venv
   source .venv/bin/activate  # macOS/Linux
   uv pip install -e ".[dev]"
   ```

3. **Verify RAG functionality:**
   ```bash
   uv run chatbot --help  # Should show RAG options
   ```

## 🚀 RAG Usage Examples

### Testing RAG vs Non-RAG

**Without RAG** (baseline behavior):
```bash
uv run chatbot --no-rag
# Ask: "Who is Dr. Aris Thorne?"
# Result: Generic response or "I don't know"
```

**With RAG** (enhanced with knowledge):
```bash
uv run chatbot --debug
# Ask: "Who is Dr. Aris Thorne?" 
# Result: Detailed info about the xenobotanist from Aethelgard
```

### RAG-Specific Options

- `--no-rag`: Disable RAG functionality for comparison
- `--knowledge-file`: Custom knowledge base file (default: `data/knowledge.json`)
- `--debug`: See RAG retrieval in action

### New Interactive Commands

Inside the chatbot, try these RAG commands:
- `/knowledge` - View knowledge base statistics
- `/search <query>` - Search knowledge manually
- `/categories` - List available knowledge categories  
- `/reload` - Reload knowledge base from file

### Perfect RAG Test Queries

Try these questions to see RAG in action:
```
"Who is Dr. Aris Thorne?"
"What is Aethelgard?"
"Tell me about Operation Grasping Hand"
"How do Sylvans communicate?"
"What is Xylos crystal?"
```

## 🧠 How the RAG Implementation Works

### 1. Knowledge Base Structure

```json
{
  "character_aris_thorne": {
    "keywords": ["Aris Thorne", "aris", "thorne", "xenobotanist", "scientist"],
    "content": "Dr. Aris Thorne is the lead xenobotanist...",
    "category": "character"
  }
}
```

### 2. RAG Pipeline

1. **Query Analysis**: Extract keywords from user input
2. **Knowledge Retrieval**: Match keywords against knowledge base
3. **Context Injection**: Add relevant entries to LLM prompt
4. **Enhanced Generation**: LLM responds with retrieved context

### 3. Key Components Added

- `knowledge_base.py`: Core RAG functionality
- `data/knowledge.json`: Fictional universe knowledge
- RAG configuration in `config.py`
- CLI extensions for knowledge exploration

## 📚 Knowledge Base: Aethelgard Universe

This project includes a **fictional sci-fi universe** to ensure RAG testing:

- **Characters**: Dr. Aris Thorne (xenobotanist), Kaelen Vance (security chief)
- **Locations**: Aethelgard (exoplanet), Crystal Spire (Xylos monument)  
- **Species**: Sylvans (sentient plant aliens)
- **Events**: Bloom of Whispers (first contact), Operation Grasping Hand
- **Technology**: Xylos crystals, Bio-Signaling communication

> **Why fictional content?** Ensures the LLM has no prior knowledge, making RAG effects clearly visible.

## 🔍 Differences from Original Project

| Feature | Original Project | This Project (with RAG) |
|---------|-----------------|-------------------------|
| **Knowledge Source** | LLM training data only | LLM + Custom knowledge base |
| **Response Quality** | General knowledge | Enhanced with specific context |
| **Temperature Default** | 0.7 (creative) | 0.3 (more deterministic) |
| **CLI Commands** | Basic chat commands | + `/knowledge`, `/search`, `/categories` |
| **Configuration** | Basic LLM settings | + RAG settings (`--no-rag`, `--knowledge-file`) |
| **Testing Focus** | General chatbot behavior | RAG retrieval and relevance |
| **Knowledge Updates** | Static (training cutoff) | Dynamic (reload knowledge file) |

## ⚙️ RAG Configuration

New environment variables for RAG:

```bash
export RAG_ENABLED="true"                    # Enable/disable RAG
export RAG_KNOWLEDGE_FILE="data/knowledge.json"  # Knowledge file path
export RAG_MAX_RESULTS="3"                   # Max knowledge entries per query
export RAG_MIN_RELEVANCE="0.1"              # Minimum relevance threshold
```

## Project Structure

```
simple-chatbot-miniRAG/
├── src/simple_chatbot/          # Main package
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration (+ RAG settings)
│   ├── llm_client.py           # Ollama client wrapper
│   ├── memory.py               # Conversation memory
│   ├── chatbot.py              # Main chatbot logic (+ RAG integration)
│   ├── knowledge_base.py       # 🆕 RAG knowledge management
│   └── cli.py                  # CLI (+ RAG commands)
├── data/                       # 🆕 Knowledge base
│   └── knowledge.json          # 🆕 Aethelgard universe data
├── tests/                      # Test suite (updated for RAG)
│   ├── test_config.py          # Configuration tests
│   ├── test_memory.py          # Memory tests
│   ├── test_chatbot.py         # Chatbot tests (+ RAG tests)
│   └── test_knowledge_base.py  # 🆕 RAG functionality tests
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

**🆕 New files for RAG:**
- `knowledge_base.py`: Core RAG implementation
- `data/knowledge.json`: Fictional knowledge base
- `test_knowledge_base.py`: RAG testing suite

## 🧪 Testing RAG Functionality

### RAG-Specific Tests

```bash
# Test knowledge base functionality
uv run pytest tests/test_knowledge_base.py -v

# Test RAG integration in chatbot
uv run pytest tests/test_chatbot.py::TestSimpleChatbotRAG -v

# All tests (should be 60 passing)
uv run pytest tests/ -v
```

### Manual RAG Testing

```python
# Test knowledge retrieval directly
from simple_chatbot.knowledge_base import SimpleKnowledgeBase

kb = SimpleKnowledgeBase('data/knowledge.json')
results = kb.search("Who is Dr. Aris Thorne?")
print(f"Found {len(results)} results")
```

## 🔧 Development

> **🔗 For general development setup**, see the [original project](https://github.com/juanje/simple-chatbot#development).

**RAG-specific development:**

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Test knowledge base changes
uv run pytest tests/test_knowledge_base.py

# Test with custom knowledge file
uv run chatbot --knowledge-file my_custom_knowledge.json
```

## 💡 Learning Examples

### RAG Implementation Study

```python
from simple_chatbot import SimpleChatbot, ChatbotConfig
from simple_chatbot.knowledge_base import SimpleKnowledgeBase

# Compare responses with/without RAG
config_no_rag = ChatbotConfig(rag_enabled=False)
config_with_rag = ChatbotConfig(rag_enabled=True)

chatbot_baseline = SimpleChatbot(config_no_rag)
chatbot_enhanced = SimpleChatbot(config_with_rag)

query = "Who is Dr. Aris Thorne?"

# Baseline response (no RAG)
response1 = chatbot_baseline.chat(query)
print("Without RAG:", response1)

# Enhanced response (with RAG)
response2 = chatbot_enhanced.chat(query)
print("With RAG:", response2)
```

### Knowledge Base Exploration

```python
from simple_chatbot.knowledge_base import SimpleKnowledgeBase

# Load and explore knowledge
kb = SimpleKnowledgeBase('data/knowledge.json')

# Get statistics
stats = kb.get_stats()
print(f"Knowledge entries: {stats['total_entries']}")
print(f"Categories: {stats['categories']}")

# Search examples
results = kb.search("scientist xenobotanist")
for result in results:
    print(f"Found: {result.entry_id} (relevance: {result.relevance_score:.2f})")

# Format for LLM context
context = kb.format_context(results)
print("Context for LLM:", context)
```

> **📖 For basic chatbot examples**, see the [original project documentation](https://github.com/juanje/simple-chatbot#programming-and-learning-examples).

## 🏗️ RAG Architecture

The RAG implementation adds a **Knowledge Layer** to the original architecture:

1. **Configuration Layer** (`config.py`): Handles all configuration + RAG settings
2. **LLM Client Layer** (`llm_client.py`): Abstracts Ollama integration *(unchanged)*
3. **Memory Layer** (`memory.py`): Manages conversation history *(unchanged)*
4. **🆕 Knowledge Layer** (`knowledge_base.py`): RAG knowledge management
5. **Core Logic** (`chatbot.py`): Orchestrates conversation flow + RAG integration
6. **Interface Layer** (`cli.py`): Provides user interaction + knowledge commands

### RAG Data Flow

```
User Query → Keyword Extraction → Knowledge Search → Context Injection → LLM → Enhanced Response
```

> **🔗 For detailed base architecture**, see [original project](https://github.com/juanje/simple-chatbot#architecture).

## 🚀 Quick Reference

### RAG Testing Commands

```bash
# Setup
uv pip install -e ".[dev]"          # Install with development dependencies

# Compare RAG vs No-RAG
uv run chatbot --no-rag              # Baseline chatbot (original behavior)
uv run chatbot --debug               # RAG-enhanced with debug output

# Test specific RAG features
uv run chatbot                       # Normal RAG-enhanced chatbot
# Then try: /search Dr. Aris Thorne
# Then try: /knowledge
# Then try: /categories

# Development
uv run pytest tests/test_knowledge_base.py -v    # Test RAG functionality
uv run pytest tests/ -v                          # All tests (60 should pass)
```

### Perfect RAG Demo

1. **Start without RAG**: `uv run chatbot --no-rag`
2. **Ask**: "Who is Dr. Aris Thorne?"
3. **Note response**: Generic or "I don't know"
4. **Start with RAG**: `uv run chatbot --debug`  
5. **Ask same question**: Should get detailed information about the xenobotanist
6. **Observe debug**: Shows knowledge retrieval in action

## 🤝 Contributing

This project focuses on **educational RAG implementation**. Contributions welcome for:

- Additional knowledge base examples
- Improved keyword extraction algorithms  
- Better relevance scoring methods
- More comprehensive tests
- Documentation improvements

> **🔗 For contributing to the base chatbot**, see [original project](https://github.com/juanje/simple-chatbot).

## 🎓 Educational Goals

This project teaches RAG concepts through:

- **Simple Implementation**: No complex vector databases or embeddings
- **Clear Code Structure**: Easy to understand and modify
- **Comprehensive Testing**: Learn to test RAG systems properly
- **Real Comparisons**: See exactly what RAG adds vs baseline
- **Fictional Data**: Eliminate LLM prior knowledge confusion

### 🧠 RAG Concepts Demonstrated

- **Retrieval**: Keyword-based knowledge search
- **Augmentation**: Context injection into prompts  
- **Generation**: Enhanced LLM responses
- **Evaluation**: Relevance scoring and filtering
- **Integration**: Adding RAG to existing chat systems

## 📊 Project Metrics

- **60 tests** covering both original and RAG functionality
- **10 knowledge entries** in fictional universe
- **4 categories** of knowledge (character, location, lore, etc.)
- **5+ new CLI commands** for knowledge exploration
- **100% test coverage** for RAG components

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

## 🔧 Troubleshooting

### RAG-Specific Issues

**RAG not working (same responses with/without --no-rag):**
- Check knowledge file exists: `ls data/knowledge.json`
- Verify keywords match: Use `/search <query>` to test manually
- Enable debug: `--debug` to see retrieval logs

**No knowledge found:**
- Try `/knowledge` to see database stats
- Use `/categories` to see available topics
- Test with exact keywords from knowledge base

**Knowledge file errors:**
- Validate JSON format: `python -m json.tool data/knowledge.json`
- Check file permissions: `ls -la data/knowledge.json`

### General Issues
> **🔗 For Ollama and basic setup issues**, see [original project troubleshooting](https://github.com/juanje/simple-chatbot#troubleshooting).

## 📚 Learning Resources

### RAG and Information Retrieval
- [RAG Papers and Implementations](https://github.com/topics/retrieval-augmented-generation)
- [Information Retrieval Basics](https://en.wikipedia.org/wiki/Information_retrieval)
- [Vector Databases (for advanced RAG)](https://www.pinecone.io/learn/vector-database/)

### Original Project Resources
- [Base Chatbot Project](https://github.com/juanje/simple-chatbot)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)

## 📄 License

Educational project based on [Simple Chatbot](https://github.com/juanje/simple-chatbot). 
Licensed for learning and demonstration purposes. 