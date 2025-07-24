from typing import List
from interface.base_retriever import BaseRetriever
from interface.base_datastore import BaseDatastore
import re


class Retriever(BaseRetriever):
    def __init__(self, datastore: BaseDatastore):
        self.datastore = datastore

    def search(self, query: str, top_k: int = 10) -> List[str]:
        """Legacy search method for compatibility."""
        return self.retrieve(query, top_k, use_hybrid_search=True)

    def retrieve(self, query: str, top_k: int = 10, use_hybrid_search: bool = True) -> List[str]:
        """
        Retrieve relevant documents using hybrid search (keyword + vector).
        
        Args:
            query: The search query
            top_k: Number of results to return
            use_hybrid_search: Whether to use hybrid search (keyword + vector)
        """
        if use_hybrid_search:
            return self._hybrid_search(query, top_k)
        else:
            return self.datastore.search(query, top_k)
    
    def _hybrid_search(self, query: str, top_k: int = 10) -> List[str]:
        """Perform hybrid search combining keyword and vector search."""
        # Extract keywords from query
        keywords = self._extract_keywords(query)
        
        # Get vector search results
        vector_results = self.datastore.search(query, top_k * 2)  # Get more for reranking
        
        # Get keyword search results
        keyword_results = []
        if keywords:
            for keyword in keywords[:3]:  # Use top 3 keywords
                keyword_results.extend(self.datastore.search(keyword, top_k // 2))
        
        # Combine and rerank results
        combined_results = self._combine_and_rerank_results(
            vector_results, keyword_results, query, top_k
        )
        
        return combined_results
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from the query."""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'what', 'when', 'where', 'why', 'how',
            'der', 'die', 'das', 'und', 'oder', 'aber', 'in', 'auf', 'an', 'zu',
            'für', 'von', 'mit', 'bei', 'ist', 'sind', 'war', 'waren', 'sein',
            'haben', 'hat', 'hatte', 'wird', 'würde', 'könnte', 'sollte', 'kann',
            'was', 'wann', 'wo', 'warum', 'wie'
        }
        
        # Clean and split query
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def _combine_and_rerank_results(self, vector_results: List[str], 
                                   keyword_results: List[str], 
                                   query: str, top_k: int) -> List[str]:
        """Combine and rerank results based on relevance."""
        # Create a combined list with scores
        all_results = {}
        
        # Extract query terms for relevance scoring
        query_terms = self._extract_keywords(query)
        query_lower = query.lower()
        
        # Score vector results (higher weight)
        for i, result in enumerate(vector_results):
            score = len(vector_results) - i  # Higher score for earlier results
            
            # Boost score if result contains query terms
            result_lower = result.lower()
            term_matches = sum(1 for term in query_terms if term in result_lower)
            if term_matches > 0:
                score += term_matches * 10  # Significant boost for term matches
            
            # Extra boost for exact phrase matches
            if query_lower in result_lower:
                score += 20
            
            all_results[result] = all_results.get(result, 0) + score * 2
        
        # Score keyword results
        for i, result in enumerate(keyword_results):
            score = len(keyword_results) - i
            
            # Boost score if result contains query terms
            result_lower = result.lower()
            term_matches = sum(1 for term in query_terms if term in result_lower)
            if term_matches > 0:
                score += term_matches * 10
            
            all_results[result] = all_results.get(result, 0) + score
        
        # Sort by score and return top_k
        sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
        
        return [result for result, score in sorted_results[:top_k]]
