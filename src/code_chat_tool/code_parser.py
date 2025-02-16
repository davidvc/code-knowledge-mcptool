"""
Code Parser Module for Chat with Code Repository Tool

This module provides functionality to parse a local repository and extract code files.
"""

import os
from dataclasses import dataclass

@dataclass
class CodeSegment:
    path: str
    content: str

def parse_repository(repo_path):
    """
    Parse the repository located at repo_path.
    Recursively scans the directory for files with code-related extensions,
    reads them, and returns a list of CodeSegment objects.

    Returns:
        List[CodeSegment]: A list where each item is a CodeSegment with:
            - path: the full file path
            - content: the content of the file
    """
    code_files = []
    # Allowed file extensions for code files. Extend this set as needed.
    allowed_extensions = {'.py', '.js', '.java', '.txt', '.md', '.c', '.cpp', '.h', '.html', '.css'}
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in allowed_extensions:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    code_files.append(CodeSegment(path=full_path, content=content))
                except Exception as e:
                    # If a file cannot be read, skip it.
                    pass
    return code_files

class CodeParser:
    """
    Wrapper class for parsing code repositories.
    Provides an instance method to parse a repository by calling the module-level function.
    """
    def parse_repository(self, repo_path):
        return parse_repository(repo_path)
