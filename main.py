# main.py - Final Working Version

from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
import pathlib

# --- IMPORTS WE HAVE CONFIRMED ARE CORRECT ---
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from docling.datamodel.document import DoclingDocument


# --- SETUP ---
app = FastAPI()
converter = DocumentConverter()

# This is the final, correct chunker setup. Since merge_peers=True is the default,
# you can simply write chunker = HybridChunker(). We'll write it explicitly for clarity.
chunker = HybridChunker(merge_peers=True)


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
    """
    Receives markdown text, saves it to a temporary file, converts it to a rich
    docling object, chunks it, and returns the chunks.
    """
    print(f"Chunking markdown text of length: {len(request.markdown_text)}")
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, suffix=".md") as temp_file:
        temp_file.write(request.markdown_text)
        temp_file.flush()

        result = converter.convert(pathlib.Path(temp_file.name))
        
        chunks_iterator = chunker.chunk(result.document)
        chunks_list = list(chunks_iterator)
        chunk_texts = [chunk.text for chunk in chunks_list]
    
    return {"chunk_count": len(chunk_texts), "chunks": chunk_texts}