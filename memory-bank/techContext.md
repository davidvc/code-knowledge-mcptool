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
httpx             # HTTP client for Ollama/OpenRouter APIs
pydantic          # Data validation
typing_extensions # Type hints support
pytest            # Testing framework
pytest-cov        # Test coverage
```

### Test Dependencies
```plaintext
openrouter-client # OpenRouter API integration
pytest-env        # Environment variable management
pytest-asyncio    # Async test support
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

## Testing Infrastructure

### Integration Testing
- Real repository submodules in test/integration/test-repos
- Response quality validation via OpenRouter API
- Configurable test settings:
  ```python
  OPENROUTER_API_KEY: str  # OpenRouter API key
  OPENROUTER_MODEL: str    # Model selection (default: google/palm-2-chat-bison)
  OLLAMA_BASE_URL: str     # Local Ollama service URL
  ```

### Test Execution
- Integration tests with real codebases
- Response quality validation using LLMs
- Performance benchmarking
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
