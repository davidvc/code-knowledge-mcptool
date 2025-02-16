"""Code parsing and repository traversal functionality."""
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Set


@dataclass
class CodeSegment:
    """Represents a segment of code with relevant metadata."""
    
    content: str
    file_path: Path
    start_line: int
    end_line: int
    language: Optional[str] = None


class CodeParser:
    """Handles traversal and parsing of code repositories."""

    def __init__(
        self,
        ignore_patterns: Optional[List[str]] = None,
        max_file_size: int = 1024 * 1024,  # 1MB
    ):
        """Initialize the code parser.
        
        Args:
            ignore_patterns: List of glob patterns to ignore
            max_file_size: Maximum file size to process in bytes
        """
        self.ignore_patterns = set(ignore_patterns or [])
        self.max_file_size = max_file_size
        self._supported_extensions: Set[str] = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c',
            '.h', '.hpp', '.cs', '.rb', '.go', '.rs',
            '.php', '.scala', '.kt', '.swift'
        }
    
    def should_process_file(self, path: Path) -> bool:
        """Check if a file should be processed.
        
        Args:
            path: Path to the file
            
        Returns:
            True if the file should be processed, False otherwise
        """
        # Check file extension
        if path.suffix not in self._supported_extensions:
            return False
            
        # Check file size
        if path.stat().st_size > self.max_file_size:
            return False
            
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if path.match(pattern):
                return False
                
        return True
    
    def parse_repository(self, repo_path: Path) -> Iterator[CodeSegment]:
        """Parse all code files in a repository.
        
        Args:
            repo_path: Path to the repository root
            
        Yields:
            CodeSegment instances for each parsed code segment
        """
        for file_path in repo_path.rglob('*'):
            if not file_path.is_file() or not self.should_process_file(file_path):
                continue
                
            yield from self.parse_file(file_path)
    
    def parse_file(self, file_path: Path) -> Iterator[CodeSegment]:
        """Parse a single code file into segments.
        
        Args:
            file_path: Path to the code file
            
        Yields:
            CodeSegment instances for the parsed file
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # TODO: Implement more sophisticated segmentation
            # For now, treat whole file as one segment
            yield CodeSegment(
                content=content,
                file_path=file_path,
                start_line=1,
                end_line=len(content.splitlines()),
                language=file_path.suffix[1:]  # Remove leading dot
            )
            
        except (UnicodeDecodeError, OSError) as e:
            # Log error but continue processing other files
            print(f"Error processing {file_path}: {str(e)}")
            return
