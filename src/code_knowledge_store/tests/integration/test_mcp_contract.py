"""Integration tests for MCP server contract and functionality."""

import os
import sys
import logging
import pytest
import pytest_asyncio
import shutil
from pathlib import Path
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
#from code_knowledge_store.server import mcp  # Don't import mcp here

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Test data
TEST_STORAGE_DIR = Path("test_knowledge_store")
TEST_KNOWLEDGE = {
    "active_context": {
        "path": "activeContext.md",
        "content": "# Active Context\nCurrent focus: Testing MCP server implementation",
        "metadata": {"type": "markdown", "category": "context"}
    },
    "system_patterns": {
        "path": "systemPatterns.md",
        "content": "# System Patterns\nMCP server architecture and design patterns",
        "metadata": {"type": "markdown", "category": "architecture"}
    }
}

@pytest.fixture(autouse=True)
def clean_storage():
    """Clean up test storage before and after each test."""
    # Clean up before test
    if TEST_STORAGE_DIR.exists():
        shutil.rmtree(TEST_STORAGE_DIR)
    yield
    # Clean up after test
    if TEST_STORAGE_DIR.exists():
        shutil.rmtree(TEST_STORAGE_DIR)

@pytest_asyncio.fixture
async def client() -> ClientSession:
    """Create an MCP client connected to the server via stdio."""
    logger.info("Starting client fixture setup")

    # Set storage dir in env
    os.environ["STORAGE_DIR"] = str(TEST_STORAGE_DIR)
    # Construct the full path to the server.py script
    server_path = Path(__file__).parent.parent.parent / "server.py"  # Adjust path if needed

    params = StdioServerParameters(
        command=sys.executable,  # Use the current Python interpreter
        args=[str(server_path)],  # Execute the server.py script directly
        env={"STORAGE_DIR": str(TEST_STORAGE_DIR)}
    )

    logger.info("Launching server process: %s %s", params.command, " ".join(params.args))
    async with stdio_client(params) as (reader, writer):
        logger.info("Server process launched, creating client session")
        async with ClientSession(reader, writer) as session:
            logger.info("Initializing client session")
            await session.initialize()
            logger.info("Client session initialized")
            yield session
            logger.info("Client session completed")

@pytest.mark.asyncio
async def test_list_tools(client: ClientSession):
    """Test that the server exposes the expected tools."""
    logger.info("Starting test_list_tools")
    result = await client.list_tools()
    tool_names = {tool.name for tool in result.tools}
    expected_tools = {
        "add_knowledge",
        "search_knowledge"
    }
    assert tool_names == expected_tools
    logger.info("test_list_tools completed")

@pytest.mark.asyncio
async def test_add_knowledge(client: ClientSession):
    """Test adding new knowledge."""
    logger.info("Starting test_add_knowledge")
    entry = TEST_KNOWLEDGE["active_context"]
    result = await client.call_tool(
        "add_knowledge",
        path=entry["path"],
        content=entry["content"],
        metadata=entry["metadata"]
    )
    assert result.content[0].text == '{"success": true}'
    logger.info("test_add_knowledge completed")
