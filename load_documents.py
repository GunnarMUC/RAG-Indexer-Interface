#!/usr/bin/env python3
"""
Script to manually load documents into the database
"""
import sys
import os
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

def load_documents():
    """Load documents into the database"""
    print("🔄 Loading documents into database...")
    
    # Initialize components
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Reset database
    print("🗑️  Resetting database...")
    pipeline.reset()
    
    # Get document paths
    sample_dir = "sample_data/source"
    document_paths = glob.glob(os.path.join(sample_dir, "*.pdf"))
    
    print(f"📄 Found {len(document_paths)} PDF documents:")
    for path in document_paths:
        print(f"  - {os.path.basename(path)}")
    
    # Add documents
    if document_paths:
        pipeline.add_documents(document_paths)
        print("✅ Documents loaded successfully!")
        
        # Test the database
        count = datastore.table.count_rows()
        print(f"📊 Database now contains {count} rows")
        
        # Test a simple search
        print("\n🔍 Testing search...")
        results = datastore.search("attraktionen", top_k=3)
        print(f"Found {len(results)} results for 'attraktionen'")
        for i, result in enumerate(results):
            print(f"  {i+1}: {result[:100]}...")
            
    else:
        print("❌ No PDF documents found!")

if __name__ == "__main__":
    load_documents() 