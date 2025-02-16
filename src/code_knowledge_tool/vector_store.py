"""Vector store implementation for memory bank."""
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class CodeSegment:
    """Represents a segment of code with its path and content."""
    path: str
    content: str

@dataclass
class SearchResult:
    """Represents a search result with similarity score."""
    segment: CodeSegment
    score: float

class VectorStore:
    """Base class for vector storage."""
    
    def add(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Add a new embedding with associated content."""
        raise NotImplementedError

    def update(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Update an existing embedding."""
        raise NotImplementedError

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """Search for similar embeddings."""
        raise NotImplementedError

    def get(self, path: str) -> Optional[Tuple[np.ndarray, CodeSegment]]:
        """Get embedding and content for a path."""
        raise NotImplementedError

class InMemoryVectorStore(VectorStore):
    """In-memory vector store for testing."""
    
    def __init__(self):
        """Initialize empty storage."""
        self._embeddings: Dict[str, np.ndarray] = {}
        self._segments: Dict[str, CodeSegment] = {}

    def add(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Add a new embedding with associated content."""
        if path in self._embeddings:
            raise ValueError(f"Path already exists: {path}")
            
        self._embeddings[path] = embedding
        self._segments[path] = CodeSegment(path=path, content=content)

    def update(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Update an existing embedding."""
        if path not in self._embeddings:
            raise ValueError(f"Path not found: {path}")
            
        self._embeddings[path] = embedding
        self._segments[path] = CodeSegment(path=path, content=content)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """Search for similar embeddings."""
        if not self._embeddings:
            return []

        results = []
        for path, embedding in self._embeddings.items():
            # Compute cosine similarity
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            results.append(SearchResult(
                segment=self._segments[path],
                score=float(similarity)
            ))

        # Sort by similarity score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def get(self, path: str) -> Optional[Tuple[np.ndarray, CodeSegment]]:
        """Get embedding and content for a path."""
        if path not in self._embeddings:
            return None
        return (self._embeddings[path], self._segments[path])

class PersistentVectorStore(VectorStore):
    """Persistent vector store using files."""
    
    def __init__(self, storage_dir: Path):
        """Initialize with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._load_or_init_storage()

    def _load_or_init_storage(self) -> None:
        """Load existing storage or initialize new."""
        self._embeddings = {}
        self._segments = {}
        
        embeddings_file = self.storage_dir / "embeddings.npy"
        segments_file = self.storage_dir / "segments.json"
        
        if embeddings_file.exists() and segments_file.exists():
            # Load existing storage
            self._load_storage()
        else:
            # Initialize new storage
            self._save_storage()

    def _load_storage(self) -> None:
        """Load storage from files."""
        # Implementation details for loading from files
        pass

    def _save_storage(self) -> None:
        """Save storage to files."""
        # Implementation details for saving to files
        pass

    def add(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Add a new embedding with associated content."""
        if path in self._embeddings:
            raise ValueError(f"Path already exists: {path}")
            
        self._embeddings[path] = embedding
        self._segments[path] = CodeSegment(path=path, content=content)
        self._save_storage()

    def update(self, embedding: np.ndarray, path: str, content: str) -> None:
        """Update an existing embedding."""
        if path not in self._embeddings:
            raise ValueError(f"Path not found: {path}")
            
        self._embeddings[path] = embedding
        self._segments[path] = CodeSegment(path=path, content=content)
        self._save_storage()

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """Search for similar embeddings."""
        if not self._embeddings:
            return []

        results = []
        for path, embedding in self._embeddings.items():
            # Compute cosine similarity
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            results.append(SearchResult(
                segment=self._segments[path],
                score=float(similarity)
            ))

        # Sort by similarity score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def get(self, path: str) -> Optional[Tuple[np.ndarray, CodeSegment]]:
        """Get embedding and content for a path."""
        if path not in self._embeddings:
            return None
        return (self._embeddings[path], self._segments[path])
