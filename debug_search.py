#!/usr/bin/env python3
"""
Debug script to test database content and search functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

def debug_database():
    """Debug the database content and search functionality"""
    print("🔍 Debugging Database Content...")
    
    # Initialize components
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Check database content
    print(f"\n📊 Database Statistics:")
    count = datastore.table.count_rows()
    print(f"Total rows: {count}")
    
    if count == 0:
        print("❌ Database is empty! No documents have been processed.")
        return
    
    # Test various search terms
    search_terms = [
        "Trinkgeld",
        "tipping", 
        "tip",
        "0,22",
        "0.22",
        "EUR",
        "Euro",
        "restaurant",
        "receipt",
        "bill"
    ]
    
    print(f"\n🔍 Testing Search Terms:")
    for term in search_terms:
        print(f"\n--- Searching for: '{term}' ---")
        try:
            results = datastore.search(term, top_k=3)
            if results:
                print(f"✅ Found {len(results)} results:")
                for i, result in enumerate(results[:2]):  # Show first 2 results
                    print(f"  {i+1}: {result[:200]}...")
            else:
                print(f"❌ No results found for '{term}'")
        except Exception as e:
            print(f"❌ Error searching for '{term}': {e}")
    
    # Test hybrid search
    print(f"\n🔍 Testing Hybrid Search for 'Trinkgeld':")
    try:
        hybrid_results = retriever.retrieve("Trinkgeld", top_k=5, use_hybrid_search=True)
        if hybrid_results:
            print(f"✅ Hybrid search found {len(hybrid_results)} results:")
            for i, result in enumerate(hybrid_results[:2]):
                print(f"  {i+1}: {result[:200]}...")
        else:
            print("❌ No results found with hybrid search")
    except Exception as e:
        print(f"❌ Error in hybrid search: {e}")
    
    # Show sample content from database
    print(f"\n📄 Sample Database Content:")
    try:
        # Get first few rows
        sample_data = datastore.table.to_pandas().head(3)
        for i, row in sample_data.iterrows():
            print(f"\n--- Row {i+1} ---")
            print(f"Source: {row.get('source', 'N/A')}")
            content = row.get('content', 'N/A')
            print(f"Content: {content[:300]}...")
    except Exception as e:
        print(f"❌ Error reading database content: {e}")

if __name__ == "__main__":
    debug_database() 