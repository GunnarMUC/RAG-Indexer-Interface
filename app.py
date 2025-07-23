from flask import Flask, render_template, request, jsonify
import os
import sys
from dotenv import load_dotenv

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize RAG pipeline
datastore = Datastore()
indexer = Indexer()
retriever = Retriever(datastore=datastore)
response_generator = ResponseGenerator()
evaluator = Evaluator()
pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors."""
    return '', 204  # No content response

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question asking via API."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided', 'status': 'error'}), 400
        
        # Process the question using hybrid search
        response = pipeline.process_query(question, use_hybrid_search=True)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing question: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/advanced', methods=['POST'])
def advanced_search():
    """Handle advanced search with metadata filtering."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        metadata_filter = data.get('metadata_filter', '')
        
        if not question:
            return jsonify({'error': 'No question provided', 'status': 'error'}), 400
        
        # Process with metadata filtering if provided
        if metadata_filter:
            response = pipeline.process_query(
                question, 
                use_hybrid_search=True,
                metadata_filter=metadata_filter
            )
        else:
            response = pipeline.process_query(question, use_hybrid_search=True)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing advanced search: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting RAG Pipeline Web Interface...")
    print("📝 Make sure your .env file contains your ANTHROPIC_API_KEY")
    print("🌐 The web interface will be available at: http://localhost:8080")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Initialize the pipeline with sample data
    try:
        print("📚 Initializing pipeline with sample data...")
        pipeline.reset()
        
        # Add sample documents
        sample_dir = os.path.join(os.path.dirname(__file__), 'sample_data', 'source')
        if os.path.exists(sample_dir):
            import glob
            document_paths = glob.glob(os.path.join(sample_dir, "*"))
            if document_paths:
                pipeline.add_documents(document_paths)
                print(f"✅ Loaded {len(document_paths)} sample documents")
            else:
                print("⚠️  No sample documents found")
        else:
            print("⚠️  Sample data directory not found")
            
    except Exception as e:
        print(f"⚠️  Error initializing pipeline: {e}")
        print("📝 You can still use the interface, but documents may not be loaded")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True) 