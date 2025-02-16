# Active Context

## Current Focus
Initial project setup and requirements definition for the Chat with Code Repository Tool.

## Recent Decisions
1. **Language Choice**: Python selected over Java due to:
   - Better ecosystem for ML/NLP tasks
   - Simpler integration with Chroma and embedding tools
   - Faster prototyping capabilities
   - No need for Git integration complexity

2. **Architecture Decisions**:
   - Local-only operation for simplicity and security
   - Direct integration with Ollama service
   - Abstracted vector storage interface:
     - Initial implementation: temporary per session
     - Designed for easy switch to persistence
   - MCP tool integration for Cline compatibility

## In Progress
- Requirements documentation
- System architecture design
- Technical specification
- Memory bank initialization

## Next Steps
1. Set up project structure
2. Implement core MCP server functionality
3. Create code parsing system
4. Integrate with Ollama for embeddings
5. Implement Chroma vector storage
6. Add query handling and response generation

## Open Questions
- Optimal chunk size for code parsing
- Best practices for temporary storage cleanup
- Performance optimization strategies
- Error handling best practices

## Current Challenges
- Ensuring consistent embedding quality
- Managing memory usage for large repositories
- Optimizing response times
- Handling different code file types effectively
