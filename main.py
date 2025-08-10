# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from docling.datamodel import DoclingDoc

# --- SETUP ---
# Create the FastAPI app instance
app = FastAPI()

# Initialize the tools once when the server starts
# This is efficient because they are loaded into memory only one time.
converter = DocumentConverter()
chunker = HybridChunker()

# --- DATA MODELS ---
# Define the structure of the data your API will expect
class UrlRequest(BaseModel):
    source_url: str

class MarkdownRequest(BaseModel):
    markdown_text: str

# --- API ENDPOINTS ---

# This is Endpoint #1
@app.post("/process-url/")
def process_url_and_get_markdown(request: UrlRequest):
    """
    Receives a URL, converts the document, and returns the full markdown.
    """
    print(f"Processing URL: {request.source_url}")
    # Run the conversion
    result = converter.convert(request.source_url)
    markdown_output = result.document.export_to_markdown()
    
    # Return the result in a JSON format
    return {"source_url": request.source_url, "markdown_content": markdown_output}

# This is Endpoint #2
@app.post("/chunk-markdown/")
def chunk_markdown_text(request: MarkdownRequest):
    """
    Receives markdown text, chunks it, and returns the chunks.
    """
    print(f"Chunking markdown text of length: {len(request.markdown_text)}")
    # Dockling's chunker needs a DoclingDoc object, so we create one from the text
    doc_to_chunk = DoclingDoc.from_text(request.markdown_text)
    
    # Run the chunking
    chunks_iterator = chunker.chunk(doc_to_chunk)
    chunks_list = list(chunks_iterator) # Convert iterator to a list
    
    # Extract just the text from each chunk object
    chunk_texts = [chunk.text for chunk in chunks_list]
    
    # Return the result in a JSON format
    return {"chunk_count": len(chunk_texts), "chunks": chunk_texts}
