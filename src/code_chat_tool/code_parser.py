"""
Code Parser Module for Chat with Code Repository Tool

This module provides functionality to parse a local repository and extract code files.
"""

import os
from dataclasses import dataclass

def extract_java_info(content: str) -> tuple[str, str]:
    """Extract class name and documentation from Java file content."""
    lines = content.split('\n')
    doc_lines = []
    class_name = ""
    
    # Collect documentation and find class name
    for line in lines:
        line = line.strip()
        # Skip empty lines and package declarations
        if not line or line.startswith('package '):
            continue
        # Collect documentation comments
        if line.startswith('/*') or line.startswith('*') or line.startswith('*/'):
            doc_lines.append(line)
        # Look for class declaration
        elif 'class ' in line or 'interface ' in line:
            parts = line.split(' ')
            for i, part in enumerate(parts):
                if part in ('class', 'interface') and i + 1 < len(parts):
                    class_name = parts[i + 1].split('{')[0].strip()
                    break
            break
        
    doc_text = '\n'.join(doc_lines)
    return class_name, doc_text

@dataclass
class CodeSegment:
    path: str
    content: str
    name: str = ""      # Class/interface name
    doc_text: str = ""  # Documentation text

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
                name = ""
                doc_text = ""
                full_path = os.path.join(root, file)
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract additional info for Java files
                    if ext == '.java':
                        name, doc_text = extract_java_info(content)
                    
                    code_files.append(CodeSegment(path=full_path, content=content, name=name, doc_text=doc_text))
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
