"""Integration tests for the code chat functionality."""
from pathlib import Path
import pytest
from code_chat_tool.vector_store import PersistentVectorStore
from code_chat_tool.embedding import SentenceTransformerEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool

# Path to test repository
COMMONS_LANG_REPO = Path(__file__).parent.parent / "test-data" / "test-repos" / "commons-lang"

def get_storage_dir(repo_path: Path) -> Path:
    """Get the storage directory for a repository's embeddings."""
    # Use just the repository name, not the full path
    return Path.home() / ".code_chat_tool" / "indices" / "commons-lang"

def check_index_exists(repo_path: Path) -> bool:
    """Check if a repository has been indexed."""
    storage_dir = get_storage_dir(repo_path)
    print(f"Checking for index at: {storage_dir}")
    exists = (storage_dir / "embeddings.npy").exists()
    print(f"Index exists: {exists}")
    return exists

def test_java_code_chat():
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
    
    # Test Java-specific queries
    queries = [
        "How does StringUtils handle null values?",
        "Show me examples of array manipulation utilities",
        "Explain the math utilities available",
        "How are random numbers generated?",
        "What date/time utilities are available?"
    ]
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"{'='*80}")
        response = chat_tool.query(query)
        print("Response:")
        print(response)
        print(f"{'='*80}")
        
        # Basic response validation
        assert response, f"No response received for query: {query}"
        assert isinstance(response, str)
        assert len(response) > 0

def test_error_handling():
    """Test error handling in the workflow."""
    embedder = SentenceTransformerEmbedder()
    # Create a vector store with an empty directory
    test_path = Path.home() / ".code_chat_tool" / "test_empty_index"
    test_path.mkdir(parents=True, exist_ok=True)
    vector_store = PersistentVectorStore(test_path)
    chat_tool = ChatWithCodeTool(embedder, vector_store)
    
    try:
        # Should return None for empty index
        response = chat_tool.query("What does this code do?")
        assert response is None or response == "I couldn't find any relevant code that answers your question."
    finally:
        # Clean up test directory
        import shutil
        if test_path.exists():
            shutil.rmtree(test_path)
