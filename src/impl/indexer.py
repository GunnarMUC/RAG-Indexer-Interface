from typing import List
from interface.base_datastore import DataItem
from interface.base_indexer import BaseIndexer
import PyPDF2


class Indexer(BaseIndexer):

    def index(self, document_paths: List[str]) -> List[DataItem]:
        items = []
        for document_path in document_paths:
            new_items = self._simple_pdf_chunker(document_path)
            items.extend(new_items)

        print(
            f"✅ Indexer: Created {len(items)} data items from {len(document_paths)} documents."
        )
        return items

    def _simple_pdf_chunker(
        self, pdf_path: str, chunk_size: int = 200
    ) -> List[DataItem]:

        items = []
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            doc_index = 0

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text().strip().replace("\n", "")
                start_index = 0

                while start_index < len(page_text):
                    end_index = min(start_index + chunk_size, len(page_text))
                    chunk = page_text[start_index:end_index]
                    source = f"{pdf_path}:{doc_index}"
                    item = DataItem(content=chunk, source=source)
                    items.append(item)
                    start_index = end_index
                    doc_index += 1

        return items
