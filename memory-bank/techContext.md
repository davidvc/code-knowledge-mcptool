# Technical Context

## Technology Stack

### Core Technologies
- **Language**: Python 3.8-3.11 (PyTorch dependency limits Python version)
- **Vector Database**: Chroma
- **Embedding Engine**: Ollama with Llama-3
- **Protocol**: MCP (Model Context Protocol)
- **SDK**: MCP SDK for server implementation

### Key Dependencies
```plaintext
@modelcontextprotocol/sdk  # MCP SDK for server implementation
chromadb                   # Vector database operations
ollama                     # Embedding generation
httpx                      # HTTP client for API calls
pydantic                   # Data validation
typing_extensions          # Type hints support
pytest                     # Testing framework
pytest-cov                 # Test coverage
```

### Test Dependencies
```plaintext
pytest-env        # Environment variable management
pytest-asyncio    # Async test support
pytest-mock       # Mocking support
```

## Development Environment
- Local development setup
- Python virtual environment with uv
- Ollama service required
- ~100MB disk space for embedding model

## Technical Constraints

### Performance Limits
- Response time: < 5 seconds
- Memory usage: < 1GB
- Repository size: <= 100MB

### Infrastructure Requirements
- Sufficient disk space for:
  - Vector storage
  - Embedding model (~100MB)
- Adequate RAM for embedding operations
- No GPU required (CPU-only operation)
- Running Ollama service

## Integration Points

### MCP SDK Integration
- Server implementation
- Tool registration
- Resource handling
- Contract compliance

### Ollama Integration
- Model: Llama-3
- Optimized for:
  - Fast embedding generation
  - Efficient batching
  - Low memory usage
- Local operation with API calls

### MCP Server Configuration
```json
{
  "server": {
    "name": "code-knowledge-tool",
    "version": "0.1.0",
    "capabilities": {
      "tools": true,
      "resources": true
    }
  },
  "tools": [
    {
      "name": "chat_with_code",
      v
      "input_schema": {
        "source_path": "string",
        "question": "string",
        "base_url": "string (optional)"
      },
      "output_schema": {
        "response": "string",
        "error": "string (optional)"
      }
    }
  ]
}
```

## Security Considerations
- Local-only operation
- No persistent storage
- Clean session management
- Limited file system access

## Testing Infrastructure

### Integration Testing
- Uses TCP/IP transport for testing (not shared memory)
- MCP contract verification
- Tool registration testing
- Resource access validation
- Network-based communication testing
- Server implementation testing

### Test Configuration
```python
@pytest.fixture
async def server() -> AsyncIterator[Server]:
    """Create and yield a test server instance."""
    server = await serve(storage_dir=TEST_STORAGE_DIR)
    yield server
    await server.close()
```

### Test Execution
- Contract compliance tests
- Tool registration tests
- Resource access tests
- Error handling tests

## Monitoring & Debugging
- Structured logging
- Performance metrics
- Error tracking
- Resource usage monitoring

## MCP Tools Configuration

### Code Knowledge Tool
```json
{
  "tool_name": "code_knowledge",
  "description": "Interact with code repositories using natural language",
  "input_schema": {
    "query": "string",
    "context": "string (optional)",
    "max_results": "number (optional)"
  },
  "output_schema": {
    "success": "boolean",
    "results": "array",
    "error": "string (optional)"
  }
}
```

### Server Implementation
When implementing the MCP server:
1. Register tools and resources
2. Handle requests asynchronously
3. Validate inputs/outputs
4. Manage errors appropriately
5. Clean up resources

## Future Technical Considerations
- Enhanced MCP tool capabilities
- Additional resource types
- Improved error handling
- Better test coverage
- Performance optimizations
