# Project Brief: Chat with Code Repository Tool

## Core Mission
Create a Python-based tool that enables conversational interaction with local code repositories through vector embeddings, exposed as an MCP tool for Cline integration.

## Key Requirements

### Must Have
- Local file system repository access
- Local embedding engine (Ollama with Llama-3)
- Local vector database (Chroma)
- MCP tool integration with Cline

### Technical Scope
- Language: Python 3.8+
- Core Dependencies:
  - chromadb for vector operations
  - Integration with local Ollama service
  - MCP protocol implementation

### Key Constraints
- Repository access limited to local file system
- All components (embedding engine, vector DB) must run locally
- Response time < 5 seconds for typical queries
- Memory usage < 1GB for typical repositories
- Support repositories up to 100MB in size

## Success Criteria
1. Successfully loads and indexes local code repositories
2. Generates meaningful embeddings via local Ollama service
3. Efficiently stores and queries vectors via local Chroma
4. Seamlessly integrates with Cline via MCP protocol
5. Provides clear, relevant responses to code queries
