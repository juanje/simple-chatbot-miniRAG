# Simple Chatbot with RAG - Technical Specifications

## Project Overview

This document outlines the technical specifications for a **RAG (Retrieval-Augmented Generation) extension** of the [Simple Chatbot](https://github.com/juanje/simple-chatbot) project. This educational implementation demonstrates how to add knowledge retrieval capabilities to enhance chatbot responses with relevant context.

> **📚 For base chatbot specifications**, refer to the [original project documentation](https://github.com/juanje/simple-chatbot). This document focuses on **RAG-specific technical details** and implementation.

## RAG Enhancement Features

### 1. Knowledge Base Management
- **Storage Format**: JSON-based knowledge entries
- **Structure**: Keywords, content, categories, and metadata
- **Content**: Fictional Aethelgard universe for testing
- **Searchability**: Keyword-based retrieval system

### 2. Retrieval System
- **Query Processing**: Keyword extraction from user input
- **Relevance Scoring**: Simple ratio-based relevance calculation
- **Filtering**: Minimum relevance threshold configuration
- **Results Limiting**: Configurable maximum results per query

### 3. Context Augmentation
- **Prompt Injection**: Add retrieved knowledge to LLM context
- **Format Control**: Structured context formatting
- **Context Boundaries**: Clear markers for RAG content
- **Integration**: Seamless integration with conversation flow

### 4. CLI Extensions
- **Knowledge Commands**: `/knowledge`, `/search`, `/categories`, `/reload`
- **RAG Controls**: `--no-rag`, `--knowledge-file` options
- **Debug Support**: Detailed RAG operation logging
- **Statistics**: Knowledge base analytics and insights

### 5. Educational Features
- **Comparison Mode**: With/without RAG testing
- **Fictional Content**: Eliminates LLM prior knowledge
- **Clear Attribution**: Visible RAG context markers
- **Testing Framework**: Comprehensive RAG-specific tests

## RAG Technical Architecture

### Enhanced Component Structure

```
Simple Chatbot with RAG
├── Configuration Layer (config.py) [+ RAG settings]
├── LLM Client Layer (llm_client.py) [unchanged]
├── Memory Management (memory.py) [unchanged]
├── Knowledge Layer (knowledge_base.py) [NEW]
├── Core Logic (chatbot.py) [+ RAG integration]
└── Interface Layer (cli.py) [+ RAG commands]
```

### RAG Data Flow

```
User Query → Keyword Extraction → Knowledge Search → Context Injection → LLM → Enhanced Response
```

### RAG-Specific Design Patterns

1. **Repository Pattern**: Knowledge base data access abstraction
2. **Strategy Pattern**: Different retrieval algorithms (extensible)
3. **Decorator Pattern**: Context augmentation around base responses
4. **Template Method**: Standardized RAG pipeline execution
5. **Builder Pattern**: Complex context formatting

## RAG Data Models

### Enhanced Configuration Model
```python
@dataclass
class ChatbotConfig:
    # Base configuration (unchanged)
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama2"
    temperature: float = 0.3  # More deterministic for RAG
    max_tokens: int = 2000
    system_prompt: str = "You are a helpful assistant..."
    conversation_memory_limit: int = 10
    
    # RAG-specific configuration
    rag_enabled: bool = True
    knowledge_file: str = "data/knowledge.json"
    rag_max_results: int = 3
    rag_min_relevance: float = 0.1
```

### Knowledge Base Models
```python
@dataclass
class KnowledgeEntry:
    keywords: List[str]
    content: str
    category: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RetrievalResult:
    entry_id: str
    content: str
    relevance_score: float
    matched_keywords: List[str]
    category: Optional[str] = None
```

### Knowledge Base JSON Schema
```json
{
  "entry_id": {
    "keywords": ["keyword1", "keyword2", "..."],
    "content": "Detailed information about the topic...",
    "category": "category_name"
  }
}
```

## RAG API Specifications

### Enhanced ChatBot Interface

```python
class SimpleChatbot:
    # Base methods (inherited)
    def __init__(self, config: ChatbotConfig = None)
    def chat(self, user_input: str) -> str
    def reset_conversation(self) -> None
    def is_healthy(self) -> bool
    
    # Enhanced methods (modified for RAG)
    def get_conversation_stats(self) -> dict  # + RAG statistics
    def get_conversation_history(self, format_for_display: bool = True) -> str
    
    # New RAG-specific methods
    def search_knowledge(self, query: str) -> List[RetrievalResult]
    def get_knowledge_stats(self) -> dict
    def get_knowledge_categories(self) -> List[str]
    def reload_knowledge(self) -> bool
    
    # Internal RAG methods
    def _get_rag_context(self, user_input: str) -> str
    def _format_prompt(self, user_input: str) -> str  # Enhanced with RAG
```

### Knowledge Base Interface

```python
class SimpleKnowledgeBase:
    def __init__(self, knowledge_file: str | Path, enabled: bool = True)
    def search(self, query: str, max_results: int = 3, min_relevance_score: float = 0.1) -> List[RetrievalResult]
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]
    def get_all_entries(self) -> Dict[str, KnowledgeEntry]
    def get_categories(self) -> List[str]
    def search_by_category(self, category: str) -> List[KnowledgeEntry]
    def format_context(self, results: List[RetrievalResult]) -> str
    def get_stats(self) -> Dict[str, Any]
    def reload(self) -> None
    
    # Internal methods
    def _extract_keywords(self, query: str) -> Set[str]
    def _load_knowledge(self) -> None
```

## RAG Implementation Requirements

### Enhanced Project Structure
```
simple-chatbot-miniRAG/
├── src/simple_chatbot/
│   ├── __init__.py
│   ├── config.py           # + RAG configuration
│   ├── llm_client.py       # unchanged
│   ├── memory.py           # unchanged
│   ├── chatbot.py          # + RAG integration
│   ├── knowledge_base.py   # NEW: Core RAG functionality
│   └── cli.py              # + RAG commands
├── data/                   # NEW: Knowledge storage
│   └── knowledge.json      # NEW: Fictional universe data
├── tests/
│   ├── test_config.py      # updated for RAG
│   ├── test_memory.py      # unchanged
│   ├── test_chatbot.py     # + RAG tests
│   └── test_knowledge_base.py  # NEW: RAG-specific tests
├── pyproject.toml          # version 0.2.0
└── README.md               # updated for RAG
```

### RAG Processing Pipeline
```python
def rag_pipeline(user_query: str) -> str:
    # 1. Query Processing
    keywords = extract_keywords(user_query)
    
    # 2. Knowledge Retrieval
    results = knowledge_base.search(keywords)
    
    # 3. Context Formatting
    context = format_context(results)
    
    # 4. Prompt Augmentation
    enhanced_prompt = inject_context(context, user_query)
    
    # 5. LLM Generation
    response = llm.generate(enhanced_prompt)
    
    return response
```

### Aethelgard Universe Schema
```json
{
  "character_aris_thorne": {
    "keywords": ["Aris Thorne", "aris", "thorne", "xenobotanist", "scientist"],
    "content": "Dr. Aris Thorne is the lead xenobotanist...",
    "category": "character"
  },
  "location_aethelgard": {
    "keywords": ["aethelgard", "planet", "world", "violet", "xylos"],
    "content": "Aethelgard is a terrestrial exoplanet...",
    "category": "location"
  }
}
```

## RAG Quality Assurance

### RAG-Specific Testing Strategy
- **Knowledge Base Tests**: JSON loading, search functionality, relevance scoring
- **Retrieval Tests**: Keyword extraction, result filtering, context formatting
- **Integration Tests**: RAG pipeline integration with chatbot
- **Comparison Tests**: With/without RAG response verification
- **Edge Cases**: Empty results, malformed queries, missing knowledge

### Test Coverage Requirements
- **Knowledge Base Tests**: 27 test cases
- **RAG Integration Tests**: 4 test cases  
- **Updated Configuration Tests**: Updated for RAG settings
- **Total Test Count**: 60 tests (100% passing)
- **Coverage Target**: 100% for RAG components

### RAG Performance Metrics
- **Retrieval Accuracy**: Relevant results for test queries
- **Response Enhancement**: Measurable improvement over baseline
- **Keyword Coverage**: Comprehensive keyword matching
- **Context Quality**: Well-formatted, relevant context injection
- **Latency Impact**: Minimal overhead from RAG processing

### Educational Validation
- **Fictional Content**: Zero LLM prior knowledge contamination
- **Clear Attribution**: RAG context clearly visible in responses
- **Reproducible Results**: Consistent behavior for testing
- **Debug Transparency**: Observable RAG operation details
- **Learning Objectives**: Demonstrable RAG concept understanding

## RAG Deployment Specifications

### Knowledge Base Management
- **File Location**: `data/knowledge.json` (configurable)
- **Format Validation**: JSON schema validation on load
- **Content Updates**: Runtime reload capability (`/reload` command)
- **Version Control**: Track knowledge base changes
- **Backup Strategy**: Knowledge file backup and recovery

### RAG-Specific Configuration
```bash
# Required for RAG deployment
export RAG_ENABLED="true"
export RAG_KNOWLEDGE_FILE="data/knowledge.json"

# Performance tuning
export RAG_MAX_RESULTS="3"
export RAG_MIN_RELEVANCE="0.1"
# Note: CHATBOT_TEMPERATURE defaults to 0.3 for deterministic responses
```

### Educational Deployment
- **Fictional Content**: Ensure knowledge base contains no real information
- **Demo Scripts**: Prepared queries for demonstration
- **Comparison Mode**: Easy switching between RAG/no-RAG modes
- **Debug Output**: Visible RAG operation for learning

## RAG Security Considerations

### Knowledge Base Security
- **Content Validation**: Sanitize knowledge entries
- **Access Control**: Read-only knowledge file access
- **Injection Prevention**: Escape special characters in content
- **File Integrity**: Validate JSON structure and content

### Prompt Injection Protection
- **Context Isolation**: Clear boundaries around RAG content
- **Content Filtering**: Remove potentially harmful content
- **Query Sanitization**: Clean user queries before processing
- **Response Validation**: Monitor generated responses

### Educational Safety
- **Fictional Content**: No real personal or sensitive information
- **Controlled Environment**: Limited to educational scenarios
- **Transparent Operation**: All RAG operations visible for learning
- **Reversible Changes**: Easy to disable RAG functionality

## Command Line Interface Specifications

### New RAG Commands
```bash
# RAG testing commands
uv run chatbot --no-rag              # Disable RAG for comparison
uv run chatbot --debug               # Show RAG retrieval process
uv run chatbot --knowledge-file path # Custom knowledge base

# Interactive RAG commands (within chatbot)
/knowledge                           # Show knowledge base stats
/search <query>                      # Manual knowledge search
/categories                          # List knowledge categories
/reload                              # Reload knowledge base
```

### RAG Debug Output Example
```
[DEBUG] Extracting keywords from: "Who is Dr. Aris Thorne?"
[DEBUG] Found keywords: {'who', 'aris', 'thorne', 'dr'}
[DEBUG] Knowledge search found 1 results
[DEBUG] Top result: character_aris_thorne (relevance: 0.29)
[DEBUG] Injecting RAG context into prompt
```

## Integration with Original Project

### Unchanged Components
- **LLM Client**: Full compatibility with original implementation
- **Memory Management**: Identical conversation history handling
- **Base Configuration**: All original settings preserved
- **Error Handling**: Same error recovery mechanisms

### Enhanced Components
- **Configuration**: Extended with RAG settings
- **Core Chatbot**: RAG integration in prompt formatting
- **CLI Interface**: Additional commands and options
- **Testing Suite**: Expanded with RAG-specific tests

### Migration Path
```python
# Original usage (still works)
chatbot = SimpleChatbot()
response = chatbot.chat("Hello")

# New RAG usage
config = ChatbotConfig(rag_enabled=True)
chatbot = SimpleChatbot(config)
response = chatbot.chat("Who is Dr. Aris Thorne?")
```

## Performance Considerations

### RAG Overhead
- **Keyword Extraction**: ~1ms per query
- **Knowledge Search**: ~5ms for typical knowledge base
- **Context Formatting**: ~2ms per result
- **Total RAG Overhead**: <10ms additional latency

### Memory Usage
- **Knowledge Base**: ~50KB for Aethelgard universe
- **Search Index**: Minimal memory footprint
- **Context Cache**: Optional for performance optimization

### Scalability
- **Knowledge Entries**: Tested up to 100 entries
- **Concurrent Queries**: Single-threaded design
- **File Size Limits**: Recommended <1MB for JSON file

## Future Extensions

### Potential Enhancements
- **Vector Embeddings**: Advanced semantic search
- **Multiple Knowledge Sources**: Support for multiple files
- **Caching Layer**: In-memory search result caching
- **Real-time Updates**: File system monitoring for changes
- **Web Interface**: Browser-based RAG exploration

### Educational Progressions
1. **Current**: Simple keyword-based RAG
2. **Intermediate**: TF-IDF scoring
3. **Advanced**: Vector similarity search
4. **Expert**: Multi-modal knowledge integration