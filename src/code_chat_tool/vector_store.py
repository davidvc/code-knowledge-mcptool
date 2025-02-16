"""
Vector Store Module for Chat with Code Repository Tool

This module defines the base VectorStore interface and provides an in-memory transient implementation.
"""

import os
import json
import pickle
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional

@dataclass
class SearchResult:
    """Result from a vector store search."""
    segment: 'CodeSegment'  # Forward reference
    score: float

class VectorStore(ABC):
    @abstractmethod
    def store(self, embeddings: List[Tuple[np.ndarray, 'CodeSegment']]) -> None:
        """
        Store a list of embeddings with their associated code segments.
        
        Args:
            embeddings: List of tuples containing (embedding vector, code segment)
        """
        pass

    @abstractmethod
    def search(self, query: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """
        Search for embeddings similar to the query.
        
        Args:
            query: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of SearchResult objects sorted by similarity score
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up the stored embeddings."""
        pass

class TransientVectorStore(VectorStore):
    def __init__(self):
        self.embeddings: List[np.ndarray] = []
        self.segments: List['CodeSegment'] = []

    def store(self, embeddings: List[Tuple[np.ndarray, 'CodeSegment']]) -> None:
        """Store embeddings and their associated code segments."""
        for embedding, segment in embeddings:
            self.embeddings.append(embedding)
            self.segments.append(segment)

    def search(self, query: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """
        Search for similar code segments using cosine similarity.
        
        Args:
            query: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of SearchResults sorted by similarity score (highest first)
        """
        if not self.embeddings:
            return []
            
        # Convert list to numpy array for vectorized operations
        embeddings_array = np.array(self.embeddings)
        
        # Compute cosine similarity
        # Normalize vectors
        query_norm = query / np.linalg.norm(query)
        embeddings_norm = embeddings_array / np.linalg.norm(embeddings_array, axis=1)[:, np.newaxis]
        
        # Compute dot product of normalized vectors (cosine similarity)
        similarities = np.dot(embeddings_norm, query_norm)
        
        # Get indices of top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Create SearchResult objects
        results = []
        for idx in top_indices:
            results.append(SearchResult(
                segment=self.segments[idx],
                score=float(similarities[idx])
            ))
            
        return results

    def cleanup(self) -> None:
        """Clean up stored embeddings and segments."""
        self.embeddings = []
        self.segments = []

class PersistentVectorStore(VectorStore):
    """Persistent vector store implementation that saves embeddings to disk."""
    
    def __init__(self, storage_dir: Path):
        """
        Initialize persistent vector store.
        
        Args:
            storage_dir: Directory to store embeddings and metadata
        """
        self.storage_dir = storage_dir
        self.embeddings_file = storage_dir / "embeddings.npy"
        self.segments_file = storage_dir / "segments.pkl"
        self.metadata_file = storage_dir / "metadata.json"
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing data if available
        self.embeddings: List[np.ndarray] = []
        self.segments: List['CodeSegment'] = []
        self._load()

    def _load(self) -> None:
        """Load embeddings and segments from disk if they exist."""
        try:
            if self.embeddings_file.exists():
                self.embeddings = list(np.load(self.embeddings_file, allow_pickle=True))
            if self.segments_file.exists():
                with open(self.segments_file, 'rb') as f:
                    self.segments = pickle.load(f)
        except Exception as e:
            print(f"Warning: Failed to load existing data: {e}")
            self.embeddings = []
            self.segments = []

    def _save(self) -> None:
        """Save embeddings and segments to disk."""
        try:
            # Save embeddings as numpy array
            np.save(self.embeddings_file, np.array(self.embeddings))
            
            # Save segments using pickle
            with open(self.segments_file, 'wb') as f:
                pickle.dump(self.segments, f)
                
            # Save metadata
            with open(self.metadata_file, 'w') as f:
                json.dump({
                    'count': len(self.embeddings),
                    'dimension': len(self.embeddings[0]) if self.embeddings else 0
                }, f)
        except Exception as e:
            print(f"Warning: Failed to save data: {e}")

    def store(self, embeddings: List[Tuple[np.ndarray, 'CodeSegment']]) -> None:
        """Store embeddings and their associated code segments."""
        for embedding, segment in embeddings:
            self.embeddings.append(embedding)
            self.segments.append(segment)
        self._save()

    def search(self, query: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        """
        Search for similar code segments using cosine similarity.
        
        Args:
            query: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of SearchResults sorted by similarity score (highest first)
        """
        if not self.embeddings:
            return []
            
        # Convert list to numpy array for vectorized operations
        embeddings_array = np.array(self.embeddings)
        
        # Compute cosine similarity
        # Normalize vectors
        query_norm = query / np.linalg.norm(query)
        embeddings_norm = embeddings_array / np.linalg.norm(embeddings_array, axis=1)[:, np.newaxis]
        
        # Compute dot product of normalized vectors (cosine similarity)
        similarities = np.dot(embeddings_norm, query_norm)
        
        # Get indices of top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Create SearchResult objects
        results = []
        for idx in top_indices:
            results.append(SearchResult(
                segment=self.segments[idx],
                score=float(similarities[idx])
            ))
            
        return results

    def cleanup(self) -> None:
        """Clean up stored embeddings and segments."""
        self.embeddings = []
        self.segments = []
        
        # Remove files
        try:
            if self.embeddings_file.exists():
                os.remove(self.embeddings_file)
            if self.segments_file.exists():
                os.remove(self.segments_file)
            if self.metadata_file.exists():
                os.remove(self.metadata_file)
        except Exception as e:
            print(f"Warning: Failed to remove files during cleanup: {e}")
