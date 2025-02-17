# Code Knowledge Tool

A knowledge management tool for code repositories using vector embeddings. This tool helps maintain and query knowledge about your codebase using advanced embedding techniques.

## Installation

There are two ways to install this tool locally:

### Option 1: Install from wheel file (recommended for usage)

1. First, install PyTorch according to your system requirements:
   - Visit [PyTorch Installation](https://pytorch.org/get-started/locally/) to get the correct command for your system
   - For example, on macOS with pip:
     ```bash
     pip install torch
     ```

2. Install the code knowledge tool from the wheel file:
```bash
# Navigate to where you downloaded/built the package
cd /path/to/code_knowledge_tool

# Install from the wheel file
pip install dist/code_knowledge_tool-0.1.0-py3-none-any.whl
```

### Option 2: Install in editable mode (recommended for development)

This option is best if you want to modify the tool or contribute to its development:

```bash
# Clone the repository
git clone https://github.com/yourusername/code-knowledge-tool.git
cd code-knowledge-tool

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install PyTorch first
pip install torch

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
        "PYTHONPATH": "${workspaceFolder}",
        "SENTENCE_TRANSFORMERS_HOME": "${userHome}/.cache/sentence-transformers"
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
- Efficient embedding generation using sentence-transformers
- Support for multiple file types
- Context-aware code understanding
- Integration with RooCode and Cline via MCP
- RAG-based context augmentation

## Requirements

- Python 3.8-3.13
- PyTorch (installed separately)
- sentence-transformers
- chromadb for vector operations

## Development

### Building the Package

To build the distribution packages:
```bash
# Make sure you're in your virtual environment
source venv/bin/activate

# Install build tools
pip install --upgrade build

# Build the package
python -m build
```

This will create two files in the dist/ directory:
- A wheel file (.whl) for installing the package
- A source distribution (.tar.gz) for distribution

### Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Future Distribution

If you want to make this package available through pip (i.e., `pip install code-knowledge-tool`), you would need to:
1. Register an account on [PyPI](https://pypi.org)
2. Install twine: `pip install twine`
3. Upload your distribution: `twine upload dist/*`

However, for now, use the local installation methods described above.

## License

MIT License