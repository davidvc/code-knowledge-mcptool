"""
Embedding Module for Chat with Code Repository Tool

This module provides functionality to generate embeddings for code segments using
the local Ollama service.
"""

from typing import List, Tuple, Union
import sys
import os
import httpx
import numpy as np
from code_knowledge_tool.code_parser import CodeSegment

class OllamaEmbedder:
    def __init__(self, base_url: str):
        """
        Initialize the OllamaEmbedder with a base URL.
        
        Args:
            base_url: The base URL of the local Ollama service
        """
        self.base_url = base_url.rstrip('/')
        
    def _get_embedding(self, text: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Get embeddings using Ollama API.
        
        Args:
            text: Single text string or list of text strings to embed
            
        Returns:
            Single numpy array or list of numpy arrays containing embedding vectors
            
        Raises:
            ConnectionError: If Ollama service is unavailable
            Exception: For other API errors
        """
        url = f"{self.base_url}/api/embeddings"
        is_batch = isinstance(text, list)
        
        try:
            # Get embedding with longer timeout since text can be large
            response = httpx.post(
                url,
                json={
                    "model": "llama2",  # Use llama2 directly since it's our base requirement
                    "prompt": text,
                    "options": {
                        "temperature": 0.0  # Deterministic output
                    }
                },
                timeout=60.0  # Increase timeout further for large files
            )
            response.raise_for_status()
            
            data = response.json()
            if is_batch:
                if "embeddings" not in data:
                    raise Exception("No embeddings in batch response")
                return [np.array(emb, dtype=np.float32) for emb in data["embeddings"]]
            else:
                if "embedding" not in data:
                    raise Exception("No embedding in response")
                return np.array(data["embedding"], dtype=np.float32)
            
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to Ollama service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error getting embedding: {str(e)}")

    def embed_segments(self, code_segments: List[CodeSegment], batch_size: int = 10) -> List[Tuple[np.ndarray, CodeSegment]]:
        """
        Generate embeddings for a list of CodeSegment objects.
        
        Args:
            code_segments: List of code segments to embed
            batch_size: Number of segments to process in each batch
        
        Returns:
            List of tuples containing (embedding vector, code segment)
            
        Raises:
            ConnectionError: If Ollama service is unavailable
            Exception: For other errors
        """
        results = []
        total_segments = len(code_segments)
        
        # Process segments in batches
        for i in range(0, total_segments, batch_size):
            batch = code_segments[i:i + batch_size]
            batch_texts = []
            
            # Prepare batch texts
            for segment in batch:
                file_name = os.path.basename(segment.path)
                file_type = os.path.splitext(file_name)[1].lower()
                
                # Build enhanced context with metadata
                context_parts = [
                    f"File: {file_name}",
                    f"Type: {file_type}",
                ]
                
                # Add Java-specific information if available
                if segment.name:
                    context_parts.append(f"Name: {segment.name}")
                if segment.doc_text:
                    context_parts.append(f"Documentation:\n{segment.doc_text}")
                
                # Add the full content
                context_parts.append(f"Content:\n{segment.content}")
                
                # Join all parts with double newlines for clear separation
                context = "\n\n".join(context_parts)
                batch_texts.append(context)
            
            # Get embeddings for batch
            try:
                batch_embeddings = self._get_embedding(batch_texts)
                
                # Pair embeddings with segments
                for segment, embedding in zip(batch, batch_embeddings):
                    results.append((embedding, segment))
                
                # Update progress
                processed = min(i + batch_size, total_segments)
                sys.stdout.write(f"\rProcessed {processed}/{total_segments} segments")
                sys.stdout.flush()
                
            except Exception as e:
                sys.stdout.write("\n")  # New line before error
                raise Exception(f"Error processing batch: {str(e)}")
        
        sys.stdout.write("\n")
        return results

    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate an embedding for a text query.
        
        Args:
            text: The text to embed
        
        Returns:
            Numpy array containing the embedding vector
            
        Raises:
            ConnectionError: If Ollama service is unavailable
            Exception: For other errors
        """
        return self._get_embedding(text)
