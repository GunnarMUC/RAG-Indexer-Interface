#!/usr/bin/env python3
"""
Test script to compare the improved RAG pipeline performance.
"""

import sys
import os
import time

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

def test_improvements():
    """Test the improved RAG pipeline."""
    print("🚀 Testing Improved RAG Pipeline")
    print("=" * 50)
    
    # Create pipeline
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Reset and add documents
    print("📚 Loading documents...")
    pipeline.reset()
    
    source_dir = os.path.join(os.path.dirname(__file__), 'sample_data', 'source')
    import glob
    document_paths = glob.glob(os.path.join(source_dir, "*"))
    pipeline.add_documents(document_paths)
    
    # Test questions
    test_questions = [
        "What is the Golden Lake?",
        "What hotels are available in Goldlake View?",
        "When was Goldlake View founded?",
        "What activities can I do in Goldlake View?",
        "Tell me about the history of Goldlake View"
    ]
    
    print("\n🧪 Testing Questions:")
    print("-" * 30)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        # Test hybrid search
        start_time = time.time()
        response_hybrid = pipeline.process_query(question, use_hybrid_search=True)
        hybrid_time = time.time() - start_time
        
        # Test vector-only search
        start_time = time.time()
        response_vector = pipeline.process_query(question, use_hybrid_search=False)
        vector_time = time.time() - start_time
        
        print(f"   Hybrid Search Time: {hybrid_time:.2f}s")
        print(f"   Vector Search Time: {vector_time:.2f}s")
        print(f"   Response Length: {len(response_hybrid)} chars")
        
        # Show first 200 chars of response
        preview = response_hybrid[:200] + "..." if len(response_hybrid) > 200 else response_hybrid
        print(f"   Preview: {preview}")
    
    # Test metadata filtering
    print("\n🔍 Testing Metadata Filtering:")
    print("-" * 30)
    
    filter_tests = [
        ("hotel", "Filter by hotel-related content"),
        ("geschichte", "Filter by history-related content"),
        ("see", "Filter by lake-related content")
    ]
    
    for filter_term, description in filter_tests:
        print(f"\n{description}:")
        results = pipeline.search_with_filter("Goldlake View", filter_metadata=filter_term, top_k=3)
        print(f"   Found {len(results)} results for filter '{filter_term}'")
        for j, result in enumerate(results, 1):
            preview = result[:100] + "..." if len(result) > 100 else result
            print(f"   {j}. {preview}")
    
    print("\n✅ Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_improvements() 