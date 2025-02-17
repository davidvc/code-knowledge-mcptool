"""MCP server implementation for code knowledge management."""
import json
import logging
from typing import AsyncIterator, Dict, Any, List, Optional
from pathlib import Path
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl

from .embedding import OllamaEmbedder
from .vector_store import PersistentVectorStore
from .tool_handlers import TOOL_HANDLERS, ToolHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "code_knowledge_tool"

async def serve(storage_dir: Optional[Path] = None) -> Server:
    """Create and configure the MCP server."""
    server = Server(APP_NAME)
    
    # Initialize components
    embedder = OllamaEmbedder(base_url="http://localhost:11434")
    vector_store = PersistentVectorStore(
        storage_dir=storage_dir or Path("knowledge_store")
    )
    
    # Initialize handlers
    handlers: Dict[str, ToolHandler] = {
        name: handler_cls(embedder, vector_store)
        for name, handler_cls in TOOL_HANDLERS.items()
    }
    
    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        """List available knowledge resources."""
        try:
            # Get all stored knowledge entries
            resources = []
            for path, entry in vector_store._segments.items():
                resources.append(
                    types.Resource(
                        uri=f"knowledge://{path}",
                        name=path,
                        mimeType="text/markdown",
                        description="Knowledge entry"
                    )
                )
            return resources
        except Exception as e:
            logger.error(f"Error listing resources: {str(e)}")
            return []

    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        """Read a specific knowledge resource."""
        try:
            if uri.scheme != "knowledge":
                raise ValueError(f"Invalid resource scheme: {uri.scheme}")
            
            path = uri.path.lstrip("/")
            entry = vector_store.get(path)
            
            if not entry:
                raise ValueError(f"Resource not found: {path}")
                
            return json.dumps({
                "content": entry[1].content,
                "metadata": entry[1].metadata
            })
        except Exception as e:
            logger.error(f"Error reading resource: {str(e)}")
            return json.dumps({"error": str(e)})

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            handler_cls.get_tool_definition()
            for handler_cls in TOOL_HANDLERS.values()
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent]:
        """Execute a tool with the given arguments."""
        try:
            handler = handlers.get(name)
            if not handler:
                raise ValueError(f"Unknown tool: {name}")
                
            return await handler.handle(arguments)
                
        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "tool": name
                })
            )]
    
    return server

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        server = await serve()
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
