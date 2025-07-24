#!/usr/bin/env python3
"""
Auto-update script for RAG pipeline.
Watches the source directory for new files and automatically re-indexes.
"""

import os
import sys
import time
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator

class SourceFileHandler(FileSystemEventHandler):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.last_update = time.time()
        self.update_cooldown = 30  # Wait 30 seconds between updates
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.pdf', '.docx', '.txt', '.xlsx')):
            self._schedule_update()
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.pdf', '.docx', '.txt', '.xlsx')):
            self._schedule_update()
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(('.pdf', '.docx', '.txt', '.xlsx')):
            self._schedule_update()
    
    def _schedule_update(self):
        current_time = time.time()
        if current_time - self.last_update > self.update_cooldown:
            print(f"🔄 Detected file changes, updating database...")
            self._update_database()
            self.last_update = current_time
    
    def _update_database(self):
        try:
            # Reset and re-index
            self.pipeline.reset()
            
            # Get all files from source directory
            source_dir = os.path.join(os.path.dirname(__file__), 'sample_data', 'source')
            document_paths = glob.glob(os.path.join(source_dir, "*"))
            
            if document_paths:
                self.pipeline.add_documents(document_paths)
                print(f"✅ Updated database with {len(document_paths)} files")
            else:
                print("⚠️  No source files found")
                
        except Exception as e:
            print(f"❌ Error updating database: {e}")

def start_auto_update():
    """Start the auto-update service."""
    print("🚀 Starting RAG Pipeline Auto-Update Service...")
    print("📁 Watching sample_data/source/ for file changes")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    # Initialize pipeline
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    pipeline = RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)
    
    # Initial indexing
    try:
        print("📚 Initial indexing...")
        pipeline.reset()
        source_dir = os.path.join(os.path.dirname(__file__), 'sample_data', 'source')
        document_paths = glob.glob(os.path.join(source_dir, "*"))
        if document_paths:
            pipeline.add_documents(document_paths)
            print(f"✅ Initial indexing complete: {len(document_paths)} files")
        else:
            print("⚠️  No source files found for initial indexing")
    except Exception as e:
        print(f"❌ Error during initial indexing: {e}")
    
    # Set up file watcher
    event_handler = SourceFileHandler(pipeline)
    observer = Observer()
    observer.schedule(event_handler, 'sample_data/source/', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Stopping auto-update service...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_auto_update() 