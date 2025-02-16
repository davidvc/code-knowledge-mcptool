# Technical Context

## Technology Stack

### Core Technologies
- **Language**: Python 3.8+
- **Vector Database**: Chroma
- **Embedding Engine**: Ollama with Llama-3
- **Protocol**: MCP (Model Context Protocol)

### Key Dependencies
```plaintext
chromadb          # Vector database operations
httpx             # HTTP client for Ollama API
pydantic          # Data validation
typing_extensions # Type hints support
```

## Development Environment
- Local development setup
- Python virtual environment recommended
- No external services required beyond Ollama

## Technical Constraints

### Performance Limits
- Response time: < 5 seconds
- Memory usage: < 1GB
- Repository size: <= 100MB

### Infrastructure Requirements
- Ollama service running locally
- Sufficient disk space for temporary vector storage
- Adequate RAM for embedding operations

## Integration Points

### Ollama Service
- Default URL: http://localhost:11434
- REST API interface
- Embedding dimension consistency

### MCP Integration
```json
{
  "tool_name": "chat_with_code",
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
```

## Security Considerations
- Local-only operation
- No persistent storage
- Clean session management
- Limited file system access

## Testing Strategy
- Unit tests for core components
- Integration tests for Ollama interaction
- Performance benchmarks
- Security validation

## Monitoring & Debugging
- Structured logging
- Performance metrics
- Error tracking
- Resource usage monitoring

## Future Technical Considerations
- Caching mechanisms
- Incremental updates
- Alternative embedding models
- Enhanced query capabilities
