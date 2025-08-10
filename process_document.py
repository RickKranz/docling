from docling.document_converter import DocumentConverter
import time 

from docling.chunking import HybridChunker

print("--> Script started.")

source = input("--> Please enter the full URL or local path to your PDF file: ")

print(f"--> Received source: {source}")
print("--> Step 1: Initializing the converter...")

converter = DocumentConverter()

print("--> Step 2: Starting conversion. This is the slow part, please wait...")

start_time = time.time()
result = converter.convert(source) 
end_time = time.time()

processing_time = end_time - start_time

print(f"--> Step 3: Conversion complete! It took {processing_time:.2f} seconds.")

# --- NEW: Print the full document before chunking ---
print("\n--- Full Converted Document (Markdown) ---")
print(result.document.export_to_markdown())
print("-" * 40 + "\n")

# ----------------------------------------------------------------------
# --- CHUNKING SECTION ---
# ----------------------------------------------------------------------

print("\n--> Step 4: Chunking the document with the Hybrid Chunker...")

chunker = HybridChunker()

chunks = list(chunker.chunk(result.document))

print(f"--> Step 5: Document successfully split into {len(chunks)} chunks.")
print("\n--- Displaying Chunks ---")

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} (Size: {len(chunk.text)} chars) ---")
    print(chunk.text)
    print("-" * 20 + "\n")