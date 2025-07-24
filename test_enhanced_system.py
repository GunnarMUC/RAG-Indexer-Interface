#!/usr/bin/env python3
"""
Test script to verify enhanced indexing system with specific product names
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore

def test_enhanced_system():
    """Test the enhanced indexing system with specific product names"""
    print("🧪 Testing Enhanced Indexing System...")
    
    # Initialize pipeline with enhanced indexer
    datastore = Datastore()
    pipeline = RAGPipeline(datastore)
    
    # Reset database
    print("🗑️  Resetting database...")
    pipeline.reset()
    
    # Add test receipt with specific product names
    receipt_path = "test_receipt.md"
    print(f"📄 Adding receipt: {receipt_path}")
    
    try:
        items = pipeline.add_documents([receipt_path])
        print(f"✅ Added {len(items)} items to database")
        
        # Test database content
        count = datastore.table.count_rows()
        print(f"📊 Database now contains {count} items")
        
        # Test specific product queries
        test_queries = [
            "What drink was ordered?",
            "Which beverage was purchased?",
            "What type of latte was bought?",
            "What dessert was ordered?",
            "What main course was ordered?",
            "vanilla matcha latte",
            "matcha",
            "latte",
            "salmon",
            "cheesecake"
        ]
        
        print("\n🔍 Testing Product Recognition:")
        for query in test_queries:
            print(f"\n--- Query: '{query}' ---")
            try:
                response = pipeline.process_query(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")
        
        # Show database content
        print("\n📋 Database Content:")
        try:
            sample_data = datastore.table.to_pandas().head(5)
            for i, row in sample_data.iterrows():
                print(f"\n--- Row {i+1} ---")
                print(f"Source: {row.get('source', 'Unknown')}")
                content = row.get('content', 'N/A')
                print(f"Content: {content[:200]}...")
        except Exception as e:
            print(f"Error reading database: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_enhanced_system() 