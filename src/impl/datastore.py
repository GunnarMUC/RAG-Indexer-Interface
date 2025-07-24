from typing import List
from interface.base_datastore import BaseDatastore, DataItem
import lancedb
from lancedb.table import Table
import pyarrow as pa
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor


class Datastore(BaseDatastore):

    DB_PATH = "data/sample-lancedb"
    DB_TABLE_NAME = "rag-table"

    def __init__(self):
        # Upgrade to better embedding model for improved accuracy
        self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
        self.vector_dimensions = self.embedding_model.get_sentence_embedding_dimension()
        self.vector_db = lancedb.connect(self.DB_PATH)
        self.table: Table = self._get_table()

    def reset(self) -> Table:
        # Drop the table if it exists
        try:
            self.vector_db.drop_table(self.DB_TABLE_NAME)
        except Exception as e:
            print("Unable to drop table. Assuming it doesn't exist.")

        # Create the new table.
        schema = pa.schema(
            [
                pa.field("vector", pa.list_(pa.float32(), self.vector_dimensions)),
                pa.field("content", pa.utf8()),
                pa.field("source", pa.utf8()),
                pa.field("metadata", pa.utf8()),  # Add metadata field for filtering
            ]
        )

        self.vector_db.create_table(self.DB_TABLE_NAME, schema=schema)
        self.table = self.vector_db.open_table(self.DB_TABLE_NAME)
        print(f"✅ Table Reset/Created: {self.DB_TABLE_NAME} in {self.DB_PATH}")
        return self.table

    def get_vector(self, content: str) -> List[float]:
        # Use sentence-transformers for embeddings
        embedding = self.embedding_model.encode(content)
        return embedding.tolist()

    def add_items(self, items: List[DataItem]) -> None:

        # Convert items to entries in parallel (since it's network bound).
        with ThreadPoolExecutor(max_workers=8) as executor:
            entries = list(executor.map(self._convert_item_to_entry, items))

        self.table.merge_insert(
            "source"
        ).when_matched_update_all().when_not_matched_insert_all().execute(entries)

    def search(self, query: str, top_k: int = 5, filter_metadata: str = None) -> List[str]:
        vector = self.get_vector(query)
        
        # Build search query
        search_query = (
            self.table.search(vector)
            .select(["content", "source", "metadata"])
            .limit(top_k)
        )
        
        # Add metadata filtering if provided
        if filter_metadata:
            search_query = search_query.where(f"metadata LIKE '%{filter_metadata}%'")
        
        results = search_query.to_list()
        result_content = [result.get("content") for result in results]
        return result_content

    def _get_table(self) -> Table:
        try:
            return self.vector_db.open_table(self.DB_TABLE_NAME)
        except Exception as e:
            print(f"Error opening table. Resetting the datastore: {e}")
            # Force recreate the database directory
            import os
            import shutil
            if os.path.exists(self.DB_PATH):
                shutil.rmtree(self.DB_PATH)
            os.makedirs(self.DB_PATH, exist_ok=True)
            return self.reset()

    def _convert_item_to_entry(self, item: DataItem) -> dict:
        """Convert a DataItem to match table schema."""
        vector = self.get_vector(item.content)
        
        # Extract metadata from source for filtering
        metadata = self._extract_metadata(item.source)
        
        return {
            "vector": vector,
            "content": item.content,
            "source": item.source,
            "metadata": metadata,
        }
    
    def _extract_metadata(self, source: str) -> str:
        """Extract metadata from source for filtering."""
        # Extract filename and section info
        if ":" in source:
            filename = source.split(":")[0]
            section = source.split(":")[1] if len(source.split(":")) > 1 else ""
            return f"{filename} {section}"
        return source
