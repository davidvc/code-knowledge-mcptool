#!/usr/bin/env python3
"""
CLI tool for indexing a local code repository for the Chat with Code Repository Tool.
This tool leverages the code parser, embedding engine, and vector storage components.
"""

import argparse
import os
import sys

from pathlib import Path
from code_chat_tool import CodeParser, SentenceTransformerEmbedder, PersistentVectorStore

def main():
    parser = argparse.ArgumentParser(
        description="Index a local code repository for the Chat with Code Repository Tool."
    )
    parser.add_argument(
        "repository_path", type=str,
        help="Path to the local repository to index."
    )
    args = parser.parse_args()

    repo_path = Path(args.repository_path)
    if not repo_path.is_dir():
        sys.stderr.write(f"Error: Directory '{repo_path}' does not exist or is not accessible.\n")
        sys.exit(1)

    # Create storage directory based on repository name
    storage_dir = Path.home() / ".code_chat_tool" / "indices" / repo_path.name
    
    # Initialize components
    code_parser = CodeParser()
    embedder = SentenceTransformerEmbedder()  # Uses default all-MiniLM-L6-v2 model
    store = PersistentVectorStore(storage_dir)

    # Parse the repository to extract code files and relevant data.
    sys.stdout.write("Parsing repository for code files...\n")
    try:
        segments = list(code_parser.parse_repository(repo_path))
        sys.stdout.write(f"Found {len(segments)} code segments.\n")
    except Exception as e:
        sys.stderr.write(f"Error during parsing: {e}\n")
        sys.exit(1)

    # Generate embeddings using the local Ollama service.
    sys.stdout.write("Generating embeddings...\n")
    try:
        # Create context strings for each segment
        for i, segment in enumerate(segments, 1):
            sys.stdout.write(f"\rProcessing segment {i}/{len(segments)}")
            sys.stdout.flush()
            
            context = f"File: {segment.path}\n\nContent:\n{segment.content}"
            embedding = embedder._get_embedding(context)
            store.store([(embedding, segment)])
            
        sys.stdout.write("\n")
    except Exception as e:
        sys.stderr.write(f"\nError during embedding generation: {e}\n")
        sys.exit(1)

    sys.stdout.write("Repository indexing complete.\n")
    sys.stdout.write(f"Indexed {len(store.embeddings)} embeddings.\n")

if __name__ == "__main__":
    main()
