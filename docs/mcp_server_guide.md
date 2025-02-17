# MCP Server Implementation Guide

This guide provides a detailed walkthrough of the MCP server implementation for the Code Knowledge Tool.

## Server Architecture

### Core Components

1. Server Class
```python
async def serve(storage_dir: Optional[Path] = None) -> Server:
    """Create and configure the MCP server."""
    server = Server(APP_NAME)
    
    # Initialize components
    embedder = OllamaEmbedder(base_url="http://localhost:11434")
    vector_store = PersistentVectorStore(
        storage_dir=storage_dir or Path("knowledge_store")
    )
    
    # Initialize handlers
    handlers = {
        name: handler_cls(embedder, vector_store)
        for name, handler_cls in TOOL_HANDLERS.items()
    }
```

2. Tool Handlers
Each operation is implemented as a separate handler class following the Open-Closed Principle:

```python
class ToolHandler:
    """Base class for MCP tool handlers."""
    
    def __init__(self, embedder: OllamaEmbedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store
    
    @classmethod
    def get_tool_definition(cls) -> types.Tool:
        """Get the tool definition."""
        raise NotImplementedError
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle the tool execution."""
        raise NotImplementedError
```

### Available Tools

1. AddKnowledgeHandler
```python
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
```

2. SearchKnowledgeHandler
```python
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
```

### Resource Management

1. Resource Listing
```python
@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available knowledge resources."""
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
```

2. Resource Access
```python
@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a specific knowledge resource."""
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
```

## Implementation Guidelines

### 1. Error Handling
- Use proper error types
- Include error context
- Return descriptive messages
- Handle async errors

```python
try:
    # Operation code
except Exception as e:
    logger.error(f"Error in operation: {str(e)}")
    return [types.TextContent(
        type="text",
        text=json.dumps({
            "error": str(e),
            "context": "Additional context"
        })
    )]
```

### 2. Response Formatting
```python
# Success response
[types.TextContent(
    type="text",
    text=json.dumps({
        "success": True,
        "data": result
    })
)]

# Error response
[types.TextContent(
    type="text",
    text=json.dumps({
        "error": "Error description",
        "details": error_details
    })
)]
```

### 3. Storage Management
```python
class PersistentVectorStore(VectorStore):
    """Persistent vector store using files."""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._load_or_init_storage()
```

### 4. Testing Support
```python
@pytest.fixture
async def server() -> AsyncIterator[Server]:
    """Create and yield a test server instance."""
    server = await serve(storage_dir=TEST_STORAGE_DIR)
    yield server
    await server.close()
```

## Best Practices

1. Tool Implementation
   - One handler per operation
   - Clear input schemas
   - Proper error handling
   - Consistent response format

2. Resource Management
   - Validate URIs
   - Handle missing resources
   - Clean up resources
   - Proper error messages

3. Storage Handling
   - Persistent storage
   - Clean environment
   - Error recovery
   - Data consistency

4. Testing
   - Clean test environment
   - Proper fixtures
   - Error scenarios
   - Resource cleanup

## Configuration

1. Server Settings
```json
{
  "mcpServers": {
    "code_knowledge": {
      "command": "python",
      "args": ["-m", "code_knowledge_tool.mcp_tool"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
```

2. Environment Variables
   - OLLAMA_BASE_URL: Ollama service URL
   - STORAGE_DIR: Knowledge storage location
   - LOG_LEVEL: Logging configuration

## Benefits

1. Maintainability
   - Separate handlers
   - Clear responsibilities
   - Easy to extend
   - Consistent patterns

2. Reliability
   - Proper error handling
   - Resource cleanup
   - Data persistence
   - Clean testing

3. Usability
   - Clear tool definitions
   - Consistent responses
   - Good documentation
   - Easy configuration