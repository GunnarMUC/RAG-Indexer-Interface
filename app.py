from flask import Flask, render_template, request, jsonify
import sys
import os
import glob

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

app = Flask(__name__)

def get_files_in_directory(source_path: str):
    """Get all files in a directory, similar to main.py"""
    if os.path.isfile(source_path):
        return [source_path]
    return glob.glob(os.path.join(source_path, "*"))

# Initialize the RAG pipeline
def create_pipeline():
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    return RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)

# Global pipeline instance
pipeline = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global pipeline
    
    try:
        # Initialize pipeline if not already done
        if pipeline is None:
            pipeline = create_pipeline()
            # Reset and add documents
            pipeline.reset()
            # Get all files from the source directory
            source_dir = os.path.join(os.path.dirname(__file__), 'sample_data', 'source')
            document_paths = get_files_in_directory(source_dir)
            if document_paths:
                pipeline.add_documents(document_paths)
        
        # Get the question from the request
        data = request.get_json()
        question = data.get('question', '')
        use_hybrid_search = data.get('use_hybrid_search', True)  # Default to hybrid search
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Process the question and get response using improved search
        response = pipeline.process_query(question, use_hybrid_search=use_hybrid_search)
        
        return jsonify({
            'question': question,
            'answer': response,
            'status': 'success',
            'search_method': 'hybrid' if use_hybrid_search else 'vector_only'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing question: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/search', methods=['POST'])
def search():
    """Advanced search endpoint with filtering."""
    global pipeline
    
    try:
        if pipeline is None:
            return jsonify({'error': 'Pipeline not initialized'}), 400
        
        data = request.get_json()
        query = data.get('query', '')
        filter_metadata = data.get('filter', None)
        top_k = data.get('top_k', 10)
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Use the new search with filtering
        results = pipeline.search_with_filter(query, filter_metadata, top_k)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error searching: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 