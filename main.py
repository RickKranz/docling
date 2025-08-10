# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from docling.datamodel.document import InputDocument
import tempfile
import pathlib

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
    """
    Receives markdown text, saves it to a temporary file, converts it to a rich
    docling object, chunks it, and returns the chunks.
    """
    print(f"Chunking markdown text of length: {len(request.markdown_text)}")
    
    # Create a temporary file to hold the markdown text
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, suffix=".md") as temp_file:
        temp_file.write(request.markdown_text)
        temp_file.flush() # Ensure all data is written to the file before reading

        # Convert the temporary file just like a normal document.
        # This creates the rich, structured object the chunker needs.
        result = converter.convert(pathlib.Path(temp_file.name))
        
        # Now, the rest of the logic will work perfectly
        chunks_iterator = chunker.chunk(result.document)
        chunks_list = list(chunks_iterator)
        chunk_texts = [chunk.text for chunk in chunks_list]
    
    return {"chunk_count": len(chunk_texts), "chunks": chunk_texts}