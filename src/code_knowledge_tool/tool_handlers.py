"""Tool handlers for MCP server operations."""
import json
from typing import Any, Dict, List
import mcp.types as types
import logging

from .embedding import OllamaEmbedder
from .vector_store import VectorStore

logger = logging.getLogger(__name__)

class ToolHandler:
    """Base class for MCP tool handlers."""
    
    def __init__(self, embedder: OllamaEmbedder, vector_store: VectorStore):
        """Initialize with required components."""
        self.embedder = embedder
        self.vector_store = vector_store
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        """Get the tool definition."""
        raise NotImplementedError
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle the tool execution."""
        raise NotImplementedError

class AddKnowledgeHandler(ToolHandler):
    """Handler for adding new knowledge."""
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        return types.Tool(
            name="add_knowledge",
            description="Add new knowledge to the repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path/identifier for the knowledge"
                    },
                    "content": {
                        "type": "string",
                        "description": "The knowledge content"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Additional metadata"
                    }
                },
                "required": ["path", "content", "metadata"]
            }
        )
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        try:
            path = arguments["path"]
            content = arguments["content"]
            metadata = arguments["metadata"]
            
            # Generate embedding
            embedding = self.embedder.embed_text(content)
            
            # Store knowledge
            self.vector_store.add(embedding, path, content, metadata)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({"success": True})
            )]
        except Exception as e:
            logger.error(f"Error adding knowledge: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]

class SearchKnowledgeHandler(ToolHandler):
    """Handler for searching knowledge."""
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        return types.Tool(
            name="search_knowledge",
            description="Search existing knowledge",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        try:
            query = arguments["query"]
            limit = arguments.get("limit", 5)
            
            # Generate query embedding
            query_embedding = self.embedder.embed_text(query)
            
            # Search vector store
            results = self.vector_store.search(query_embedding, limit)
            
            # Format results
            formatted_results = [{
                "path": r.segment.path,
                "content": r.segment.content,
                "score": r.score
            } for r in results]
            
            return [types.TextContent(
                type="text",
                text=json.dumps({"results": formatted_results})
            )]
        except Exception as e:
            logger.error(f"Error searching knowledge: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]

class GetContextHandler(ToolHandler):
    """Handler for getting relevant context."""
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        return types.Tool(
            name="get_context",
            description="Get relevant context for a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task description"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 3
                    }
                },
                "required": ["task"]
            }
        )
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        try:
            task = arguments["task"]
            limit = arguments.get("limit", 3)
            
            # Generate task embedding
            task_embedding = self.embedder.embed_text(task)
            
            # Search for relevant context
            results = self.vector_store.search(task_embedding, limit)
            
            # Format context
            context = [{
                "path": r.segment.path,
                "content": r.segment.content,
                "relevance": r.score
            } for r in results]
            
            return [types.TextContent(
                type="text",
                text=json.dumps({"context": context})
            )]
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]

class ListKnowledgeHandler(ToolHandler):
    """Handler for listing knowledge entries."""
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        return types.Tool(
            name="list_knowledge",
            description="List all knowledge entries",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number",
                        "default": 1
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Results per page",
                        "default": 10
                    }
                }
            }
        )
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        try:
            page = arguments.get("page", 1)
            page_size = arguments.get("page_size", 10)
            
            # Get all entries
            entries = []
            for path, entry in self.vector_store._segments.items():
                entries.append({
                    "path": path,
                    "content": entry.content,
                    "metadata": entry.metadata
                })
            
            # Paginate results
            start = (page - 1) * page_size
            end = start + page_size
            paginated = entries[start:end]
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "entries": paginated,
                    "total": len(entries),
                    "page": page,
                    "page_size": page_size
                })
            )]
        except Exception as e:
            logger.error(f"Error listing knowledge: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]

class UpdateKnowledgeHandler(ToolHandler):
    """Handler for updating knowledge."""
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        return types.Tool(
            name="update_knowledge",
            description="Update existing knowledge",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of entry to update"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "New metadata"
                    }
                },
                "required": ["path", "content", "metadata"]
            }
        )
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        try:
            path = arguments["path"]
            content = arguments["content"]
            metadata = arguments["metadata"]
            
            # Generate new embedding
            embedding = self.embedder.embed_text(content)
            
            # Update knowledge
            self.vector_store.update(embedding, path, content, metadata)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({"success": True})
            )]
        except Exception as e:
            logger.error(f"Error updating knowledge: {str(e)}")
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]

# Registry of all tool handlers
TOOL_HANDLERS = {
    "add_knowledge": AddKnowledgeHandler,
    "search_knowledge": SearchKnowledgeHandler,
    "get_context": GetContextHandler,
    "list_knowledge": ListKnowledgeHandler,
    "update_knowledge": UpdateKnowledgeHandler
}