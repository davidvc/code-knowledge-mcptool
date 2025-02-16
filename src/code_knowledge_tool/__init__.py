"""Code Knowledge Tool package."""

from .code_parser import (
    CodeParser,
    CodeSegment as ParserCodeSegment
)

from .vector_store import (
    VectorStore,
    InMemoryVectorStore,
    PersistentVectorStore,
    SearchResult,
    CodeSegment as StoreCodeSegment
)

from .embedding import (
    SentenceTransformerEmbedder,
    OllamaEmbedder
)

from .mcp_tool import (
    CodeKnowledgeTool,
    KnowledgeEntry,
    ContextEntry
)

__all__ = [
    'CodeParser',
    'ParserCodeSegment',
    'VectorStore',
    'InMemoryVectorStore',
    'PersistentVectorStore',
    'SearchResult',
    'StoreCodeSegment',
    'SentenceTransformerEmbedder',
    'OllamaEmbedder',
    'CodeKnowledgeTool',
    'KnowledgeEntry',
    'ContextEntry'
]
