#!/usr/bin/env python3
"""Interactive tool for querying code embeddings."""
import argparse
from pathlib import Path
from code_chat_tool.vector_store import PersistentVectorStore
from code_chat_tool.embedding import SentenceTransformerEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool

def get_storage_dir(index_path: str) -> Path:
    """Get the storage directory for embeddings."""
    return Path(index_path)

def main():
    """Run the interactive query tool."""
    parser = argparse.ArgumentParser(description='Query a code embedding index')
    parser.add_argument('index_path', 
                       help='Path to the index directory (e.g., ~/.code_chat_tool/indices/commons-lang)')
    args = parser.parse_args()

    storage_dir = get_storage_dir(args.index_path)
    if not (storage_dir / "embeddings.npy").exists():
        print(f"Error: No index found at {storage_dir}")
        print("Please run index_repository.py on your repository first.")
        return

    # Initialize the chat tool
    embedder = SentenceTransformerEmbedder()
    vector_store = PersistentVectorStore(storage_dir)
    chat_tool = ChatWithCodeTool(embedder, vector_store)

    print("\nWelcome to the Code Query Tool!")
    print("Enter your questions about the codebase (or 'quit' to exit)")
    print("Example questions:")
    print("- Show me examples of array manipulation utilities")
    print("- How are random numbers generated?")
    print("- What date/time utilities are available?")
    
    while True:
        print("\nEnter your question (or 'quit' to exit):")
        query = input("> ").strip()
        
        if query.lower() in ('quit', 'exit', 'q'):
            break
            
        if not query:
            continue
            
        try:
            response = chat_tool.query(query)
            if response:
                print("\nResponse:")
                print(response)
            else:
                print("\nNo relevant code found for your query.")
        except Exception as e:
            print(f"\nError processing query: {str(e)}")

if __name__ == '__main__':
    main()