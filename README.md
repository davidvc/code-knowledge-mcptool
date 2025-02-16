# Code Knowledge Tool

A knowledge management tool for code repositories using vector embeddings. This tool helps maintain and query knowledge about your codebase using advanced embedding techniques.

## Installation

1. First, install PyTorch according to your system requirements:
   - Visit [PyTorch Installation](https://pytorch.org/get-started/locally/) to get the correct command for your system
   - For example, on macOS with pip:
     ```bash
     pip3 install torch
     ```

2. Install the code knowledge tool:
```bash
pip install code-knowledge-tool[torch]
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

## Usage

The tool provides several ways to interact with your codebase:

1. Build knowledge about your code:
```python
# Add knowledge about a file or component
knowledge_tool.add_knowledge(
    path="src/your_file.py",
    summary="Description of the code's purpose",
    metadata={"type": "file", "last_updated": "2024-02-16"}
)
```

2. Search your codebase:
```python
# Search for specific functionality
results = knowledge_tool.search_knowledge("How does authentication work?")
for result in results:
    print(f"File: {result.segment.path}")
    print(f"Relevance: {result.score}")
```

3. Get context for tasks:
```python
# Get relevant context for a development task
context = knowledge_tool.get_relevant_context("Implement password reset")
for entry in context:
    print(f"File: {entry.path}")
    print(f"Relevance: {entry.relevance}")
```

## Features

- Local vector storage for code knowledge
- Efficient embedding generation using sentence-transformers
- Support for multiple file types
- Context-aware code understanding
- Integration with RooCode and Cline via MCP

## Requirements

- Python 3.8-3.13
- PyTorch (installed separately)
- sentence-transformers
- chromadb for vector operations

## Development

To set up for development:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/code-knowledge-tool.git
cd code-knowledge-tool
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install PyTorch:
```bash
# Visit pytorch.org for the correct command for your system
pip install torch
```

4. Install development dependencies:
```bash
pip install -e ".[dev,torch]"
```

5. Run tests:
```bash
pytest
```

## Building the Package

To build the distribution packages:
```bash
python -m build
```

This will create:
- A wheel file (.whl) in dist/
- A source distribution (.tar.gz) in dist/

## License

MIT License