# Code MCP Tool

A semantic code search tool that helps you find relevant code in your repositories by understanding what the code actually does.

## Overview

Code MCP Tool analyzes your codebase to enable natural language queries about code functionality. Instead of just matching text, it helps you find code based on what it does.

For example, you can ask:
- "find string manipulation utilities"
- "show me code that handles date formatting"
- "where is the array sorting implementation"

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/code_mcp_tool.git
cd code_mcp_tool

# Install dependencies
pip install -e .
```

## Usage

1. Index a repository:
```bash
python src/index_repository.py path/to/your/repo
```
This creates a searchable index in `~/.code_chat_tool/indices/your-repo-name`

2. Search the code:
```bash
python src/query_index.py ~/.code_chat_tool/indices/your-repo-name
```

Then enter your questions in natural language to find relevant code.

## Security

- Designed to work with both public and private codebases
- Support for local model deployment for proprietary code
- No code sent to external services when using local models

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
