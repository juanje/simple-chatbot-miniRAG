"""Tests for the knowledge base module.

This module contains tests for the SimpleKnowledgeBase class
and related RAG functionality.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from simple_chatbot.knowledge_base import (
    KnowledgeEntry,
    RetrievalResult,
    SimpleKnowledgeBase,
)


@pytest.fixture
def sample_knowledge_data():
    """Sample knowledge data for testing with fictional universe."""
    return {
        "character_aris_thorne": {
            "keywords": ["Aris Thorne", "aris", "thorne", "xenobotanist", "scientist", "character"],
            "content": "Dr. Aris Thorne is the lead xenobotanist on the Aethelgard expedition. He discovered the sentient nature of the planet's flora.",
            "category": "character",
        },
        "character_kaelen_vance": {
            "keywords": ["Kaelen Vance", "kaelen", "vance", "security chief", "omnicorp", "antagonist"],
            "content": "Kaelen Vance is the ruthless security chief for OmniCorp's Outpost Delta and driver behind Operation Grasping Hand.",
            "category": "character",
        },
        "location_aethelgard": {
            "keywords": ["aethelgard", "planet", "world", "violet sky", "xylos"],
            "content": "Aethelgard is a terrestrial exoplanet with a violet sky and massive Xylos crystal deposits.",
            "category": "location",
        },
        "species_sylvans": {
            "keywords": ["sylvans", "aliens", "flora", "sentient plants", "bio-signaling"],
            "content": "The Sylvans are native, semi-sentient plant-like lifeforms that communicate through bioluminescent patterns.",
            "category": "lore",
        },
    }


@pytest.fixture
def temp_knowledge_file(sample_knowledge_data):
    """Create a temporary knowledge file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample_knowledge_data, f)
        temp_file = f.name

    yield temp_file

    # Cleanup
    Path(temp_file).unlink(missing_ok=True)


class TestKnowledgeEntry:
    """Tests for KnowledgeEntry model."""

    def test_knowledge_entry_creation(self):
        """Test KnowledgeEntry creation with valid data."""
        entry = KnowledgeEntry(
            keywords=["test", "example"],
            content="This is test content",
            category="testing",
        )

        assert entry.keywords == ["test", "example"]
        assert entry.content == "This is test content"
        assert entry.category == "testing"
        assert entry.metadata == {}

    def test_knowledge_entry_with_metadata(self):
        """Test KnowledgeEntry creation with metadata."""
        metadata = {"author": "test", "created": "2024-01-01"}
        entry = KnowledgeEntry(
            keywords=["test"],
            content="Test content",
            metadata=metadata,
        )

        assert entry.metadata == metadata

    def test_knowledge_entry_validation(self):
        """Test KnowledgeEntry validation."""
        # Test missing required fields
        with pytest.raises(ValueError):
            KnowledgeEntry(keywords=["test"])  # Missing content

        with pytest.raises(ValueError):
            KnowledgeEntry(content="test")  # Missing keywords


class TestRetrievalResult:
    """Tests for RetrievalResult model."""

    def test_retrieval_result_creation(self):
        """Test RetrievalResult creation."""
        result = RetrievalResult(
            entry_id="test_entry",
            content="Test content",
            relevance_score=0.8,
            matched_keywords=["test", "content"],
            category="testing",
        )

        assert result.entry_id == "test_entry"
        assert result.content == "Test content"
        assert result.relevance_score == 0.8
        assert result.matched_keywords == ["test", "content"]
        assert result.category == "testing"


class TestSimpleKnowledgeBase:
    """Tests for SimpleKnowledgeBase class."""

    def test_initialization_disabled(self):
        """Test knowledge base initialization when disabled."""
        kb = SimpleKnowledgeBase(knowledge_file="nonexistent.json", enabled=False)

        assert not kb.enabled
        assert len(kb.knowledge_data) == 0

    def test_initialization_enabled_with_valid_file(self, temp_knowledge_file):
        """Test knowledge base initialization with valid file."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file, enabled=True)

        assert kb.enabled
        assert len(kb.knowledge_data) == 4
        assert "character_aris_thorne" in kb.knowledge_data
        assert isinstance(kb.knowledge_data["character_aris_thorne"], KnowledgeEntry)

    def test_initialization_with_nonexistent_file(self):
        """Test knowledge base initialization with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            SimpleKnowledgeBase(knowledge_file="nonexistent.json", enabled=True)

    def test_initialization_with_invalid_json(self):
        """Test knowledge base initialization with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="Invalid JSON format"):
                SimpleKnowledgeBase(knowledge_file=temp_file, enabled=True)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_extract_keywords(self, temp_knowledge_file):
        """Test keyword extraction from queries."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        keywords = kb._extract_keywords("Who is Dr. Aris Thorne?")
        expected = {"who", "aris", "thorne"}
        assert expected.issubset(keywords)

        # Test with punctuation and short words
        keywords = kb._extract_keywords("Tell me about Aethelgard planet!")
        expected = {"tell", "about", "aethelgard", "planet"}
        assert expected.issubset(keywords)

    def test_search_basic(self, temp_knowledge_file):
        """Test basic search functionality."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Search for character-related content
        results = kb.search("aris thorne scientist")
        assert len(results) > 0
        assert results[0].entry_id == "character_aris_thorne"
        assert "aris" in results[0].matched_keywords or "thorne" in results[0].matched_keywords

    def test_search_disabled(self, temp_knowledge_file):
        """Test search when knowledge base is disabled."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file, enabled=False)

        results = kb.search("python programming")
        assert len(results) == 0

    def test_search_empty_query(self, temp_knowledge_file):
        """Test search with empty query."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        results = kb.search("")
        assert len(results) == 0

        results = kb.search("   ")
        assert len(results) == 0

    def test_search_with_parameters(self, temp_knowledge_file):
        """Test search with custom parameters."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Test max_results parameter
        results = kb.search("character", max_results=1)
        assert len(results) <= 1

        # Test min_relevance_score parameter
        results = kb.search("character", min_relevance_score=0.9)
        # Should return fewer results with high threshold
        high_threshold_count = len(results)

        results = kb.search("character", min_relevance_score=0.1)
        # Should return more results with low threshold
        low_threshold_count = len(results)

        assert low_threshold_count >= high_threshold_count

    def test_search_relevance_scoring(self, temp_knowledge_file):
        """Test relevance scoring in search results."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        results = kb.search("aris thorne xenobotanist character")

        # Results should be sorted by relevance (descending)
        for i in range(len(results) - 1):
            assert results[i].relevance_score >= results[i + 1].relevance_score

        # Check that relevance scores are reasonable
        for result in results:
            assert 0.0 <= result.relevance_score <= 1.0

    def test_get_entry(self, temp_knowledge_file):
        """Test getting specific entries."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        entry = kb.get_entry("character_aris_thorne")
        assert entry is not None
        assert isinstance(entry, KnowledgeEntry)
        assert "aris" in entry.keywords

        # Test nonexistent entry
        entry = kb.get_entry("nonexistent")
        assert entry is None

    def test_get_all_entries(self, temp_knowledge_file):
        """Test getting all entries."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        entries = kb.get_all_entries()
        assert len(entries) == 4
        assert "character_aris_thorne" in entries
        assert isinstance(entries["character_aris_thorne"], KnowledgeEntry)

        # Ensure it returns a copy (modifying returned dict shouldn't affect original)
        entries["test"] = "test_entry"
        assert "test" not in kb.knowledge_data

    def test_get_categories(self, temp_knowledge_file):
        """Test getting categories."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        categories = kb.get_categories()
        expected = ["character", "location", "lore"]
        assert sorted(categories) == expected

    def test_search_by_category(self, temp_knowledge_file):
        """Test searching by category."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Test existing category
        character_entries = kb.search_by_category("character")
        assert len(character_entries) == 2
        assert character_entries[0].category == "character"

        # Test case insensitive search
        lore_entries = kb.search_by_category("LORE")
        assert len(lore_entries) == 1
        assert lore_entries[0].category == "lore"

        # Test nonexistent category
        nonexistent_entries = kb.search_by_category("nonexistent")
        assert len(nonexistent_entries) == 0

    def test_format_context(self, temp_knowledge_file):
        """Test context formatting."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Test with results
        results = kb.search("aris thorne scientist")
        context = kb.format_context(results)

        assert "[CONTEXTO RAG - Información relevante:]" in context
        assert "[FIN CONTEXTO RAG]" in context
        assert "xenobotanist" in context

        # Test with empty results
        empty_context = kb.format_context([])
        assert empty_context == ""

    def test_get_stats(self, temp_knowledge_file):
        """Test getting statistics."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        stats = kb.get_stats()
        assert stats["enabled"] is True
        assert stats["total_entries"] == 4
        assert stats["total_categories"] == 3
        assert "character" in stats["categories"]
        assert stats["total_keywords"] > 0
        assert str(temp_knowledge_file) in stats["knowledge_file"]

    def test_get_stats_disabled(self, temp_knowledge_file):
        """Test getting statistics when disabled."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file, enabled=False)

        stats = kb.get_stats()
        assert stats["enabled"] is False
        assert stats["total_entries"] == 0

    def test_reload(self, temp_knowledge_file, sample_knowledge_data):
        """Test reloading knowledge base."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Verify initial state
        assert len(kb.knowledge_data) == 4

        # Modify the file
        modified_data = sample_knowledge_data.copy()
        modified_data["new_tech_entry"] = {
            "keywords": ["xylos", "crystal", "new", "tech"],
            "content": "Xylos is a powerful crystalline mineral from Aethelgard",
            "category": "technology",
        }

        with open(temp_knowledge_file, "w") as f:
            json.dump(modified_data, f)

        # Reload and verify changes
        kb.reload()
        assert len(kb.knowledge_data) == 5
        assert "new_tech_entry" in kb.knowledge_data

    def test_reload_disabled(self, temp_knowledge_file):
        """Test reloading when disabled."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file, enabled=False)

        # Should not raise an error, but won't actually reload
        kb.reload()
        assert len(kb.knowledge_data) == 0

    @patch("simple_chatbot.knowledge_base.logger")
    def test_logging(self, mock_logger, temp_knowledge_file):
        """Test that appropriate logging occurs."""
        SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Check that initialization logging occurred
        mock_logger.info.assert_called()

    def test_error_handling_in_search(self, temp_knowledge_file):
        """Test error handling during search operations."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Mock an error in the search method by mocking the search method directly
        with patch.object(kb, "_extract_keywords", side_effect=Exception("Test error")):
            # The search method has error handling, so it should return empty results
            results = kb.search("test query")
            # Should return empty results when error occurs
            assert results == []


class TestIntegration:
    """Integration tests for knowledge base functionality."""

    def test_full_rag_workflow(self, temp_knowledge_file):
        """Test complete RAG workflow."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # 1. Search for relevant content
        query = "Who is Dr. Aris Thorne?"
        results = kb.search(query)

        assert len(results) > 0
        assert results[0].entry_id == "character_aris_thorne"

        # 2. Format context
        context = kb.format_context(results)
        assert context
        assert "[CONTEXTO RAG" in context

        # 3. Verify context contains relevant information
        assert "xenobotanist" in context and "Aethelgard" in context

    def test_fictional_universe_consistency(self, temp_knowledge_file):
        """Test that the fictional universe data is consistent and searchable."""
        kb = SimpleKnowledgeBase(knowledge_file=temp_knowledge_file)

        # Test character searches
        results = kb.search("scientist xenobotanist")
        assert len(results) > 0
        assert "Aris Thorne" in results[0].content

        # Test location searches  
        results = kb.search("planet violet sky")
        assert len(results) > 0
        assert "Aethelgard" in results[0].content

        # Test cross-references work
        results = kb.search("aethelgard expedition")
        character_found = any("Aris Thorne" in r.content for r in results)
        location_found = any("Aethelgard" in r.content for r in results)
        assert character_found or location_found 