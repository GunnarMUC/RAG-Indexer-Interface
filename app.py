from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
import traceback

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize RAG pipeline with enhanced indexer
try:
    datastore = Datastore()
    # Use enhanced indexer for better product recognition
    pipeline = RAGPipeline(datastore)
    logger.info("✅ RAG Pipeline initialized successfully with Enhanced Indexer")
except Exception as e:
    logger.error(f"❌ Failed to initialize RAG Pipeline: {e}")
    pipeline = None

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors."""
    return '', 204

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'pipeline_ready': pipeline is not None
    })

@app.route('/api/ask', methods=['POST'])
@limiter.limit("10 per minute")
def ask_question():
    """Handle question asking via API with rate limiting."""
    try:
        if not pipeline:
            return jsonify({
                'error': 'RAG Pipeline not initialized',
                'status': 'error'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'status': 'error'
            }), 400

        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'No question provided',
                'status': 'error'
            }), 400

        logger.info(f"Processing question: {question[:100]}...")
        
        # Process the question using hybrid search
        response = pipeline.process_query(question, use_hybrid_search=True)
        
        logger.info("Question processed successfully")
        
        return jsonify({
            'response': response,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Error processing question: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/advanced', methods=['POST'])
@limiter.limit("5 per minute")
def advanced_search():
    """Handle advanced search with metadata filtering."""
    try:
        if not pipeline:
            return jsonify({
                'error': 'RAG Pipeline not initialized',
                'status': 'error'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'status': 'error'
            }), 400

        question = data.get('question', '').strip()
        metadata_filter = data.get('metadata_filter', '').strip()
        
        if not question:
            return jsonify({
                'error': 'No question provided',
                'status': 'error'
            }), 400

        logger.info(f"Processing advanced search: {question[:100]}...")
        
        # Process with metadata filtering if provided
        if metadata_filter:
            response = pipeline.process_query(
                question, 
                use_hybrid_search=True,
                metadata_filter=metadata_filter
            )
        else:
            response = pipeline.process_query(question, use_hybrid_search=True)
        
        logger.info("Advanced search processed successfully")
        
        return jsonify({
            'response': response,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing advanced search: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Error processing advanced search: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/upload', methods=['POST'])
@limiter.limit("5 per minute")
def upload_document():
    """Handle document upload and processing."""
    try:
        if not pipeline:
            return jsonify({
                'error': 'RAG Pipeline not initialized',
                'status': 'error'
            }), 503

        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'status': 'error'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'status': 'error'
            }), 400

        # Save file temporarily
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)
        
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Process the document
        try:
            items_added = pipeline.add_documents([file_path])
            logger.info(f"Successfully added {len(items_added)} items to database")
            
            # Verify the items were actually added
            current_count = pipeline.datastore.table.count_rows()
            logger.info(f"Database now contains {current_count} total items")
            
        except Exception as e:
            logger.error(f"Failed to add documents to pipeline: {e}")
            raise e
        
        # Clean up temporary file
        os.remove(file_path)
        
        logger.info("Document processed successfully")
        
        return jsonify({
            'message': f'Document "{file.filename}" processed successfully',
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing uploaded document: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Error processing document: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get system statistics."""
    try:
        if not pipeline:
            return jsonify({
                'error': 'RAG Pipeline not initialized',
                'status': 'error'
            }), 503

        # Get document count from database
        doc_count = pipeline.datastore.table.count_rows()
        
        # Get sample content for debugging
        sample_content = []
        if doc_count > 0:
            try:
                sample_data = pipeline.datastore.table.to_pandas().head(2)
                for _, row in sample_data.iterrows():
                    sample_content.append({
                        'source': row.get('source', 'Unknown'),
                        'content_preview': row.get('content', '')[:100] + '...' if len(row.get('content', '')) > 100 else row.get('content', '')
                    })
            except Exception as e:
                logger.warning(f"Could not get sample content: {e}")
        
        stats = {
            'document_count': doc_count,
            'sample_content': sample_content,
            'pipeline_ready': True,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': f'Error getting stats: {str(e)}',
            'status': 'error'
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded."""
    return jsonify({
        'error': 'Rate limit exceeded. Please try again later.',
        'status': 'error'
    }), 429

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting RAG Pipeline Web Interface...")
    print("📝 Make sure your .env file contains your ANTHROPIC_API_KEY")
    print("🌐 The web interface will be available at: http://localhost:8080")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Initialize the pipeline with sample data
    if pipeline:
        try:
            print("📚 Initializing pipeline with sample data...")
            
            # Check if database already has data
            count = pipeline.datastore.table.count_rows()
            if count > 0:
                print(f"✅ Database already contains {count} documents - skipping sample data")
            else:
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
    else:
        print("❌ Failed to initialize RAG Pipeline")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True) 