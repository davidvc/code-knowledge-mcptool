"""Vector storage abstraction and implementations."""
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from .embedding import Embedding  # Add import for Embedding type

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

class TransientVectorStore(VectorStore[Embedding, Embedding]):
    """Temporary in-memory vector store implementation using Chroma."""
    
    def __init__(self):
        """Initialize temporary vector store."""
        import chromadb
        import tempfile
        import atexit
        
        # Create temporary directory for Chroma
        self._temp_dir = tempfile.mkdtemp(prefix="code_chat_")
        
        # Initialize Chroma client with temporary persistence and reset enabled
        self._client = chromadb.PersistentClient(
            path=self._temp_dir,
            settings=chromadb.Settings(allow_reset=True)
        )
        self._collection = self._client.create_collection(name="code_segments")
        
        # Register cleanup on exit
        atexit.register(self.cleanup)
        
        # Cache embeddings for retrieval
        self._embeddings_cache = {}
    
    def store(self, embeddings: List[Embedding]) -> None:
        """Store embeddings in temporary Chroma instance.
        
        Args:
            embeddings: List of embeddings to store
        """
        if not embeddings:
            return
            
        # Prepare data for Chroma
        ids = [str(i) for i in range(len(embeddings))]
        vectors = [e.vector for e in embeddings]
        
        # Cache embeddings for retrieval
        for id_, emb in zip(ids, embeddings):
            self._embeddings_cache[id_] = emb
        
        # Add to collection
        self._collection.add(
            embeddings=vectors,
            ids=ids
        )
    
    def search(self, query: Embedding) -> List[Embedding]:
        """Search temporary Chroma instance.
        
        Args:
            query: Query embedding
            
        Returns:
            List of results ordered by similarity
        """
        # Search collection
        results = self._collection.query(
            query_embeddings=[query.vector],
            n_results=5  # Return top 5 matches
        )
        
        # Get matching embeddings from cache
        matches = []
        if results and 'ids' in results:
            for id_ in results['ids'][0]:  # First query's results
                if id_ in self._embeddings_cache:
                    matches.append(self._embeddings_cache[id_])
                    
        return matches
    
    def cleanup(self) -> None:
        """Clean up temporary storage."""
        import shutil
        
        try:
            # Close Chroma client
            if hasattr(self, '_client'):
                self._client.reset()
                
            # Remove temporary directory
            if hasattr(self, '_temp_dir'):
                shutil.rmtree(self._temp_dir, ignore_errors=True)
                
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

# Future implementation
# class PersistentVectorStore(VectorStore[E, R]):
#     """Persistent vector store implementation."""
#     pass
