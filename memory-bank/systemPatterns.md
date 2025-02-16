# System Patterns

## Memory Bank Architecture

### Unified Knowledge System
The memory bank combines two complementary storage approaches:

1. Vector Database (In Project)
   - File and directory summaries
   - Component relationships
   - Implementation patterns
   - Supports updates and evolution
   - Version control optional

2. Markdown Documentation
   - Project briefs
   - Active context
   - System patterns
   - Progress tracking
   - Stored in filesystem

### Knowledge Management

#### Dynamic Updates
- Knowledge can be updated when:
  * Code semantics change
  * New understanding is gained
  * User requests re-evaluation
  * Implementation patterns evolve
- Updates preserve knowledge history
- Maintains consistency across related entries

#### RAG-Based Context Retrieval
- Contextual information fetched as needed
- Relevant documentation pulled for specific tasks
- Reduces context token usage
- More efficient API utilization
- Supports focused understanding

### Storage Structure
```
project-root/
  ├── memory-bank/
  │   ├── markdown/        # Documentation
  │   │   ├── projectbrief.md
  │   │   ├── activeContext.md
  │   │   └── ...
  │   └── knowledge/      # Vector store
  │       ├── embeddings.npy
  │       ├── metadata.json
  │       └── segments.json
```

### MCP Tool Interface

#### Knowledge Operations
1. Addition
   ```python
   add_knowledge(path: str, summary: str, metadata: dict)
   ```

2. Update
   ```python
   update_knowledge(path: str, new_summary: str, metadata: dict)
   ```

3. Search
   ```python
   search_knowledge(query: str) -> List[KnowledgeEntry]
   ```

4. Context Retrieval
   ```python
   get_relevant_context(task: str) -> List[ContextEntry]
   ```

### Cline/RooCode Integration

#### Specialized Instructions
- Stored in .clinerules or configuration
- Guides knowledge building and updates
- Defines when to re-evaluate
- Sets context retrieval patterns

Example Prompt:
```
As you explore code:
1. Generate concise summaries focusing on:
   - Component purpose
   - Key functionality
   - Important patterns
   - Critical relationships

2. Update knowledge when you:
   - Discover new patterns
   - Find changed semantics
   - Receive user requests
   - Learn new relationships

3. Use RAG for context:
   - Pull relevant documentation
   - Focus on task-specific needs
   - Maintain efficiency
```

## Usage Patterns

### Knowledge Building
1. Code Exploration
   - Generate summaries
   - Store understanding
   - Track relationships

2. Knowledge Updates
   - Monitor semantic changes
   - Handle user requests
   - Maintain consistency
   - Preserve history

3. Context Management
   - RAG-based retrieval
   - Task-specific focus
   - Efficient token usage

### Benefits
1. Dynamic Knowledge
   - Updateable understanding
   - Evolution support
   - Consistency maintenance

2. Efficient Context
   - RAG-based retrieval
   - Focused information
   - Reduced token usage

3. Team Support
   - Shared understanding
   - Knowledge evolution
   - Collaborative learning

## Implementation Strategy

### Knowledge Format
1. Summaries
   - Concise descriptions
   - Key functionality
   - Important patterns
   - Critical relationships

2. Metadata
   - Last updated
   - Update reason
   - Related entries
   - Version information

3. Context Links
   - Related documentation
   - Connected components
   - Usage patterns
