import os
from typing import List
from interface.base_datastore import DataItem
from interface.base_indexer import BaseIndexer
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker, DocChunk
import re


class Indexer(BaseIndexer):
    def __init__(self):
        self.converter = DocumentConverter()
        # Improved chunking parameters for better results
        self.chunker = HybridChunker(
            chunk_size=512,  # Optimal size for most models
            chunk_overlap=50,  # Good overlap for context preservation
            min_chunk_size=100,  # Minimum chunk size
            max_chunk_size=800   # Maximum chunk size
        )
        # Disable tokenizers parallelism to avoid OOM errors.
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    def index(self, document_paths: List[str]) -> List[DataItem]:
        items = []
        for document_path in document_paths:
            document = self.converter.convert(document_path).document
            chunks: List[DocChunk] = self.chunker.chunk(document)
            items.extend(self._items_from_chunks(chunks))
        return items

    def _items_from_chunks(self, chunks: List[DocChunk]) -> List[DataItem]:
        items = []
        for i, chunk in enumerate(chunks):
            # Improved content formatting with better structure
            content_headings = "## " + ", ".join(chunk.meta.headings) if chunk.meta.headings else ""
            content_text = self._preprocess_content(chunk.text)
            
            # Combine headings and content with better formatting
            if content_headings:
                final_content = f"{content_headings}\n{content_text}"
            else:
                final_content = content_text
            
            source = f"{chunk.meta.origin.filename}:{i}"
            item = DataItem(content=final_content, source=source)
            items.append(item)

        return items
    
    def _preprocess_content(self, text: str) -> str:
        """Preprocess content for better embedding quality."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove very short chunks that might be noise
        if len(text.strip()) < 20:
            return ""
        
        # Clean up common formatting issues
        text = text.replace('\n\n\n', '\n\n')
        text = text.replace('\t', ' ')
        
        # Ensure proper sentence endings
        text = text.strip()
        
        return text
