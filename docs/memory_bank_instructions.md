# Memory Bank Instructions for Cline/RooCode

## Overview

You have access to a memory bank MCP tool that helps you store and retrieve knowledge about code. This tool allows you to:
1. Store summaries of code you examine
2. Update knowledge when code changes
3. Find relevant code for tasks
4. Access context efficiently

## When to Store Knowledge

Store knowledge when you:
1. Examine a new file or directory
2. Discover important code patterns
3. Learn about component relationships
4. Understand implementation details

Example knowledge entry:
```python
add_knowledge(
    path="src/auth/login.py",
    summary="Authentication handler implementing JWT-based login/logout. Uses bcrypt for password hashing and includes session management.",
    metadata={
        "type": "file",
        "related": ["auth/session.py", "models/user.py"],
        "patterns": ["JWT authentication", "Password hashing"]
    }
)
```

## When to Update Knowledge

Update knowledge when:
1. Code semantics change
2. You discover new relationships
3. Implementation patterns evolve
4. The user requests re-evaluation

Example update:
```python
update_knowledge(
    path="src/auth/login.py",
    new_summary="Enhanced authentication handler with OAuth support and rate limiting.",
    metadata={
        "type": "file",
        "related": ["auth/session.py", "models/user.py", "auth/oauth.py"],
        "patterns": ["OAuth", "Rate limiting", "JWT authentication"]
    }
)
```

## How to Generate Summaries

When creating summaries:
1. Focus on functionality and purpose
2. Identify key patterns and relationships
3. Note important dependencies
4. Keep descriptions concise but informative

Good summary examples:
```
✓ "User authentication service handling login, session management, and access control. Implements JWT tokens and integrates with OAuth providers."

✓ "Core data validation module providing schema validation, sanitization, and type checking. Used across all data input paths."

✓ "Background job processing system using Redis for queue management. Handles task scheduling, retries, and error reporting."
```

## How to Find Relevant Code

When you need to find code:
1. Describe what you're looking for in natural language
2. Use the search_knowledge function
3. Consider the context of your task
4. Look for related components

Example searches:
```python
# Finding authentication code
results = search_knowledge("user authentication and session management")

# Looking for data validation
results = search_knowledge("input validation and sanitization")

# Finding specific patterns
results = search_knowledge("background job processing with Redis")
```

## Getting Task Context

When starting a task:
1. Use get_relevant_context to find related code
2. Consider all returned components
3. Look for relationships between components
4. Use metadata for additional context

Example:
```python
# Starting a password reset feature
context = get_relevant_context("implement password reset functionality")
for entry in context:
    print(f"Relevant file: {entry.path}")
    print(f"Summary: {entry.content}")
    print(f"Relevance: {entry.relevance}")
```

## Best Practices

1. Knowledge Storage
   - Store clear, focused summaries
   - Include important relationships
   - Note implementation patterns
   - Keep metadata current

2. Knowledge Updates
   - Update promptly when code changes
   - Maintain relationship information
   - Preserve important patterns
   - Track evolution of components

3. Knowledge Retrieval
   - Use specific search terms
   - Consider task context
   - Look for related components
   - Check metadata for insights

4. Context Management
   - Pull relevant documentation
   - Focus on task-specific needs
   - Consider component relationships
   - Use metadata effectively

Remember: Building and maintaining this knowledge base helps you understand the codebase better and makes your assistance more effective.