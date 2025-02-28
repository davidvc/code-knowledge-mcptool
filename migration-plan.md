# Migration Plan: Moving to uvx create-mcp-server Structure

## Simplified Approach
Focus on getting a working MCP server using the standard MCP server structure.

### Project Structure
```
code-knowledge-store/
├── README.md
├── pyproject.toml
└── src/
    └── code_knowledge_store/
        ├── __init__.py
        ├── server.py          # FastMCP server
        ├── embedding.py       # Existing embedding code
        └── vector_store.py    # Existing storage code
```

## Migration Steps

### 1. Project Setup
```bash
uvx create-mcp-server --name code-knowledge-store --path code-knowledge-store
```

### 2. Dependencies
```toml
[project]
dependencies = [
    "mcp>=1.2.1",
    "chromadb",
    "httpx",
    "numpy"
]
```

### 3. Server Implementation
```python
from mcp.server.fastmcp import FastMCP
from .embedding import OllamaEmbedder
from .vector_store import PersistentVectorStore

mcp = FastMCP("Code Knowledge Store")
```

### 4. Build and Test
1. Install dependencies:
   ```bash
   uv sync --dev --all-extras
   ```

2. Run MCP contract tests:
   ```bash
   pytest src/code_knowledge_store/tests/integration/test_mcp_contract.py
   ```

### 5. Cline Integration
Add to cline_mcp_settings.json:
```json
"mcpServers": {
  "code-knowledge-store": {
    "command": "python",
    "args": ["-m", "code_knowledge_store"]
  }
}
```

## Success Criteria
1. Passes MCP contract tests
2. Works with Cline
3. Maintains current functionality:
   - Knowledge storage
   - Embeddings
   - Search

## Next Steps
1. Complete server implementation
2. Test in Cline
3. Verify functionality

This simplified approach:
- Follows MCP server conventions
- Uses standard MCP deployment
- Focuses on core functionality