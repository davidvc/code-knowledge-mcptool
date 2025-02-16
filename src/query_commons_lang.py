#!/usr/bin/env python3
"""Interactive tool for querying the commons-lang code embeddings."""
from pathlib import Path
from code_chat_tool.vector_store import PersistentVectorStore
from code_chat_tool.embedding import SentenceTransformerEmbedder
from code_chat_tool.mcp_tool import ChatWithCodeTool

def get_storage_dir() -> Path:
    """Get the storage directory for commons-lang embeddings."""
    return Path.home() / ".code_chat_tool" / "indices" / "commons-lang"

def main():
    """Run the interactive query tool."""
    storage_dir = get_storage_dir()
    if not (storage_dir / "embeddings.npy").exists():
        print(f"Error: No index found at {storage_dir}")
        print("Please run index_repository.py on the commons-lang repository first.")
        return

    # Initialize the chat tool
    embedder = SentenceTransformerEmbedder()
    vector_store = PersistentVectorStore(storage_dir)
    chat_tool = ChatWithCodeTool(embedder, vector_store)

    print("\nWelcome to the Commons Lang Code Query Tool!")
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