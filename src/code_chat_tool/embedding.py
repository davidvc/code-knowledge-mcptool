"""Code embedding functionality using Ollama service."""
from dataclasses import dataclass
from typing import List, Optional
import httpx
from .code_parser import CodeSegment

@dataclass
class Embedding:
    """Represents a vector embedding with its source code context."""
    
    vector: List[float]
    segment: CodeSegment
    
    def __str__(self) -> str:
        """Return the source code content for this embedding."""
        return self.segment.content

class OllamaEmbedder:
    """Handles code embedding using Ollama service."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama embedder.
        
        Args:
            base_url: Base URL for Ollama service
        """
        self.base_url = base_url.rstrip('/')
        
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for text from Ollama.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            ConnectionError: If Ollama service is unavailable
            Exception: For other embedding errors
        """
        url = f"{self.base_url}/api/embeddings"
        
        try:
            response = httpx.post(
                url,
                json={
                    "model": "llama2",  # TODO: Make configurable
                    "prompt": text,  # Ollama API uses "prompt" for embeddings
                },
                timeout=30.0  # Add timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("embedding", data.get("embeddings", []))  # Ollama might put it under either key
            
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Ollama service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error getting embedding: {str(e)}")
    
    def embed_text(self, text: str) -> Embedding:
        """Generate embedding for arbitrary text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding instance
        """
        vector = self._get_embedding(text)
        
        # Create a CodeSegment for the query text
        segment = CodeSegment(
            content=text,
            file_path=None,  # type: ignore
            start_line=1,
            end_line=1
        )
        
        return Embedding(vector=vector, segment=segment)
    
    def embed_segments(self, segments: List[CodeSegment]) -> List[Embedding]:
        """Generate embeddings for code segments.
        
        Args:
            segments: List of code segments to embed
            
        Returns:
            List of Embedding instances
            
        Raises:
            ConnectionError: If Ollama service is unavailable
            Exception: For other embedding errors
        """
        embeddings = []
        
        for segment in segments:
            vector = self._get_embedding(segment.content)
            embeddings.append(Embedding(vector=vector, segment=segment))
            
        return embeddings
