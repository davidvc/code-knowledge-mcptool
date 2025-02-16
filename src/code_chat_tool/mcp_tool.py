"""MCP tool implementation for code chat functionality."""
from pathlib import Path
from typing import List, Optional, Tuple
import numpy as np

from .code_parser import CodeParser, CodeSegment
from .embedding import OllamaEmbedder
from .vector_store import VectorStore, SearchResult

class ChatWithCodeTool:
    """MCP tool for chatting with code repositories."""
    
    def __init__(
        self,
        embedder: OllamaEmbedder,
        vector_store: VectorStore
    ):
        """Initialize the chat tool.
        
        Args:
            embedder: Component for generating query embeddings
            vector_store: Component for searching pre-built vector store
        """
        self.embedder = embedder
        self.vector_store = vector_store
    
    def query(self, question: str) -> Optional[str]:
        """Query the processed repository.
        
        Args:
            question: Natural language query about the code
            
        Returns:
            Response string, or None if no relevant code found
            
        Raises:
            ConnectionError: If embedding service is unavailable
            Exception: For other query errors
        """
        try:
            # Generate embedding for query
            query_embedding = self.embedder.embed_text(question)
            
            # Search for similar code segments
            results = self.vector_store.search(query_embedding)
            
            if not results:
                return None
                
            # Format response using the most relevant code segments
            return self._format_response(question, results)
            
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to embedding service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")
            
    def _format_response(self, question: str, results: List[SearchResult]) -> str:
        """Format a response using the search results.
        
        Args:
            question: The original query
            results: List of search results with code segments and similarity scores
            
        Returns:
            Formatted response string
        """
        # Filter results with low similarity scores
        relevant_results = [r for r in results if r.score > 0.5]
        
        if not relevant_results:
            return "I couldn't find any relevant code that answers your question."
            
        # Build response using the most relevant code segments
        response_parts = []
        
        # Add introduction
        response_parts.append(f"Based on the code, here's what I found about '{question}':\n")
        
        # Add relevant code segments
        for i, result in enumerate(relevant_results, 1):
            # Get relative path for cleaner display
            rel_path = Path(result.segment.path).name
            
            response_parts.append(f"\n{i}. From {rel_path}:\n")
            response_parts.append(f"```\n{result.segment.content}\n```\n")
            
        # Add summary if multiple segments found
        if len(relevant_results) > 1:
            response_parts.append("\nThese code segments show different aspects of your query.")
            
        return "".join(response_parts)
