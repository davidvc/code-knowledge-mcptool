"""Test fixtures for memory bank testing."""
from typing import Dict, List

# Sample knowledge entries for testing
TEST_KNOWLEDGE = [
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
    },
    {
        "path": "src/models/user.py",
        "summary": "User model with profile management, permissions, and authentication state.",
        "metadata": {
            "type": "file",
            "last_updated": "2024-02-16",
            "related": ["auth/login.py", "models/profile.py"]
        }
    },
    {
        "path": "src/auth/session.py",
        "summary": "Session management implementation with timeout handling and token refresh.",
        "metadata": {
            "type": "file",
            "last_updated": "2024-02-16",
            "related": ["auth/login.py"]
        }
    }
]

# Sample memory bank markdown content
TEST_MARKDOWN = {
    "projectbrief.md": """# Test Project Brief
Authentication system implementing secure user management with JWT support.
Features include:
- User authentication
- Session management
- Access control
- Profile management""",

    "activeContext.md": """# Test Active Context
Currently implementing session management with focus on:
- JWT token handling
- Session timeouts
- Refresh token logic""",

    "systemPatterns.md": """# Test System Patterns
Authentication follows these patterns:
- JWT-based authentication
- Role-based access control
- Stateless session management"""
}

# Test queries and expected matches
TEST_QUERIES = [
    {
        "query": "authentication jwt",
        "expected_paths": ["src/auth/login.py", "src/auth/"]
    },
    {
        "query": "user profile",
        "expected_paths": ["src/models/user.py"]
    },
    {
        "query": "session management",
        "expected_paths": ["src/auth/login.py", "src/auth/"]
    }
]

# Test tasks and expected context
TEST_TASKS = [
    {
        "task": "implement password reset",
        "expected_context": ["src/auth/login.py", "src/models/user.py"]
    },
    {
        "task": "add session timeout",
        "expected_context": ["src/auth/login.py", "src/auth/session.py"]
    }
]