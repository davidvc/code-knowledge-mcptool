"""MCP server implementation for code knowledge management."""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator
import os
from mcp.server.fastmcp import FastMCP, Context

from embedding import OllamaEmbedder  # CORRECTED: Fully qualified name
from vector_store import PersistentVectorStore  # CORRECTED: Fully qualified name

@dataclass
class ServerContext:
    """Server context with initialized components."""
    embedder: OllamaEmbedder
    store: PersistentVectorStore

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
    """Initialize and cleanup server resources."""
    # Get storage dir from env or use default
    storage_dir = Path(os.getenv("STORAGE_DIR", "knowledge_store"))
    # Initialize components
    embedder = OllamaEmbedder(base_url="http://localhost:11434")
    store = PersistentVectorStore(storage_dir=storage_dir)
    try:
        yield ServerContext(embedder=embedder, store=store)
    finally:
        # Cleanup if needed
        pass

# Create server with lifespan
mcp = FastMCP("code-knowledge-store", lifespan=server_lifespan)

@mcp.tool()
def add_knowledge(path: str, content: str, metadata: dict, ctx: Context) -> dict:
    """Add new knowledge to the repository."""
    embedder = ctx.lifespan_context.embedder
    store = ctx.lifespan_context.store
    embedding = embedder.embed_text(content)
    store.add(embedding, path, content, metadata)
    return {"success": True}

@mcp.tool()
def search_knowledge(query: str, ctx: Context, limit: int = 5) -> dict:
    """Search existing knowledge."""
    embedder = ctx.lifespan_context.embedder
    store = ctx.lifespan_context.store
    query_embedding = embedder.embed_text(query)
    results = store.search(query_embedding, limit)
    return {
        "results": [{
            "path": r.segment.path,
            "content": r.segment.content,
            "score": r.score
        } for r in results]
    }

if __name__ == "__main__":
    mcp.run()