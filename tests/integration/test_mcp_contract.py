"""Integration tests for MCP server contract and functionality."""
import pytest
import shutil
from typing import AsyncIterator
import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl

from code_knowledge_tool.mcp_tool import serve
from ..fixtures import (
    TEST_STORAGE_DIR,
    TEST_KNOWLEDGE,
    assert_tool_response,
    assert_resource_content,
    assert_storage_exists,
    add_test_knowledge
)

@pytest.fixture(autouse=True)
async def clean_storage():
    """Clean up test storage before and after each test."""
    # Clean up before test
    if TEST_STORAGE_DIR.exists():
        shutil.rmtree(TEST_STORAGE_DIR)
    
    yield
    
    # Clean up after test
    if TEST_STORAGE_DIR.exists():
        shutil.rmtree(TEST_STORAGE_DIR)

@pytest.fixture
async def server() -> AsyncIterator[Server]:
    """Create and yield a test server instance."""
    server = await serve(storage_dir=TEST_STORAGE_DIR)
    yield server
    await server.close()

async def test_list_tools(server: Server):
    """Test that the server exposes the expected tools."""
    tools = await server.list_tools()
    
    # Verify tool list
    tool_names = {tool.name for tool in tools}
    expected_tools = {
        "add_knowledge",
        "search_knowledge",
        "get_context",
        "list_knowledge",
        "update_knowledge"
    }
    assert tool_names == expected_tools
    
    # Verify tool schemas
    add_tool = next(t for t in tools if t.name == "add_knowledge")
    assert "path" in add_tool.inputSchema["required"]
    assert "content" in add_tool.inputSchema["required"]
    assert "metadata" in add_tool.inputSchema["required"]
    
    search_tool = next(t for t in tools if t.name == "search_knowledge")
    assert "query" in search_tool.inputSchema["required"]

async def test_list_resources(server: Server):
    """Test listing available knowledge resources."""
    # Add test knowledge
    await add_test_knowledge(server)
    
    # List and verify resources
    resources = await server.list_resources()
    resource_uris = {r.uri for r in resources}
    expected_uris = {f"knowledge://{entry['path']}" for entry in TEST_KNOWLEDGE.values()}
    assert resource_uris == expected_uris

async def test_read_resource(server: Server):
    """Test reading knowledge resources."""
    entry = TEST_KNOWLEDGE["active_context"]
    await add_test_knowledge(server, {"test": entry})
    
    # Read and verify resource
    uri = f"knowledge://{entry['path']}"
    content = await server.read_resource(uri)
    assert_resource_content(content, entry["content"], entry["metadata"])

async def test_add_knowledge(server: Server):
    """Test adding new knowledge."""
    entry = TEST_KNOWLEDGE["active_context"]
    await add_test_knowledge(server, {"test": entry})
    
    # Verify response and storage
    assert_storage_exists()
    
    # Verify through resource
    uri = f"knowledge://{entry['path']}"
    content = await server.read_resource(uri)
    assert_resource_content(content, entry["content"], entry["metadata"])

async def test_search_knowledge(server: Server):
    """Test searching knowledge."""
    await add_test_knowledge(server)
    
    # Search and verify results
    result = await server.call_tool(
        "search_knowledge",
        {
            "query": "memory bank architecture",
            "limit": 5
        }
    )
    
    data = assert_tool_response(result)
    assert len(data["results"]) > 0
    assert any("systemPatterns.md" in r["path"] for r in data["results"])

async def test_get_context(server: Server):
    """Test getting relevant context."""
    await add_test_knowledge(server)
    
    # Get and verify context
    result = await server.call_tool(
        "get_context",
        {
            "task": "implement testing strategy",
            "limit": 3
        }
    )
    
    data = assert_tool_response(result)
    assert len(data["context"]) > 0
    assert any("activeContext.md" in c["path"] for c in data["context"])

async def test_list_knowledge(server: Server):
    """Test listing all knowledge entries."""
    await add_test_knowledge(server)
    
    # List and verify entries
    result = await server.call_tool(
        "list_knowledge",
        {
            "page": 1,
            "page_size": 10
        }
    )
    
    data = assert_tool_response(result)
    assert len(data["entries"]) == len(TEST_KNOWLEDGE)
    assert all(entry["path"] in [e["path"] for e in data["entries"]] 
              for entry in TEST_KNOWLEDGE.values())

async def test_update_knowledge(server: Server):
    """Test updating existing knowledge."""
    entry = TEST_KNOWLEDGE["active_context"]
    await add_test_knowledge(server, {"test": entry})
    
    # Update knowledge
    updated_content = entry["content"] + "\n- Added new test cases"
    updated_metadata = {**entry["metadata"], "last_updated": "2024-02-18"}
    
    result = await server.call_tool(
        "update_knowledge",
        {
            "path": entry["path"],
            "content": updated_content,
            "metadata": updated_metadata
        }
    )
    
    # Verify update
    assert_tool_response(result, {"success": True})
    
    # Verify through resource
    uri = f"knowledge://{entry['path']}"
    content = await server.read_resource(uri)
    assert_resource_content(content, updated_content, updated_metadata)
    assert_storage_exists()

async def test_error_handling(server: Server):
    """Test error handling in MCP server."""
    # Test duplicate knowledge
    await add_test_knowledge(server)
    
    # Try adding duplicate entry
    entry = TEST_KNOWLEDGE["active_context"]
    result = await server.call_tool(
        "add_knowledge",
        {
            "path": entry["path"],
            "content": "Duplicate content",
            "metadata": {}
        }
    )
    assert_tool_response(result, expect_error=True)
    
    # Test updating non-existent knowledge
    result = await server.call_tool(
        "update_knowledge",
        {
            "path": "nonexistent.md",
            "content": "New content",
            "metadata": {}
        }
    )
    assert_tool_response(result, expect_error=True)
    
    # Test invalid search query
    empty_query_result = await server.call_tool(
        "search_knowledge",
        {
            "query": "",  # Empty query
            "limit": 5
        }
    )
    assert_tool_response(empty_query_result, expect_error=True)
    
    # Test invalid tool name
    invalid_tool_result = await server.call_tool(
        "invalid_tool",
        {}
    )
    assert_tool_response(invalid_tool_result, expect_error=True)

@pytest.mark.parametrize("query,expected_path", [
    ("memory bank architecture", "systemPatterns.md"),
    ("testing strategy", "activeContext.md"),
])
async def test_search_variations(server: Server, query: str, expected_path: str):
    """Test search with different queries."""
    await add_test_knowledge(server)
    
    result = await server.call_tool(
        "search_knowledge",
        {
            "query": query,
            "limit": 5
        }
    )
    
    data = assert_tool_response(result)
    assert len(data["results"]) > 0
    assert any(expected_path in r["path"] for r in data["results"])