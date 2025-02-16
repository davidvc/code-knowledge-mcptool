# System Patterns

## Code Analysis Architecture

### Two-Phase Code Understanding
The system uses a two-phase approach for code understanding:

1. Semantic Analysis Phase
   - Code is analyzed by an LLM to generate semantic summaries
   - Captures actual functionality and purpose rather than just text
   - Abstracts implementation details into high-level understanding

2. Embedding Phase
   - Semantic summaries are embedded for similarity search
   - File paths preserved as metadata
   - Enables semantic-based code search

### Model Abstraction Layer
```python
class CodeAnalyzer:
    """Abstract base class for code analysis"""
    def analyze_code(self, code: str, file_path: str) -> str:
        """Generate semantic summary of code"""
        raise NotImplementedError
```

- Flexible model selection through abstraction
- Supports both cloud and local models
- Enables future switch to proprietary models for sensitive code

### Rate Limiting Strategy
The system implements robust rate limiting for API calls:

1. Sliding Window Rate Limiting
   - Tracks requests within a time window
   - Prevents exceeding API rate limits
   - Configurable window size and request limits

2. Exponential Backoff
   - Handles rate limit errors gracefully
   - Increases wait time between retries
   - Maximum retry attempts configurable

3. Batch Processing
   - Checkpointing for interrupted runs
   - Progress tracking
   - Error collection and reporting

### Configuration System
```python
config = {
    "rate_limit": {
        "requests_per_minute": 20,
        "max_retries": 3,
        "backoff_base": 2
    },
    "batch": {
        "checkpoint_interval": 10,
        "checkpoint_file": "analysis_checkpoint.json"
    },
    "model": {
        "type": "openai",  # or "local"
        "parameters": {
            "temperature": 0.3,
            "max_tokens": 500
        }
    }
}
```

- Configuration-driven behavior
- Easy switching between models
- Adjustable processing parameters

## Code Search Patterns

### Semantic Search
- Based on code meaning rather than text similarity
- Leverages LLM understanding of code structure
- More accurate results for functional queries

### Metadata Integration
- File paths preserved with semantic summaries
- Enables filtering and organization
- Maintains project structure context

## Implementation Considerations

### Security
- Model abstraction supports local processing for sensitive code
- No proprietary code sent to cloud services when needed
- Configurable security boundaries

### Scalability
- Rate limiting ensures stable processing
- Checkpointing enables handling large codebases
- Batch processing with resume capability

### Extensibility
- Abstract interfaces for key components
- Easy addition of new model implementations
- Configurable processing pipeline
