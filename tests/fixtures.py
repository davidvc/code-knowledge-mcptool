"""Test fixtures and helper functions."""
import json
from typing import Any, Dict, List
import mcp.types as types
from pathlib import Path

# Test storage directory
TEST_STORAGE_DIR = Path("test_knowledge_store")

# Test knowledge examples
TEST_KNOWLEDGE = {
    "active_context": {
        "path": "memory-bank/activeContext.md",
        "content": """
# Active Context

## Current Focus
Integration testing with focus on MCP functionality:
- Single comprehensive integration test suite
- Focus on MCP tool functionality
- Testing real-world usage scenarios
""",
        "metadata": {
            "type": "memory_bank",
            "category": "active_context",
            "last_updated": "2024-02-17"
        }
    },
    "system_patterns": {
        "path": "memory-bank/systemPatterns.md",
        "content": """
# System Patterns

## Memory Bank Architecture
The memory bank combines two complementary storage approaches:
1. Vector Database (ChromaDB)
2. Markdown Documentation
""",
        "metadata": {
            "type": "memory_bank",
            "category": "architecture",
            "status": "current"
        }
    }
}

def assert_tool_response(
    result: List[types.TextContent | types.ImageContent],
    expected_data: Dict[str, Any] = None,
    expect_error: bool = False
) -> Dict[str, Any]:
    """Assert tool response format and return parsed data."""
    assert len(result) == 1
    assert result[0].type == "text"
    
    data = json.loads(result[0].text)
    
    if expect_error:
        assert "error" in data
    else:
        assert "error" not in data
        if expected_data:
            for key, value in expected_data.items():
                assert data[key] == value
    
    return data

def assert_resource_content(
    content: str,
    expected_content: str,
    expected_metadata: Dict[str, Any]
) -> None:
    """Assert resource content matches expectations."""
    data = json.loads(content)
    assert data["content"] == expected_content
    assert data["metadata"] == expected_metadata

def assert_storage_exists() -> None:
    """Assert storage files exist."""
    assert TEST_STORAGE_DIR.exists()
    assert (TEST_STORAGE_DIR / "embeddings.npy").exists()
    assert (TEST_STORAGE_DIR / "segments.json").exists()

async def add_test_knowledge(server, entries: Dict[str, Dict] = None) -> None:
    """Add test knowledge entries to server."""
    entries = entries or TEST_KNOWLEDGE
    for entry in entries.values():
        await server.call_tool(
            "add_knowledge",
            {
                "path": entry["path"],
                "content": entry["content"],
                "metadata": entry["metadata"]
            }
        )