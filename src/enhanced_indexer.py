#!/usr/bin/env python3
"""
Enhanced Indexer for better product recognition in receipts and structured documents
"""
import os
import re
from typing import List, Dict, Any
from interface.base_datastore import DataItem
from impl.indexer import Indexer
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker, DocChunk


class EnhancedIndexer(Indexer):
    def __init__(self):
        self.converter = DocumentConverter()
        # Smaller chunks for better product recognition
        self.chunker = HybridChunker(
            chunk_size=256,  # Smaller chunks for detailed items
            chunk_overlap=100,  # More overlap to preserve context
            min_chunk_size=50,  # Allow smaller chunks for products
            max_chunk_size=512   # Reasonable max for receipts
        )
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        
        # Use the same database path as the regular indexer
        self.datastore = None  # Will be set by the pipeline

    def index(self, document_paths: List[str]) -> List[DataItem]:
        items = []
        for document_path in document_paths:
            document = self.converter.convert(document_path).document
            chunks: List[DocChunk] = self.chunker.chunk(document)
            
            # Enhanced processing for receipts
            if self._is_receipt_document(document_path):
                items.extend(self._process_receipt_chunks(chunks, document_path))
            else:
                items.extend(self._items_from_chunks(chunks))
                
        return items

    def _is_receipt_document(self, document_path: str) -> bool:
        """Detect if document is likely a receipt."""
        receipt_indicators = [
            'receipt', 'bill', 'invoice', 'check', 'tab',
            'total', 'subtotal', 'tax', 'tip', 'trinkgeld',
            '€', '$', 'amount', 'price'
        ]
        
        # Check filename
        filename = os.path.basename(document_path).lower()
        if any(indicator in filename for indicator in receipt_indicators):
            return True
            
        return False

    def _process_receipt_chunks(self, chunks: List[DocChunk], document_path: str) -> List[DataItem]:
        """Enhanced processing for receipt documents."""
        items = []
        
        for i, chunk in enumerate(chunks):
            content = chunk.text
            
            # Extract structured data from receipt
            structured_data = self._extract_receipt_data(content)
            
            # Create multiple items for better searchability
            items.extend(self._create_receipt_items(structured_data, chunk, i, document_path))
            
        return items

    def _extract_receipt_data(self, content: str) -> Dict[str, Any]:
        """Extract structured data from receipt content."""
        data = {
            'items': [],
            'total': None,
            'tax': None,
            'tip': None,
            'date': None,
            'time': None,
            'restaurant': None
        }
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Extract items with prices
            item_match = re.search(r'([^€$]*?)\s*[€$]\s*(\d+\.?\d*)', line)
            if item_match:
                item_name = item_match.group(1).strip()
                price = item_match.group(2)
                
                # Clean up item name
                item_name = re.sub(r'^\s*[-•*]\s*', '', item_name)
                item_name = re.sub(r'\s+', ' ', item_name).strip()
                
                if item_name and item_name.lower() not in ['total', 'subtotal', 'tax', 'tip', 'trinkgeld']:
                    data['items'].append({
                        'name': item_name,
                        'price': price,
                        'type': self._categorize_item(item_name)
                    })
            
            # Extract totals
            if 'total' in line.lower() and not data['total']:
                total_match = re.search(r'[€$]\s*(\d+\.?\d*)', line)
                if total_match:
                    data['total'] = total_match.group(1)
            
            # Extract tax
            if 'tax' in line.lower() and not data['tax']:
                tax_match = re.search(r'[€$]\s*(\d+\.?\d*)', line)
                if tax_match:
                    data['tax'] = tax_match.group(1)
            
            # Extract tip/trinkgeld
            if any(word in line.lower() for word in ['tip', 'trinkgeld']) and not data['tip']:
                tip_match = re.search(r'[€$]\s*(\d+\.?\d*)', line)
                if tip_match:
                    data['tip'] = tip_match.group(1)
            
            # Extract date/time
            date_match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', line)
            if date_match and not data['date']:
                data['date'] = date_match.group(1)
            
            time_match = re.search(r'(\d{1,2}:\d{2})', line)
            if time_match and not data['time']:
                data['time'] = time_match.group(1)
        
        return data

    def _categorize_item(self, item_name: str) -> str:
        """Categorize items for better search."""
        item_lower = item_name.lower()
        
        # Drink categories
        if any(word in item_lower for word in ['latte', 'coffee', 'tea', 'juice', 'soda', 'water', 'drink', 'beverage']):
            return 'drink'
        
        # Food categories
        if any(word in item_lower for word in ['main', 'course', 'entree', 'dish', 'meal', 'food']):
            return 'food'
        
        # Dessert categories
        if any(word in item_lower for word in ['dessert', 'cake', 'ice cream', 'sweet', 'pastry']):
            return 'dessert'
        
        # Default
        return 'item'

    def _create_receipt_items(self, data: Dict[str, Any], chunk: DocChunk, chunk_index: int, document_path: str) -> List[DataItem]:
        """Create multiple searchable items from receipt data."""
        items = []
        
        # Original content item
        original_content = self._preprocess_content(chunk.text)
        items.append(DataItem(
            content=original_content,
            source=f"{os.path.basename(document_path)}:chunk_{chunk_index}"
        ))
        
        # Structured items for each product
        for i, item in enumerate(data['items']):
            # Create detailed item description
            item_content = f"""
Product: {item['name']}
Category: {item['type']}
Price: €{item['price']}
Source: Receipt from {os.path.basename(document_path)}
"""
            
            items.append(DataItem(
                content=item_content.strip(),
                source=f"{os.path.basename(document_path)}:item_{i}"
            ))
            
            # Create searchable variations
            if item['type'] == 'drink':
                drink_content = f"""
Drink Item: {item['name']}
Price: €{item['price']}
Type: Beverage
"""
                items.append(DataItem(
                    content=drink_content.strip(),
                    source=f"{os.path.basename(document_path)}:drink_{i}"
                ))
        
        # Summary item
        if data['items']:
            summary_content = f"""
Receipt Summary:
Items: {len(data['items'])} items
Total: €{data['total'] or 'N/A'}
Tax: €{data['tax'] or 'N/A'}
Tip: €{data['tip'] or 'N/A'}
Date: {data['date'] or 'N/A'}
"""
            items.append(DataItem(
                content=summary_content.strip(),
                source=f"{os.path.basename(document_path)}:summary"
            ))
        
        return items

    def _items_from_chunks(self, chunks: List[DocChunk]) -> List[DataItem]:
        """Standard processing for non-receipt documents."""
        items = []
        for i, chunk in enumerate(chunks):
            content_headings = "## " + ", ".join(chunk.meta.headings) if chunk.meta.headings else ""
            content_text = self._preprocess_content(chunk.text)
            
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
        text = re.sub(r'\s+', ' ', text)
        
        if len(text.strip()) < 20:
            return ""
        
        text = text.replace('\n\n\n', '\n\n')
        text = text.replace('\t', ' ')
        text = text.strip()
        
        return text 