from typing import List
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator
from enhanced_indexer import EnhancedIndexer
from interface.base_datastore import DataItem
from interface.base_evaluator import EvaluationResult
import json


class RAGPipeline:
    def __init__(
        self,
        datastore: Datastore,
        indexer: Indexer = None,
        retriever: Retriever = None,
        response_generator: ResponseGenerator = None,
        evaluator: Evaluator = None,
    ):
        self.datastore = datastore
        # Use enhanced indexer by default for better product recognition
        self.indexer = indexer if indexer else EnhancedIndexer()
        self.retriever = retriever if retriever else Retriever(datastore=datastore)
        self.response_generator = response_generator if response_generator else ResponseGenerator()
        self.evaluator = evaluator if evaluator else Evaluator()

    def reset(self) -> None:
        """Reset the database."""
        self.datastore.reset()

    def add_documents(self, document_paths: List[str]) -> List[DataItem]:
        """Add documents to the database."""
        items = self.indexer.index(document_paths)
        self.datastore.add_items(items)
        print(f"✅ Added {len(items)} items to the datastore.")
        return items

    def process_query(self, query: str, use_hybrid_search: bool = True) -> str:
        """Process a query and return a response."""
        # Use improved hybrid search
        search_results = self.retriever.retrieve(
            query, 
            top_k=10, 
            use_hybrid_search=use_hybrid_search
        )
        
        # Generate response using the search results
        response = self.response_generator.generate_response(query, search_results)
        return response

    def evaluate(self, questions: List[dict]) -> List[EvaluationResult]:
        """Evaluate the pipeline on a set of questions."""
        results = []
        
        for question_data in questions:
            question = question_data["question"]
            expected_answer = question_data["expected_answer"]
            
            # Get response using hybrid search
            response = self.process_query(question, use_hybrid_search=True)
            
            # Evaluate the response
            result = self.evaluator.evaluate(question, response, expected_answer)
            results.append(result)
        
        return results

    def search_with_filter(self, query: str, filter_metadata: str = None, top_k: int = 10) -> List[str]:
        """Search with optional metadata filtering."""
        return self.datastore.search(query, top_k, filter_metadata)
