"""MCP tool implementation for code chat functionality."""
from pathlib import Path
from typing import Optional

from .code_parser import CodeParser
from .embedding import OllamaEmbedder
from .vector_store import VectorStore

class ChatWithCodeTool:
    """MCP tool for chatting with code repositories."""
    
    def __init__(
        self,
        parser: CodeParser,
        embedder: OllamaEmbedder,
        vector_store: VectorStore
    ):
        """Initialize the chat tool.
        
        Args:
            parser: Component for parsing code repositories
            embedder: Component for generating embeddings
            vector_store: Component for storing and searching vectors
        """
        self.parser = parser
        self.embedder = embedder
        self.vector_store = vector_store
        
    def process_repository(self, repo_path: Path) -> None:
        """Process a code repository for querying.
        
        Args:
            repo_path: Path to the repository
            
        Raises:
            FileNotFoundError: If repository path doesn't exist
            ConnectionError: If embedding service is unavailable
            Exception: For other processing errors
        """
        if not repo_path.exists():
            raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
            
        # Parse repository into code segments
        segments = list(self.parser.parse_repository(repo_path))
        
        if not segments:
            raise Exception(f"No code segments found in repository: {repo_path}")
            
        try:
            # Generate embeddings for segments
            embeddings = self.embedder.embed_segments(segments)
            
            # Store embeddings
            self.vector_store.store(embeddings)
            
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to embedding service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing repository: {str(e)}")
    
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
                
            # TODO: Format response based on results
            # For now, return the first result
            return str(results[0])
            
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to embedding service: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")
