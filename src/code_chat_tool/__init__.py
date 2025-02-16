"""
Initialization module for code_chat_tool package.

Exports core functionality from submodules.
"""

from .code_parser import CodeParser, CodeSegment
from .embedding import OllamaEmbedder, SentenceTransformerEmbedder
from .vector_store import VectorStore, TransientVectorStore, PersistentVectorStore, SearchResult
from .mcp_tool import ChatWithCodeTool

__all__ = [
    'CodeParser',
    'CodeSegment',
    'OllamaEmbedder',
    'SentenceTransformerEmbedder',
    'VectorStore',
    'TransientVectorStore',
    'PersistentVectorStore',
    'SearchResult',
    'ChatWithCodeTool'
]
