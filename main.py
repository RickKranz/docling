# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
# --- CORRECTED: Import the real class name ---
from docling.datamodel.document import InputDocument

# --- SETUP ---
app = FastAPI()
converter = DocumentConverter()
chunker = HybridChunker()

# --- DATA MODELS ---
class UrlRequest(BaseModel):
    source_url: str

class MarkdownRequest(BaseModel):
    markdown_text: str

# --- API ENDPOINTS ---

@app.post("/process-url/")
def process_url_and_get_markdown(request: UrlRequest):
    print(f"Processing URL: {request.source_url}")
    result = converter.convert(request.source_url)
    markdown_output = result.document.export_to_markdown()
    return {"source_url": request.source_url, "markdown_content": markdown_output}

@app.post("/chunk-markdown/")
def chunk_markdown_text(request: MarkdownRequest):
    print(f"Chunking markdown text of length: {len(request.markdown_text)}")
    
    # --- CORRECTED: Use the real class name here ---
    doc_to_chunk = InputDocument.from_text(request.markdown_text)
    
    chunks_iterator = chunker.chunk(doc_to_chunk)
    chunks_list = list(chunks_iterator)
    chunk_texts = [chunk.text for chunk in chunks_list]
    
    return {"chunk_count": len(chunk_texts), "chunks": chunk_texts}