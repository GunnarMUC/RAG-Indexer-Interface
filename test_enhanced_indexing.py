#!/usr/bin/env python3
"""
Test script to demonstrate enhanced indexing for product recognition
"""
import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_indexer import EnhancedIndexer
from impl import Datastore, Retriever

def test_enhanced_indexing():
    """Test enhanced indexing for product recognition"""
    print("🧪 Testing Enhanced Indexing for Product Recognition...")
    
    # Create a realistic receipt with specific product names
    receipt_content = """
    RESTAURANT RECEIPT
    ==================
    
    Date: 2024-07-24
    Time: 19:30
    
    Items:
    - Grilled Salmon with Vegetables €15.50
    - Vanilla Matcha Latte €3.20
    - Chocolate Cheesecake €4.80
    
    Subtotal: €23.50
    Tax: €1.88
    Total: €25.38
    
    Trinkgeld: €0.22
    Final Total: €25.60
    
    Thank you for your visit!
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(receipt_content)
        temp_file_path = f.name
    
    try:
        print(f"📄 Created test receipt: {temp_file_path}")
        
        # Test enhanced indexing
        enhanced_indexer = EnhancedIndexer()
        items = enhanced_indexer.index([temp_file_path])
        
        print(f"✅ Enhanced indexing created {len(items)} items")
        
        # Show the structured items
        print("\n📋 Structured Items Created:")
        for i, item in enumerate(items):
            print(f"\n--- Item {i+1} ---")
            print(f"Source: {item.source}")
            print(f"Content: {item.content[:200]}...")
        
        # Test search functionality
        print("\n🔍 Testing Search Functionality:")
        
        # Initialize datastore and retriever
        datastore = Datastore()
        datastore.add_items(items)
        retriever = Retriever(datastore=datastore)
        
        # Test various search queries
        test_queries = [
            "vanilla matcha latte",
            "drink",
            "latte",
            "matcha",
            "vanilla",
            "beverage",
            "salmon",
            "cheesecake",
            "dessert"
        ]
        
        for query in test_queries:
            print(f"\n--- Searching for: '{query}' ---")
            results = retriever.retrieve(query, top_k=3, use_hybrid_search=True)
            
            if results:
                print(f"✅ Found {len(results)} results:")
                for j, result in enumerate(results[:2]):
                    print(f"  {j+1}: {result[:150]}...")
            else:
                print("❌ No results found")
        
        # Test specific product queries
        print("\n🎯 Testing Specific Product Queries:")
        specific_queries = [
            "What drink was ordered?",
            "Which beverage was purchased?",
            "What type of latte was bought?",
            "What dessert was ordered?"
        ]
        
        for query in specific_queries:
            print(f"\n--- Query: '{query}' ---")
            results = retriever.retrieve(query, top_k=3, use_hybrid_search=True)
            
            if results:
                print(f"✅ Found {len(results)} results:")
                for j, result in enumerate(results[:2]):
                    print(f"  {j+1}: {result[:150]}...")
            else:
                print("❌ No results found")
                
    finally:
        # Clean up
        os.unlink(temp_file_path)
        print(f"\n🧹 Cleaned up test file")

if __name__ == "__main__":
    test_enhanced_indexing() 