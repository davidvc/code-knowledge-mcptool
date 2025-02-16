# Chat with Code Repository Tool Requirements

## Overview
A tool that enables conversational interaction with code repositories through a local vector database and embedding engine, exposed as an MCP tool.

## Core Requirements

### 1. Repository Source Support
- Must support loading code from:
  - Local file system directories
  - GitHub repositories (optional)
- Directory/repository scanning should:
  - Handle all common code file types
  - Respect .gitignore patterns
  - Support recursive directory traversal

### 2. Local Infrastructure
- Vector Database:
  - Use Chroma as the vector database
  - Store in temporary directories for each session
  - Support efficient similarity search
  
- Embedding Engine:
  - Use local Ollama with Llama-3 model
  - Support configurable base URL for Ollama service
  - Maintain consistent embedding dimensions

### 3. MCP Tool Integration
- Tool Registration:
  - Register as "chat_with_code" MCP tool
  - Accept JSON input parameters
  - Return text responses
  
- Required Parameters:
  - source_path: Path to local directory OR GitHub repository URL
  - question: The user's query about the code
  - github_token: (Optional) Only required for GitHub repositories
  - base_url: (Optional) Ollama service URL, defaults to http://localhost:11434

### 4. Performance Requirements
- Response time: < 5 seconds for typical queries
- Memory usage: < 1GB for typical repositories
- Support repositories up to 100MB in size

### 5. Error Handling
- Clear error messages for:
  - Invalid repository paths
  - Missing GitHub tokens
  - Ollama service connection issues
  - Embedding generation failures
  - Vector database errors

## Technical Requirements

### Dependencies
- embedchain[github]: For repository loading and RAG functionality
- chromadb: For vector database operations
- Required Python version: 3.8+

### Configuration
- No persistent configuration required
- All settings passed through MCP tool parameters
- Support for environment variables for sensitive data

### Security
- No persistent storage of repository content
- Temporary vector databases cleaned up after use
- GitHub tokens handled securely
- Local file system access limited to specified directories

## Integration Requirements

### MCP Server
- Tool registration in MCP settings
- Standard JSON input/output interface
- Error reporting through MCP protocol

### Local Environment
- Ollama service must be running and accessible
- Sufficient disk space for temporary vector databases
- Adequate memory for embedding operations

## Future Considerations
- Support for additional repository sources (GitLab, Bitbucket)
- Caching mechanism for frequently accessed repositories
- Support for repository updates/changes
- Advanced query capabilities (code search, function finding)
