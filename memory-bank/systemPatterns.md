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

## Testing Strategy

### Test Data
Instead of using real codebases, we'll use crafted test data:

1. Knowledge Entries
```python
test_knowledge = [
    {
        "path": "src/auth/login.py",
        "summary": "Handles user authentication with JWT tokens. Implements login, logout, and session management.",
        "metadata": {
            "type": "file",
            "last_updated": "2024-02-16",
            "related": ["auth/session.py", "models/user.py"]
        }
    },
    {
        "path": "src/auth/",
        "summary": "Authentication module handling user identity, sessions, and access control.",
        "metadata": {
            "type": "directory",
            "components": ["login.py", "session.py", "permissions.py"]
        }
    }
]
```

2. Memory Bank Content
```markdown
# Test Project Brief
Authentication system with JWT support...

# Test Active Context
Currently implementing session management...
```

### Test Scenarios

1. Knowledge Operations
```python
# Adding Knowledge
add_knowledge("src/auth/login.py", "Authentication handler...")

# Updating Knowledge
update_knowledge("src/auth/login.py", "Updated auth handler...")

# Searching Knowledge
results = search_knowledge("authentication jwt")
```

2. Context Retrieval
```python
# Task-specific Context
context = get_relevant_context("implement password reset")

# Documentation Access
docs = get_markdown_content("projectbrief.md")
```

### Test Structure
1. Unit Tests
   - Knowledge operations
   - Context retrieval
   - RAG functionality
   - Update mechanisms

2. Integration Tests
   - End-to-end workflows
   - Combined operations
   - Context building

3. Consistency Tests
   - Update validation
   - Knowledge integrity
   - Context relevance

### Test Environment
- In-memory vector store
- Predefined test data
- Controlled context
- Simulated updates
