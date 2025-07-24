#!/usr/bin/env python3
"""
Test script to see what context is retrieved for specific queries
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

def test_context_retrieval():
    """Test what context is retrieved for specific queries"""
    print("🔍 Testing Context Retrieval...")
    
    # Initialize components
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Test queries
    test_queries = [
        "How much Trinkgeld was given?",
        "Trinkgeld",
        "0.22",
        "restaurant receipt",
        "tipping amount"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 Query: '{query}'")
        print(f"{'='*60}")
        
        # Get search results
        search_results = retriever.retrieve(query, top_k=5, use_hybrid_search=True)
        
        print(f"📊 Found {len(search_results)} results:")
        
        for i, result in enumerate(search_results):
            print(f"\n--- Result {i+1} ---")
            print(f"Content: {result[:300]}...")
            
            # Check if it contains relevant terms
            relevant_terms = ['trinkgeld', '0.22', 'restaurant', 'receipt', 'tip']
            found_terms = [term for term in relevant_terms if term.lower() in result.lower()]
            if found_terms:
                print(f"✅ Contains relevant terms: {found_terms}")
            else:
                print("❌ No relevant terms found")
        
        # Test vector search only
        print(f"\n🔍 Vector search only for '{query}':")
        vector_results = datastore.search(query, top_k=3)
        for i, result in enumerate(vector_results):
            print(f"  {i+1}: {result[:100]}...")
        
        # Test keyword search
        print(f"\n🔍 Keyword search for '{query}':")
        keywords = retriever._extract_keywords(query)
        print(f"Extracted keywords: {keywords}")
        
        for keyword in keywords[:2]:
            keyword_results = datastore.search(keyword, top_k=2)
            print(f"  Keyword '{keyword}': {len(keyword_results)} results")
            for j, result in enumerate(keyword_results):
                print(f"    {j+1}: {result[:100]}...")

if __name__ == "__main__":
    test_context_retrieval() 