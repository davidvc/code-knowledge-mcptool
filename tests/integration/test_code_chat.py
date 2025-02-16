"""Integration tests for memory bank functionality."""
import pytest
from code_chat_tool.vector_store import InMemoryVectorStore
from code_chat_tool.embedding import SentenceTransformerEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool
from ..fixtures import (
    TEST_KNOWLEDGE,
    TEST_MARKDOWN,
    TEST_QUERIES,
    TEST_TASKS
)

@pytest.fixture
def chat_tool():
    """Initialize chat tool with test data."""
    embedder = SentenceTransformerEmbedder()
    vector_store = InMemoryVectorStore()
    tool = ChatWithCodeTool(embedder, vector_store)
    
    # Add test knowledge
    for entry in TEST_KNOWLEDGE:
        tool.add_knowledge(
            path=entry["path"],
            summary=entry["summary"],
            metadata=entry["metadata"]
        )
    
    return tool

def test_add_knowledge(chat_tool):
    """Test adding new knowledge."""
    new_entry = {
        "path": "src/auth/permissions.py",
        "summary": "Handles role-based access control and permission checking.",
        "metadata": {
            "type": "file",
            "last_updated": "2024-02-16",
            "related": ["auth/login.py"]
        }
    }
    
    # Add new knowledge
    chat_tool.add_knowledge(
        path=new_entry["path"],
        summary=new_entry["summary"],
        metadata=new_entry["metadata"]
    )
    
    # Search for the new knowledge
    results = chat_tool.search_knowledge("role-based access control")
    assert any(r.segment.path == new_entry["path"] for r in results)

def test_update_knowledge(chat_tool):
    """Test updating existing knowledge."""
    path = "src/auth/login.py"
    new_summary = "Updated authentication handler with OAuth support."
    
    # Update existing knowledge
    chat_tool.update_knowledge(
        path=path,
        new_summary=new_summary,
        metadata={"type": "file", "last_updated": "2024-02-16"}
    )
    
    # Search for updated knowledge
    results = chat_tool.search_knowledge("OAuth")
    assert any(r.segment.path == path for r in results)

def test_search_knowledge(chat_tool):
    """Test searching knowledge with different queries."""
    for test_case in TEST_QUERIES:
        results = chat_tool.search_knowledge(test_case["query"])
        found_paths = [r.segment.path for r in results]
        
        # Check that expected paths are found
        for expected_path in test_case["expected_paths"]:
            assert any(expected_path in path for path in found_paths)

def test_get_relevant_context(chat_tool):
    """Test retrieving relevant context for tasks."""
    for test_case in TEST_TASKS:
        print(f"\nTask: {test_case['task']}")
        context = chat_tool.get_relevant_context(test_case["task"])
        found_paths = [entry.path for entry in context]
        print(f"Expected paths: {test_case['expected_context']}")
        print(f"Found paths: {found_paths}")
        
        # Check that expected context is retrieved
        for expected_path in test_case["expected_context"]:
            assert any(expected_path in path for path in found_paths)

def test_knowledge_consistency(chat_tool):
    """Test that knowledge remains consistent after updates."""
    # Get initial search results
    initial_results = chat_tool.search_knowledge("authentication")
    initial_count = len(initial_results)
    
    # Update some knowledge
    chat_tool.update_knowledge(
        path="src/auth/login.py",
        new_summary="Updated authentication handler with new features.",
        metadata={"type": "file", "last_updated": "2024-02-16"}
    )
    
    # Check that result count remains same
    updated_results = chat_tool.search_knowledge("authentication")
    assert len(updated_results) == initial_count

def test_invalid_operations(chat_tool):
    """Test handling of invalid operations."""
    # Try to update non-existent entry
    with pytest.raises(ValueError):
        chat_tool.update_knowledge(
            path="nonexistent.py",
            new_summary="This should fail",
            metadata={}
        )
    
    # Try to add invalid entry
    with pytest.raises(ValueError):
        chat_tool.add_knowledge(
            path="",  # Empty path
            summary="This should fail",
            metadata={}
        )

def test_metadata_access(chat_tool):
    """Test accessing metadata for paths."""
    # Get metadata for existing path
    path = "src/auth/login.py"
    metadata = chat_tool.get_metadata(path)
    assert metadata is not None
    assert metadata["type"] == "file"
    
    # Get metadata for non-existent path
    assert chat_tool.get_metadata("nonexistent.py") is None
