"""
Configuration settings for RAG Indexer Interface
"""
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Application configuration"""
    
    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    CO_API_KEY: Optional[str] = os.getenv('CO_API_KEY')
    
    # Flask Settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8080'))
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = os.getenv('RATE_LIMIT_DEFAULT', '200 per day, 50 per hour')
    RATE_LIMIT_ASK: str = os.getenv('RATE_LIMIT_ASK', '10 per minute')
    RATE_LIMIT_UPLOAD: str = os.getenv('RATE_LIMIT_UPLOAD', '5 per minute')
    
    # Database Settings
    LANCEDB_PATH: str = os.getenv('LANCEDB_PATH', './data/rag_database')
    
    # File Upload Settings
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '16 * 1024 * 1024'))  # 16MB
    ALLOWED_EXTENSIONS: set = frozenset({'pdf', 'txt', 'doc', 'docx', 'md'})
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'app.log')
    
    # Model Settings
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'all-mpnet-base-v2')
    CHUNK_SIZE: int = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', '200'))
    
    # Search Settings
    TOP_K_RESULTS: int = int(os.getenv('TOP_K_RESULTS', '5'))
    SIMILARITY_THRESHOLD: float = float(os.getenv('SIMILARITY_THRESHOLD', '0.7'))
    
    # Sample Data
    SAMPLE_DATA_PATH: str = os.getenv('SAMPLE_DATA_PATH', './sample_data/source')
    EVAL_DATA_PATH: str = os.getenv('EVAL_DATA_PATH', './sample_data/eval/sample_questions.json')

# Global config instance
config = Config()

def validate_config() -> bool:
    """Validate that required configuration is present"""
    errors = []
    
    if not config.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is required")
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

def get_config_summary() -> dict:
    """Get a summary of current configuration"""
    return {
        'api_keys_configured': bool(config.ANTHROPIC_API_KEY),
        'cohere_configured': bool(config.CO_API_KEY),
        'debug_mode': config.DEBUG,
        'host': config.HOST,
        'port': config.PORT,
        'embedding_model': config.EMBEDDING_MODEL,
        'chunk_size': config.CHUNK_SIZE,
        'chunk_overlap': config.CHUNK_OVERLAP,
        'top_k_results': config.TOP_K_RESULTS,
        'similarity_threshold': config.SIMILARITY_THRESHOLD
    } 