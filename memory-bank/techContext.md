# Technical Context

## Technology Stack

### Core Technologies
- **Language**: Python 3.8-3.11 (PyTorch dependency limits Python version)
- **Vector Database**: Chroma
- **Embedding Engine**: sentence-transformers with all-MiniLM-L6-v2
- **Protocol**: MCP (Model Context Protocol)

### Key Dependencies
```plaintext
chromadb             # Vector database operations
sentence-transformers # Efficient embedding generation
torch               # Deep learning framework required by sentence-transformers
transformers        # Hugging Face transformers library
tokenizers          # Fast tokenization
httpx               # HTTP client for OpenRouter API
pydantic            # Data validation
typing_extensions   # Type hints support
pytest              # Testing framework
pytest-cov          # Test coverage
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
- No external services required
- ~100MB disk space for embedding model (downloaded on first use)

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

## Integration Points

### Sentence Transformers
- Model: all-MiniLM-L6-v2
- Optimized for:
  - Fast embedding generation
  - Efficient batching
  - Low memory usage
- Local operation with no API calls

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

## MCP Tools Configuration

### Git Automation Tool
```json
{
  "tool_name": "git_automation",
  "description": "Automates git operations when triggered by specific phrases",
  "input_schema": {
    "trigger_phrase": "string",
    "commit_message": "string (optional)",
    "push": "boolean (optional, default: true)"
  },
  "output_schema": {
    "success": "boolean",
    "message": "string",
    "git_output": "string"
  },
  "trigger_phrases": [
    "let's check this in",
    "commit and push changes"
  ]
}
```

### Activation
When Cline detects phrases like "let's check this in", it should:
1. Generate a descriptive commit message from recent changes
2. Execute git add -A
3. Commit with the generated message
4. Push to the remote repository
5. Report success/failure

## Future Technical Considerations
- Caching mechanisms for embeddings
- Incremental updates to avoid full reprocessing
- Alternative embedding models or configurations
- Enhanced query capabilities
- Extended git automation features:
  - Branch management
  - Conflict resolution
  - Custom commit message templates
