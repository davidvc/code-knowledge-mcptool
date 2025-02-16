"""MCP tool implementation for memory bank functionality."""
from pathlib import Path
from typing import List, Optional, Dict, Any
import numpy as np
from dataclasses import dataclass

from .embedding import SentenceTransformerEmbedder
from .vector_store import VectorStore, SearchResult

@dataclass
class KnowledgeEntry:
    """Represents a piece of knowledge about code."""
    path: str
    summary: str
    metadata: Dict[str, Any]

@dataclass
class ContextEntry:
    """Represents a relevant context entry."""
    path: str
    content: str
    relevance: float

class ChatWithCodeTool:
    """MCP tool for managing code knowledge."""
    
    def __init__(
        self,
        embedder: SentenceTransformerEmbedder,
        vector_store: VectorStore
    ):
        """Initialize the chat tool.
        
        Args:
            embedder: Component for generating embeddings
            vector_store: Component for storing and searching knowledge
        """
        self.embedder = embedder
        self.vector_store = vector_store
        self._path_to_metadata = {}  # Cache for path -> metadata mapping

    def add_knowledge(self, path: str, summary: str, metadata: Dict[str, Any]) -> None:
        """Add new knowledge about code.
        
        Args:
            path: Path to the code component
            summary: Semantic summary of the code
            metadata: Additional information about the code
            
        Raises:
            ValueError: If path is empty or knowledge already exists
        """
        if not path:
            raise ValueError("Path cannot be empty")
            
        if path in self._path_to_metadata:
            raise ValueError(f"Knowledge already exists for {path}")
            
        # Create embedding for the summary
        embedding = self.embedder.embed_text(summary)
        
        # Store the knowledge
        self.vector_store.add(embedding, path, summary)
        self._path_to_metadata[path] = metadata

    def update_knowledge(self, path: str, new_summary: str, metadata: Dict[str, Any]) -> None:
        """Update existing knowledge about code.
        
        Args:
            path: Path to the code component
            new_summary: Updated semantic summary
            metadata: Updated metadata
            
        Raises:
            ValueError: If path doesn't exist
        """
        if path not in self._path_to_metadata:
            raise ValueError(f"No knowledge exists for {path}")
            
        # Create embedding for the new summary
        embedding = self.embedder.embed_text(new_summary)
        
        # Update the knowledge
        self.vector_store.update(embedding, path, new_summary)
        self._path_to_metadata[path] = metadata

    def search_knowledge(self, query: str) -> List[SearchResult]:
        """Search for relevant code knowledge.
        
        Args:
            query: Natural language query
            
        Returns:
            List of search results with similarity scores
        """
        # Generate embedding for query
        query_embedding = self.embedder.embed_text(query)
        
        # Search for similar knowledge
        results = self.vector_store.search(query_embedding)
        
        # Filter results with low similarity
        return [r for r in results if r.score > 0.3]

    def get_relevant_context(self, task: str) -> List[ContextEntry]:
        """Get relevant context for a task.
        
        Args:
            task: Description of the task
            
        Returns:
            List of relevant context entries
        """
        # Get all results without filtering
        query_embedding = self.embedder.embed_text(task)
        results = self.vector_store.search(query_embedding, top_k=10)
        
        # Convert to context entries
        context = []
        for result in results:
            # Include even lower similarity results for context
            context.append(ContextEntry(
                path=result.segment.path,
                content=result.segment.content,
                relevance=result.score
            ))
            
        return context

    def get_metadata(self, path: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a path.
        
        Args:
            path: Path to get metadata for
            
        Returns:
            Metadata dictionary or None if not found
        """
        return self._path_to_metadata.get(path)
