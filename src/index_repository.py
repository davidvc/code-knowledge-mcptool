#!/usr/bin/env python3
"""
CLI tool for indexing a local code repository for the Chat with Code Repository Tool.
This tool leverages the code parser, embedding engine, and vector storage components.
"""

import argparse
import os
import sys
from collections import Counter
from pathlib import Path
from code_chat_tool import CodeParser, SentenceTransformerEmbedder, PersistentVectorStore

def format_file_stats(segments):
    """Format file statistics for display."""
    extensions = Counter(Path(s.path).suffix for s in segments)
    stats = ["File types found:"]
    for ext, count in sorted(extensions.items()):
        if ext:  # Skip empty extensions
            stats.append(f"  {ext}: {count} files")
    return "\n".join(stats)

def main():
    parser = argparse.ArgumentParser(
        description="Index a local code repository for the Chat with Code Repository Tool."
    )
    parser.add_argument(
        "repository_path", type=str,
        help="Path to the local repository to index."
    )
    parser.add_argument(
        "--batch-size", type=int, default=32,
        help="Batch size for embedding generation (default: 32)"
    )
    args = parser.parse_args()

    repo_path = Path(args.repository_path)
    if not repo_path.is_dir():
        sys.stderr.write(f"Error: Directory '{repo_path}' does not exist or is not accessible.\n")
        sys.exit(1)

    # Create storage directory based on repository name
    storage_dir = Path.home() / ".code_chat_tool" / "indices" / repo_path.name
    
    sys.stdout.write(f"Indexing repository: {repo_path}\n")
    sys.stdout.write(f"Output directory: {storage_dir}\n\n")
    
    # Initialize components
    code_parser = CodeParser()
    embedder = SentenceTransformerEmbedder()  # Uses default all-MiniLM-L6-v2 model
    store = PersistentVectorStore(storage_dir)

    # Parse the repository to extract code files and relevant data.
    sys.stdout.write("Step 1/3: Parsing repository for code files...\n")
    try:
        segments = list(code_parser.parse_repository(repo_path))
        sys.stdout.write(f"Found {len(segments)} code segments.\n")
        sys.stdout.write(f"{format_file_stats(segments)}\n\n")
    except Exception as e:
        sys.stderr.write(f"Error during parsing: {e}\n")
        sys.exit(1)

    # Generate embeddings using sentence-transformers
    sys.stdout.write("Step 2/3: Generating embeddings...\n")
    try:
        # Process segments in batches
        total_segments = len(segments)
        for i in range(0, total_segments, args.batch_size):
            batch = segments[i:i + args.batch_size]
            batch_texts = []
            
            # Prepare batch texts
            for segment in batch:
                context = f"File: {segment.path}\n\nContent:\n{segment.content}"
                batch_texts.append(context)
            
            # Get embeddings for batch
            batch_embeddings = embedder._get_embedding(batch_texts)
            
            # Store embeddings with segments
            embeddings_with_segments = list(zip(batch_embeddings, batch))
            store.store(embeddings_with_segments)
            
            # Update progress
            processed = min(i + args.batch_size, total_segments)
            progress = (processed / total_segments) * 100
            sys.stdout.write(f"\rProgress: {processed}/{total_segments} segments ({progress:.1f}%)")
            sys.stdout.flush()
            
        sys.stdout.write("\n\n")
    except Exception as e:
        sys.stderr.write(f"\nError during embedding generation: {e}\n")
        sys.exit(1)

    # Final status
    sys.stdout.write("Step 3/3: Finalizing index...\n")
    sys.stdout.write(f"Successfully indexed {len(store.embeddings)} embeddings.\n")
    sys.stdout.write(f"Index stored in: {storage_dir}\n")

if __name__ == "__main__":
    main()
