# System Patterns

## Development Environment

### Package Management with uv

1. Environment Setup
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

2. Dependency Management
   - Use pyproject.toml for dependencies
   - Lock file for reproducibility
   - Fast parallel installations
   - Efficient dependency resolution

3. Development Workflow
   - Clean environments with uv venv
   - Direct dependency installation
   - Quick environment recreation
   - Consistent builds

### Testing Architecture

1. Integration Tests
   ```python
   @pytest.fixture(autouse=True)
   async def clean_storage():
       """Clean up test storage before and after each test."""
       if TEST_STORAGE_DIR.exists():
           shutil.rmtree(TEST_STORAGE_DIR)
       yield
       if TEST_STORAGE_DIR.exists():
           shutil.rmtree(TEST_STORAGE_DIR)
   ```

2. Test Organization
   ```
   tests/
   ├── fixtures.py           # Shared test data and helpers
   └── integration/
       ├── test_mcp_contract.py    # MCP functionality
       └── test_package_build.py   # Installation verification
   ```

### Storage Architecture

1. Persistent Storage
   ```python
   class PersistentVectorStore(VectorStore):
       """Persistent vector store using atomic file operations."""
       
       def __init__(self, storage_dir: Path):
           self.storage_dir = Path(storage_dir)
           self.storage_dir.mkdir(parents=True, exist_ok=True)
           self._load_or_init_storage()
   ```

2. File Structure
   ```
   knowledge_store/
   ├── embeddings.npy     # Vector embeddings
   └── segments.json      # Knowledge entries and metadata
   ```

### MCP Server Architecture

1. Tool Handlers
   ```python
   class ToolHandler:
       """Base class for MCP tool handlers."""
       
       def __init__(self, embedder, vector_store):
           self.embedder = embedder
           self.vector_store = vector_store
       
       @classmethod
       def get_tool_definition(cls) -> types.Tool:
           raise NotImplementedError
   ```

2. Server Implementation
   ```python
   async def serve(storage_dir: Optional[Path] = None) -> Server:
       """Create and configure the MCP server."""
       server = Server(APP_NAME)
       embedder = OllamaEmbedder(base_url="http://localhost:11434")
       vector_store = PersistentVectorStore(
           storage_dir=storage_dir or Path("knowledge_store")
       )
   ```

## Implementation Guidelines

### 1. Error Handling
- Use proper error types
- Include error context
- Return descriptive messages
- Handle async errors

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
def _save_storage(self) -> None:
    """Save storage to files atomically."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        # Save files to temp directory
        # Move files atomically
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

1. Development
   - Use uv for environments
   - Keep dependencies minimal
   - Use lock files
   - Fast clean builds

2. Testing
   - Clean environment
   - Proper fixtures
   - Error scenarios
   - Resource cleanup

3. Storage
   - Atomic operations
   - Data validation
   - Error recovery
   - Proper cleanup

4. MCP Server
   - Clear tool definitions
   - Proper error handling
   - Resource management
   - Consistent responses

## Benefits

1. Development
   - Fast dependency resolution
   - Clean environments
   - Reproducible builds
   - Modern tooling

2. Testing
   - Reliable tests
   - Clean state
   - Clear failures
   - Easy debugging

3. Storage
   - Data integrity
   - Error recovery
   - Clean operations
   - Safe updates

4. MCP Server
   - Clear interface
   - Proper handling
   - Safe operations
   - Good documentation
