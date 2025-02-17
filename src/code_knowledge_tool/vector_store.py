"""Vector store implementation with persistent storage."""
from pathlib import Path
import json
import tempfile
import shutil
import logging
from typing import List, Optional, Dict, Tuple, Any
import numpy as np
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class CodeSegment:
    """Represents a segment of code with its path, content, and metadata."""
    path: str
    content: str
    metadata: Dict[str, Any]

@dataclass
class SearchResult:
    """Represents a search result with similarity score."""
    segment: CodeSegment
    score: float

class VectorStore:
    """Base class for vector storage."""
    
    def add(self, embedding: np.ndarray, path: str, content: str, metadata: Dict[str, Any]) -> None:
        """Add a new embedding with associated content."""
        raise NotImplementedError
    
    def update(self, embedding: np.ndarray, path: str, content: str, metadata: Dict[str, Any]) -> None:
        """Update an existing embedding."""
        raise NotImplementedError
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """Search for similar embeddings."""
        raise NotImplementedError
    
    def get(self, path: str) -> Optional[Tuple[np.ndarray, CodeSegment]]:
        """Get embedding and content for a path."""
        raise NotImplementedError

class PersistentVectorStore(VectorStore):
    """Persistent vector store using atomic file operations."""
    
    def __init__(self, storage_dir: Path):
        """Initialize with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._embeddings: Dict[str, np.ndarray] = {}
        self._segments: Dict[str, CodeSegment] = {}
        self._load_or_init_storage()
    
    def _load_or_init_storage(self) -> None:
        """Load existing storage or initialize new."""
        try:
            self._load_storage()
        except Exception as e:
            logger.error(f"Error loading storage: {str(e)}")
            logger.info("Initializing new storage")
            self._save_storage()
    
    def _load_storage(self) -> None:
        """Load storage from files with validation."""
        embeddings_file = self.storage_dir / "embeddings.npy"
        segments_file = self.storage_dir / "segments.json"
        
        if not (embeddings_file.exists() and segments_file.exists()):
            logger.info("No existing storage found")
            return
        
        try:
            # Load embeddings
            embeddings_data = np.load(embeddings_file, allow_pickle=True)
            embeddings_dict = {
                path: embedding for path, embedding in embeddings_data
            }
            
            # Load segments
            with open(segments_file, 'r') as f:
                segments_data = json.load(f)
            
            # Validate data consistency
            if set(embeddings_dict.keys()) != set(segments_data.keys()):
                raise ValueError("Inconsistent storage: embeddings and segments don't match")
            
            # Create CodeSegment objects
            segments_dict = {
                path: CodeSegment(
                    path=path,
                    content=data["content"],
                    metadata=data["metadata"]
                )
                for path, data in segments_data.items()
            }
            
            self._embeddings = embeddings_dict
            self._segments = segments_dict
            logger.info(f"Loaded {len(self._embeddings)} entries from storage")
            
        except Exception as e:
            logger.error(f"Error loading storage: {str(e)}")
            raise
    
    def _save_storage(self) -> None:
        """Save storage to files atomically."""
        # Create temporary directory for atomic writes
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            try:
                # Save embeddings to temp file
                embeddings_data = [
                    (path, embedding) 
                    for path, embedding in self._embeddings.items()
                ]
                temp_embeddings = temp_path / "embeddings.npy"
                np.save(temp_embeddings, embeddings_data)
                
                # Save segments to temp file
                segments_data = {
                    path: {
                        "content": segment.content,
                        "metadata": segment.metadata
                    }
                    for path, segment in self._segments.items()
                }
                temp_segments = temp_path / "segments.json"
                with open(temp_segments, 'w') as f:
                    json.dump(segments_data, f, indent=2)
                
                # Move files to final location atomically
                shutil.move(str(temp_embeddings), str(self.storage_dir / "embeddings.npy"))
                shutil.move(str(temp_segments), str(self.storage_dir / "segments.json"))
                
                logger.info(f"Saved {len(self._embeddings)} entries to storage")
                
            except Exception as e:
                logger.error(f"Error saving storage: {str(e)}")
                raise
    
    def add(self, embedding: np.ndarray, path: str, content: str, metadata: Dict[str, Any]) -> None:
        """Add a new embedding with associated content."""
        if path in self._embeddings:
            raise ValueError(f"Path already exists: {path}")
        
        try:
            self._embeddings[path] = embedding
            self._segments[path] = CodeSegment(
                path=path,
                content=content,
                metadata=metadata
            )
            self._save_storage()
        except Exception as e:
            # Rollback on error
            self._embeddings.pop(path, None)
            self._segments.pop(path, None)
            raise ValueError(f"Failed to add knowledge: {str(e)}")
    
    def update(self, embedding: np.ndarray, path: str, content: str, metadata: Dict[str, Any]) -> None:
        """Update an existing embedding."""
        if path not in self._embeddings:
            raise ValueError(f"Path not found: {path}")
        
        # Store old values for rollback
        old_embedding = self._embeddings[path]
        old_segment = self._segments[path]
        
        try:
            self._embeddings[path] = embedding
            self._segments[path] = CodeSegment(
                path=path,
                content=content,
                metadata=metadata
            )
            self._save_storage()
        except Exception as e:
            # Rollback on error
            self._embeddings[path] = old_embedding
            self._segments[path] = old_segment
            raise ValueError(f"Failed to update knowledge: {str(e)}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """Search for similar embeddings."""
        if not self._embeddings:
            return []
        
        try:
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
            
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []
    
    def get(self, path: str) -> Optional[Tuple[np.ndarray, CodeSegment]]:
        """Get embedding and content for a path."""
        try:
            if path not in self._embeddings:
                return None
            return (self._embeddings[path], self._segments[path])
        except Exception as e:
            logger.error(f"Error retrieving entry: {str(e)}")
            return None
    
    def cleanup(self) -> None:
        """Clean up storage files."""
        try:
            if self.storage_dir.exists():
                shutil.rmtree(self.storage_dir)
            logger.info("Storage cleaned up successfully")
        except Exception as e:
            logger.error(f"Error cleaning up storage: {str(e)}")
            raise
