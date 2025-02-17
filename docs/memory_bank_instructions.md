# Memory Bank Instructions for Cline/RooCode

## Overview

You have access to a memory bank MCP server that helps you store and retrieve knowledge about code. This server provides tools to:
1. Store and manage knowledge entries
2. Search for relevant information
3. Get context for tasks
4. Update existing knowledge
5. List available entries

## When to Store Knowledge

Store knowledge when you:
1. Examine a new file or directory
2. Discover important code patterns
3. Learn about component relationships
4. Understand implementation details

Example knowledge entry:
```json
// Tool: add_knowledge
{
    "path": "src/auth/login.py",
    "content": "Authentication handler implementing JWT-based login/logout. Uses bcrypt for password hashing and includes session management.",
    "metadata": {
        "type": "file",
        "category": "authentication",
        "last_updated": "2024-02-17",
        "related": ["auth/session.py", "models/user.py"],
        "patterns": ["JWT authentication", "Password hashing"]
    }
}

// Response
{
    "success": true
}
```

## When to Update Knowledge

Update knowledge when:
1. Code semantics change
2. You discover new relationships
3. Implementation patterns evolve
4. The user requests re-evaluation

Example update:
```json
// Tool: update_knowledge
{
    "path": "src/auth/login.py",
    "content": "Enhanced authentication handler with OAuth support and rate limiting.",
    "metadata": {
        "type": "file",
        "category": "authentication",
        "last_updated": "2024-02-18",
        "related": ["auth/session.py", "models/user.py", "auth/oauth.py"],
        "patterns": ["OAuth", "Rate limiting", "JWT authentication"]
    }
}

// Response
{
    "success": true
}
```

## How to Generate Content

When creating content:
1. Focus on functionality and purpose
2. Identify key patterns and relationships
3. Note important dependencies
4. Keep descriptions concise but informative

Good content examples:
```markdown
✓ # Authentication Service
   Handles user authentication with JWT tokens and OAuth integration.
   Includes session management and access control.
   Integrates with multiple OAuth providers.

✓ # Data Validation Module
   Core validation system providing schema validation and sanitization.
   Used across all data input paths.
   Implements type checking and custom validators.

✓ # Background Processing
   Job processing system using Redis queues.
   Handles task scheduling, retries, and reporting.
   Implements error recovery and monitoring.
```

## How to Find Relevant Code

When you need to find code:
1. Describe what you're looking for in natural language
2. Use the search_knowledge tool
3. Consider the context of your task
4. Look for related components

Example searches:
```json
// Tool: search_knowledge
{
    "query": "user authentication and session management",
    "limit": 5
}

// Response
{
    "results": [
        {
            "path": "src/auth/login.py",
            "content": "Authentication handler implementing JWT...",
            "score": 0.92
        },
        {
            "path": "src/auth/session.py",
            "content": "Session management system...",
            "score": 0.85
        }
    ]
}
```

## Getting Task Context

When starting a task:
1. Use get_context to find related knowledge
2. Consider all returned entries
3. Look for relationships between components
4. Use metadata for additional context

Example:
```json
// Tool: get_context
{
    "task": "implement password reset functionality",
    "limit": 3
}

// Response
{
    "context": [
        {
            "path": "src/auth/login.py",
            "content": "Authentication handler...",
            "relevance": 0.95
        },
        {
            "path": "src/auth/password.py",
            "content": "Password management...",
            "relevance": 0.88
        }
    ]
}
```

## Storage and Persistence

Knowledge is stored persistently in your repository so you can use it across sessions as a persistent
store of knowledge about the project and the code base.

## Best Practices

1. Knowledge Storage
   - Store clear, focused content
   - Include important relationships
   - Note implementation patterns
   - Keep metadata current
   - Use consistent formatting

2. Knowledge Updates
   - Update promptly when code changes
   - Maintain relationship information
   - Preserve important patterns
   - Track evolution of components
   - Version metadata appropriately

3. Knowledge Retrieval
   - Use specific search terms
   - Consider task context
   - Look for related components
   - Check metadata for insights
   - Leverage similarity search

4. Context Management
   - Pull relevant documentation
   - Focus on task-specific needs
   - Consider component relationships
   - Use metadata effectively
   - Track knowledge evolution

Remember: The knowledge base is persistent and can be checked into your repository, helping maintain a shared understanding of the codebase across the team.