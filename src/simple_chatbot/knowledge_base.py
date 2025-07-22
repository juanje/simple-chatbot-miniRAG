"""Knowledge base module for simple RAG implementation.

This module provides classes for managing a JSON-based knowledge base
and implementing keyword-based retrieval for RAG functionality.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class KnowledgeEntry(BaseModel):
    """Represents a single knowledge entry.

    Attributes:
        keywords: List of keywords that trigger this entry
        content: The actual knowledge content
        category: Optional category for organization
        metadata: Additional metadata for the entry
    """

    keywords: List[str] = Field(description="Keywords that trigger this entry")
    content: str = Field(description="The actual knowledge content")
    category: Optional[str] = Field(default=None, description="Category for organization")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RetrievalResult(BaseModel):
    """Represents a retrieval result with relevance information.

    Attributes:
        entry_id: ID of the knowledge entry
        content: The knowledge content
        relevance_score: Score indicating relevance to the query
        matched_keywords: Keywords that matched the query
        category: Category of the knowledge entry
    """

    entry_id: str = Field(description="ID of the knowledge entry")
    content: str = Field(description="The knowledge content")
    relevance_score: float = Field(description="Score indicating relevance to the query")
    matched_keywords: List[str] = Field(description="Keywords that matched the query")
    category: Optional[str] = Field(default=None, description="Category of the knowledge entry")


class SimpleKnowledgeBase:
    """Simple JSON-based knowledge base for RAG retrieval.

    This class manages a JSON file containing knowledge entries and provides
    keyword-based search functionality for simple RAG implementation.

    Attributes:
        knowledge_file: Path to the JSON knowledge file
        knowledge_data: Loaded knowledge entries
        enabled: Whether the knowledge base is enabled
    """

    def __init__(self, knowledge_file: str | Path, enabled: bool = True) -> None:
        """Initialize the knowledge base.

        Args:
            knowledge_file: Path to the JSON knowledge file
            enabled: Whether the knowledge base is enabled

        Raises:
            FileNotFoundError: If the knowledge file doesn't exist
            ValueError: If the knowledge file format is invalid
        """
        self.knowledge_file = Path(knowledge_file)
        self.enabled = enabled
        self.knowledge_data: Dict[str, KnowledgeEntry] = {}

        if self.enabled:
            self._load_knowledge()

        logger.info(f"Initialized knowledge base with {len(self.knowledge_data)} entries")

    def _load_knowledge(self) -> None:
        """Load knowledge from the JSON file.

        Raises:
            FileNotFoundError: If the knowledge file doesn't exist
            ValueError: If the knowledge file format is invalid
        """
        if not self.knowledge_file.exists():
            raise FileNotFoundError(f"Knowledge file not found: {self.knowledge_file}")

        try:
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            # Convert raw data to KnowledgeEntry objects
            for entry_id, entry_data in raw_data.items():
                self.knowledge_data[entry_id] = KnowledgeEntry(**entry_data)

            logger.info(f"Loaded {len(self.knowledge_data)} knowledge entries")

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in knowledge file: {e}") from e
        except Exception as e:
            raise ValueError(f"Error loading knowledge file: {e}") from e

    def _extract_keywords(self, query: str) -> Set[str]:
        """Extract potential keywords from a query.

        Args:
            query: The user query

        Returns:
            Set of normalized keywords
        """
        # Simple keyword extraction: lowercase, split by spaces, remove short words
        words = query.lower().split()
        keywords = {word.strip(".,!?;:()[]{}") for word in words if len(word) > 2}
        return keywords

    def search(
        self,
        query: str,
        max_results: int = 3,
        min_relevance_score: float = 0.1,
    ) -> List[RetrievalResult]:
        """Search for relevant knowledge entries.

        Args:
            query: The search query
            max_results: Maximum number of results to return
            min_relevance_score: Minimum relevance score for results

        Returns:
            List of RetrievalResult objects ordered by relevance
        """
        if not self.enabled or not query.strip():
            return []

        try:
            query_keywords = self._extract_keywords(query)
            results = []

            for entry_id, entry in self.knowledge_data.items():
                # Find matching keywords
                entry_keywords = {kw.lower() for kw in entry.keywords}
                matched_keywords = query_keywords.intersection(entry_keywords)

                if matched_keywords:
                    # Simple relevance scoring: ratio of matched keywords
                    relevance_score = len(matched_keywords) / len(entry_keywords)

                    if relevance_score >= min_relevance_score:
                        result = RetrievalResult(
                            entry_id=entry_id,
                            content=entry.content,
                            relevance_score=relevance_score,
                            matched_keywords=list(matched_keywords),
                            category=entry.category,
                        )
                        results.append(result)

            # Sort by relevance score (descending) and limit results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:max_results]

        except Exception as e:
            logger.error(f"Error during search operation: {e}")
            return []

    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get a specific knowledge entry by ID.

        Args:
            entry_id: The entry identifier

        Returns:
            KnowledgeEntry if found, None otherwise
        """
        return self.knowledge_data.get(entry_id)

    def get_all_entries(self) -> Dict[str, KnowledgeEntry]:
        """Get all knowledge entries.

        Returns:
            Dictionary of all knowledge entries
        """
        return self.knowledge_data.copy()

    def get_categories(self) -> List[str]:
        """Get all available categories.

        Returns:
            List of unique categories
        """
        categories = {entry.category for entry in self.knowledge_data.values() if entry.category}
        return sorted(categories)

    def search_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Search entries by category.

        Args:
            category: The category to search for

        Returns:
            List of entries in the specified category
        """
        return [
            entry
            for entry in self.knowledge_data.values()
            if entry.category and entry.category.lower() == category.lower()
        ]

    def format_context(self, results: List[RetrievalResult]) -> str:
        """Format retrieval results as context for the LLM.

        Args:
            results: List of retrieval results

        Returns:
            Formatted context string
        """
        if not results:
            return ""

        context_parts = ["[CONTEXTO RAG - Información relevante:]"]

        for i, result in enumerate(results, 1):
            category_info = f" ({result.category})" if result.category else ""
            context_parts.append(f"{i}. {result.content}{category_info}")

        context_parts.append("[FIN CONTEXTO RAG]")
        return "\n".join(context_parts)

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics.

        Returns:
            Dictionary with statistics
        """
        if not self.enabled:
            return {"enabled": False, "total_entries": 0}

        categories = self.get_categories()
        total_keywords = sum(len(entry.keywords) for entry in self.knowledge_data.values())

        return {
            "enabled": True,
            "total_entries": len(self.knowledge_data),
            "total_categories": len(categories),
            "categories": categories,
            "total_keywords": total_keywords,
            "knowledge_file": str(self.knowledge_file),
        }

    def reload(self) -> None:
        """Reload the knowledge base from file.

        Raises:
            FileNotFoundError: If the knowledge file doesn't exist
            ValueError: If the knowledge file format is invalid
        """
        if self.enabled:
            self.knowledge_data.clear()
            self._load_knowledge()
            logger.info("Knowledge base reloaded") 