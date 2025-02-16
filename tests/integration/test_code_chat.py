"""Integration tests for the code chat functionality."""
from pathlib import Path
import pytest
from code_chat_tool.vector_store import PersistentVectorStore
from code_chat_tool.embedding import SentenceTransformerEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool
from .response_evaluator import OpenRouterEvaluator, ResponseEvaluator

# Test configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "google/palm-2-chat-bison"

# Path to test repository
COMMONS_LANG_REPO = Path(__file__).parent / "test-repos" / "commons-lang"

@pytest.fixture
def evaluator() -> ResponseEvaluator:
    """Create response evaluator."""
    return OpenRouterEvaluator(OPENROUTER_API_KEY, OPENROUTER_MODEL)

def get_storage_dir(repo_path: Path) -> Path:
    """Get the storage directory for a repository's embeddings."""
    return Path.home() / ".code_chat_tool" / "indices" / repo_path.name

def check_index_exists(repo_path: Path) -> bool:
    """Check if a repository has been indexed."""
    storage_dir = get_storage_dir(repo_path)
    return (storage_dir / "embeddings.npy").exists()

def test_java_code_chat(evaluator):
    """Test the code chat tool with the Commons Lang repository."""
    # Check if repository is indexed
    if not check_index_exists(COMMONS_LANG_REPO):
        cli_path = Path(__file__).parent.parent.parent / "src" / "index_repository.py"
        message = (
            f"\n{'='*80}\n"
            f"Repository {COMMONS_LANG_REPO.name} needs to be indexed first.\n"
            f"Please run:\n\n"
            f"    python {cli_path} {COMMONS_LANG_REPO}\n\n"
            f"Then run this test again.\n"
            f"{'='*80}\n"
        )
        print(message)
        pytest.skip("Repository not indexed")
    
    # Use the same embedder type as the CLI for query embedding
    embedder = SentenceTransformerEmbedder()
    vector_store = PersistentVectorStore(get_storage_dir(COMMONS_LANG_REPO))
    chat_tool = ChatWithCodeTool(embedder, vector_store)
    
    try:
        # Test Java-specific queries
        queries = [
            "How does StringUtils handle null values?",
            "Show me examples of array manipulation utilities",
            "Explain the math utilities available",
            "How are random numbers generated?",
            "What date/time utilities are available?"
        ]
        
        for query in queries:
            response = chat_tool.query(query)
            assert response, f"No response received for query: {query}"
            
            # Basic response validation
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Evaluate response quality using LLM
            result = evaluator.evaluate_response(
                query=query,
                response=response,
                context=f"This is a query about Apache Commons Lang, a Java utility library. The response should reference the Commons Lang codebase."
            )
            
            # Assert response quality
            assert result.is_acceptable, f"Response quality check failed: {result.reasoning}"
            assert result.score >= 0.7, f"Response score too low: {result.score}"
                
    finally:
        vector_store.cleanup()

def test_error_handling():
    """Test error handling in the workflow."""
    embedder = SentenceTransformerEmbedder()
    vector_store = PersistentVectorStore(Path("/nonexistent/path"))
    chat_tool = ChatWithCodeTool(embedder, vector_store)
    
    # Should handle missing index gracefully
    with pytest.raises(Exception) as exc_info:
        chat_tool.query("What does this code do?")
    assert "index" in str(exc_info.value).lower()
