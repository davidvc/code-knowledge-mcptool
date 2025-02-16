"""Vector storage abstraction and implementations."""
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

# Type variables for flexibility
E = TypeVar('E')  # Embedding type
R = TypeVar('R')  # Result type

class VectorStore(ABC, Generic[E, R]):
    """Abstract base class for vector storage implementations."""
    
    @abstractmethod
    def store(self, embeddings: List[E]) -> None:
        """Store embeddings in the vector database.
        
        Args:
            embeddings: List of embeddings to store
        """
        pass
    
    @abstractmethod
    def search(self, query: E) -> List[R]:
        """Search for similar embeddings.
        
        Args:
            query: Query embedding
            
        Returns:
            List of results ordered by similarity
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the store."""
        pass

class TransientVectorStore(VectorStore[E, R]):
    """Temporary in-memory vector store implementation using Chroma."""
    
    def __init__(self):
        """Initialize temporary vector store."""
        # TODO: Initialize Chroma client with temporary persistence
        pass
    
    def store(self, embeddings: List[E]) -> None:
        """Store embeddings in temporary Chroma instance."""
        # TODO: Implement storing embeddings
        pass
    
    def search(self, query: E) -> List[R]:
        """Search temporary Chroma instance."""
        # TODO: Implement similarity search
        pass
    
    def cleanup(self) -> None:
        """Clean up temporary storage."""
        # TODO: Implement cleanup of temporary files
        pass

# Future implementation
# class PersistentVectorStore(VectorStore[E, R]):
#     """Persistent vector store implementation."""
#     pass
