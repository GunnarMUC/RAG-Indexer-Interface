#!/usr/bin/env python3
"""
Test script to verify document upload and storage
"""
import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

def test_upload():
    """Test document upload and storage"""
    print("🧪 Testing Document Upload...")
    
    # Initialize components
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Check initial state
    initial_count = datastore.table.count_rows()
    print(f"📊 Initial database count: {initial_count}")
    
    # Create a test document
    test_content = """
    Restaurant Receipt
    ==================
    
    Date: 2024-07-24
    Time: 19:30
    
    Items:
    - Main Course: €15.50
    - Drink: €3.20
    - Dessert: €4.80
    
    Subtotal: €23.50
    Tax: €1.88
    Total: €25.38
    
    Trinkgeld: €0.22
    Final Total: €25.60
    
    Thank you for your visit!
    """
    
    # Create temporary file with .md extension (more likely to be supported)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_file_path = f.name
    
    try:
        print(f"📄 Created test file: {temp_file_path}")
        
        # Add document to pipeline
        items = pipeline.add_documents([temp_file_path])
        print(f"✅ Added {len(items)} items to database")
        
        # Check final state
        final_count = datastore.table.count_rows()
        print(f"📊 Final database count: {final_count}")
        
        # Test search
        print("\n🔍 Testing search for 'Trinkgeld':")
        results = datastore.search("Trinkgeld", top_k=3)
        if results:
            print(f"✅ Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"  {i+1}: {result[:200]}...")
        else:
            print("❌ No results found for 'Trinkgeld'")
        
        # Test search for amount
        print("\n🔍 Testing search for '0.22':")
        results = datastore.search("0.22", top_k=3)
        if results:
            print(f"✅ Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"  {i+1}: {result[:200]}...")
        else:
            print("❌ No results found for '0.22'")
        
        # Show sample content
        print("\n📄 Sample database content:")
        sample_data = datastore.table.to_pandas().tail(2)
        for i, row in sample_data.iterrows():
            print(f"\n--- Row {i+1} ---")
            print(f"Source: {row.get('source', 'Unknown')}")
            content = row.get('content', 'N/A')
            print(f"Content: {content[:300]}...")
            
    finally:
        # Clean up
        os.unlink(temp_file_path)
        print(f"🧹 Cleaned up test file")

if __name__ == "__main__":
    test_upload() 