"""Integration tests for the code chat functionality."""
from pathlib import Path
import pytest
from code_chat_tool.code_parser import CodeParser
from code_chat_tool.vector_store import TransientVectorStore
from code_chat_tool.embedding import OllamaEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool
from .response_evaluator import OpenRouterEvaluator, ResponseEvaluator

# Test configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "google/palm-2-chat-bison"

# Paths to test repositories
FLASK_REPO = Path(__file__).parent / "test-repos" / "flask"
COMMONS_LANG_REPO = Path(__file__).parent / "test-repos" / "commons-lang"

@pytest.fixture
def evaluator() -> ResponseEvaluator:
    """Create response evaluator."""
    return OpenRouterEvaluator(OPENROUTER_API_KEY, OPENROUTER_MODEL)

def test_python_code_chat(evaluator):
    """Test the code chat tool with the Flask repository."""
    parser = CodeParser()
    embedder = OllamaEmbedder(base_url="http://localhost:11434")
    vector_store = TransientVectorStore()
    chat_tool = ChatWithCodeTool(parser, embedder, vector_store)
    
    try:
        # Process Flask repository
        chat_tool.process_repository(FLASK_REPO)
        
        # Test Python-specific queries
        queries = [
            "How does Flask handle request context?",
            "Explain Flask's blueprint feature",
            "Show me the main application class",
            "How does Flask handle static files?",
            "What is Flask's configuration system?"
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
                context=f"This is a query about Flask, a Python web framework. The response should reference the Flask codebase."
            )
            
            # Assert response quality
            assert result.is_acceptable, f"Response quality check failed: {result.reasoning}"
            assert result.score >= 0.7, f"Response score too low: {result.score}"
                
    finally:
        vector_store.cleanup()

def test_java_code_chat(evaluator):
    """Test the code chat tool with the Commons Lang repository."""
    parser = CodeParser()
    embedder = OllamaEmbedder(base_url="http://localhost:11434")
    vector_store = TransientVectorStore()
    chat_tool = ChatWithCodeTool(parser, embedder, vector_store)
    
    try:
        # Process Commons Lang repository
        chat_tool.process_repository(COMMONS_LANG_REPO)
        
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
    parser = CodeParser()
    embedder = OllamaEmbedder(base_url="http://invalid-url")
    vector_store = TransientVectorStore()
    chat_tool = ChatWithCodeTool(parser, embedder, vector_store)
    
    try:
        # Should handle Ollama connection error gracefully
        with pytest.raises(Exception) as exc_info:
            chat_tool.process_repository(FLASK_REPO)
            error_msg = str(exc_info.value).lower()
            assert any(term in error_msg for term in ["connection", "failed to connect", "nodename nor servname"])
        
        # Should handle invalid repository path
        with pytest.raises(Exception) as exc_info:
            chat_tool.process_repository(Path("/nonexistent/path"))
        assert "path" in str(exc_info.value).lower()
        
    finally:
        vector_store.cleanup()
