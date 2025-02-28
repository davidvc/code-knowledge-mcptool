"""
Embedding Module for Chat with Code Repository Tool

This module provides functionality to generate embeddings for text using
the local Ollama service.
"""

import sys
import httpx
import numpy as np

class OllamaEmbedder:
    def __init__(self, base_url: str):
        """Initialize the OllamaEmbedder with a base URL."""
        self.base_url = base_url.rstrip('/')
        
    def _get_embedding(self, text):
        """Get embeddings using Ollama API."""
        url = f"{self.base_url}/api/embeddings"
        is_batch = isinstance(text, list)
        
        try:
            response = httpx.post(
                url,
                json={
                    "model": "llama2",
                    "prompt": text,
                    "options": {
                        "temperature": 0.0
                    }
                },
                timeout=60.0
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

    def embed_segments(self, segments, batch_size=10):
        """Generate embeddings for a list of text segments."""
        results = []
        total_segments = len(segments)
        
        for i in range(0, total_segments, batch_size):
            batch = segments[i:i + batch_size]
            
            try:
                batch_embeddings = self._get_embedding(batch)
                
                for segment, embedding in zip(batch, batch_embeddings):
                    results.append((embedding, segment))
                
                processed = min(i + batch_size, total_segments)
                sys.stdout.write(f"\rProcessed {processed}/{total_segments} segments")
                sys.stdout.flush()
                
            except Exception as e:
                sys.stdout.write("\n")
                raise Exception(f"Error processing batch: {str(e)}")
        
        sys.stdout.write("\n")
        return results

    def embed_text(self, text):
        """Generate an embedding for a text query."""
        return self._get_embedding(text)
