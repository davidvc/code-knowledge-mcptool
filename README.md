# Code Knowledge Tool

A knowledge management tool for code repositories using vector embeddings. This tool helps maintain and query knowledge about your codebase using advanced embedding techniques.

## Building and Installing

### 1. Build the Package

First, you need to build the distribution files:

```bash
# Clone the repository
git clone https://github.com/yourusername/code-knowledge-tool.git
cd code-knowledge-tool

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install build tools
python -m pip install --upgrade pip build

# Build the package
python -m build
```

This will create two files in the dist/ directory:
- code_knowledge_tool-0.1.0-py3-none-any.whl (wheel file for installation)
- code_knowledge_tool-0.1.0.tar.gz (source distribution)

### 2. Install the Package

#### Prerequisites

1. Ensure Ollama is installed and running:
```bash
# Install Ollama (if not already installed)
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

2. Install the package:

##### Option 1: Install from wheel file (recommended for usage)

```bash
# Navigate to where you built the package
cd /path/to/code_knowledge_tool

# Install from the wheel file
pip install dist/code_knowledge_tool-0.1.0-py3-none-any.whl
```

##### Option 2: Install in editable mode (recommended for development)

This option is best if you want to modify the tool or contribute to its development:

```bash
# Assuming you're already in the code-knowledge-tool directory
# and have activated your virtual environment

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

## Integration with RooCode/Cline

1. Copy the MCP configuration to your settings:

For Cline (VSCode):
```bash
# Open the settings file
open ~/Library/Application\ Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

Add this configuration:
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

For RooCode:
```bash
# Open the settings file
open ~/Library/Application\ Support/RooCode/roocode_config.json
```
Add the same configuration as above.

2. Restart RooCode/Cline to load the new tool.

## Using as Memory Bank and RAG Context Provider

This tool can serve as your project's memory bank and RAG context provider. To set this up:

1. Copy the provided template to your project:
```bash
cp clinerules_template.md /path/to/your/project/.clinerules
```

2. Customize the rules and patterns in .clinerules for your project's needs

The template includes comprehensive instructions for:
- Knowledge base management
- RAG-based development workflows
- Code quality guidelines
- Memory management practices

See clinerules_template.md for the full configuration and usage details.

## Features

- Local vector storage for code knowledge
- Efficient embedding generation using Ollama
- Support for multiple file types
- Context-aware code understanding
- Integration with RooCode and Cline via MCP
- RAG-based context augmentation
- Persistent knowledge storage

## Requirements

- Python 3.8 or higher
- Ollama service running locally
- chromadb for vector operations

## Development

### Running Tests

The project follows an integration-first testing approach, focusing on end-to-end functionality and MCP contract compliance. The test suite consists of:

1. MCP Contract Tests
   - Tool registration and execution
   - Resource management
   - Knowledge operations
   - Error handling

2. Package Build Tests
   - Installation verification
   - Dependency resolution
   - MCP server initialization
   - Basic functionality

To run the tests:
```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test suites
pytest tests/integration/test_mcp_contract.py -v  # MCP functionality
pytest tests/integration/test_package_build.py -v  # Installation verification
```

Test Environment Requirements:
```bash
# Ensure Ollama is running
ollama serve
```

The tests use a temporary directory (test_knowledge_store) that is cleaned up automatically between test runs.

For more details on the testing strategy and patterns, see the documentation in `docs/`.

## Future Distribution

If you want to make this package available through pip (i.e., `pip install code-knowledge-tool`), you would need to:
1. Register an account on [PyPI](https://pypi.org)
2. Install twine: `pip install twine`
3. Upload your distribution: `twine upload dist/*`

However, for now, use the local build and installation methods described above.

## License

MIT License