# Active Context

## Current Focus
Optimizing embedding generation performance for the Chat with Code Repository Tool.

## Recent Decisions
1. **Language Choice**: Python selected due to its robust ecosystem for ML/NLP tasks, rapid prototyping capabilities, and ease of integrating with embedding tools.
2. **Architecture Decisions**:
   - Local-only operation for simplicity and security.
   - Switching from Ollama to sentence-transformers for embeddings due to performance concerns.
   - Abstracted vector storage interface with both transient and persistent implementations.
   - MCP tool integration for Cline compatibility.
3. **Testing Strategy**:
   - Integration testing using real-world codebases:
     - Flask for Python capabilities.
     - Commons Lang for Java capabilities (current focus).
   - Use of an abstract evaluator interface for response quality assessment via LLMs.
4. **Performance Optimizations**:
   - Implemented batched embedding generation.
   - Switching to sentence-transformers which is:
     - Specifically designed for embeddings
     - Much faster than general-purpose models
     - Memory efficient
     - Supports efficient batching
     - Uses compact models (~100MB)

## In Progress
- Implementing sentence-transformers based embedding.
- Optimizing embedding generation performance.
- Testing with large repositories.

## Next Steps
1. Complete sentence-transformers integration.
2. Test performance improvements.
3. Implement persistent storage for embeddings.
4. Add query handling and response generation.
5. Add support for incremental updates.

## Future Plans
- **Multi-Repository Support**: Expand the system to handle multiple repositories by assigning unique collections based on each repository's folder name; enforce uniqueness and detect duplicates.
- **Incremental Indexing**: Create mechanisms to update an existing repository index without fully rebuilding it, making the indexing process more efficient when only small changes occur.
- **Caching**: Add caching mechanisms to further improve performance.
