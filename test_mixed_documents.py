#!/usr/bin/env python3
"""
Test script to demonstrate enhanced indexing with different document types
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore

def test_different_document_types():
    """Test enhanced indexing with different document types"""
    print("🧪 Testing Enhanced Indexing with Different Document Types...")
    
    # Initialize pipeline with enhanced indexer
    datastore = Datastore()
    pipeline = RAGPipeline(datastore)
    
    # Reset database
    print("🗑️  Resetting database...")
    pipeline.reset()
    
    # Test documents
    test_docs = [
        ("test_receipt.pdf", "Receipt with product names"),
        ("test_different_docs.md", "Technical documentation"),
        ("test_receipt.md", "Receipt in markdown format")
    ]
    
    for doc_path, description in test_docs:
        print(f"\n📄 Adding {description}: {doc_path}")
        
        try:
            items = pipeline.add_documents([doc_path])
            print(f"✅ Added {len(items)} items to database")
            
            # Show database content for this document
            count = datastore.table.count_rows()
            print(f"📊 Database now contains {count} total items")
            
            # Show sample items for this document
            try:
                sample_data = datastore.table.to_pandas()
                doc_items = sample_data[sample_data['source'].str.contains(os.path.basename(doc_path), na=False)]
                print(f"📋 Items for {os.path.basename(doc_path)}:")
                for i, row in doc_items.head(3).iterrows():
                    source = row.get('source', 'Unknown')
                    content = row.get('content', 'N/A')[:100]
                    print(f"  - {source}: {content}...")
            except Exception as e:
                print(f"Error reading database: {e}")
                
        except Exception as e:
            print(f"❌ Error processing {doc_path}: {e}")
    
    # Test queries for different document types
    print("\n🔍 Testing Queries Across Different Document Types:")
    
    test_queries = [
        # Receipt-specific queries
        ("What drink was ordered?", "Receipt product recognition"),
        ("vanilla matcha latte", "Specific product search"),
        
        # Technical documentation queries
        ("How does authentication work?", "Technical doc search"),
        ("What are the API endpoints?", "API documentation search"),
        
        # General queries
        ("What is the total amount?", "Receipt total search"),
        ("database settings", "Technical config search")
    ]
    
    for query, description in test_queries:
        print(f"\n--- Query: '{query}' ({description}) ---")
        try:
            response = pipeline.process_query(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_different_document_types() 