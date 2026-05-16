import os
import re
import fitz
import chromadb
from sentence_transformers import SentenceTransformer


# =========================
# EMBEDDING MODEL
# =========================

print("Loading Embedding Model...")

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

print("Embedding model loaded!")


# =========================
# CHROMADB SETUP
# =========================

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="rag_collection")


# =========================
# PDF TEXT EXTRACTION
# =========================

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


# =========================
# TEXT CLEANING
# =========================

def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Page \d+", "", text)
    return text.strip()


# =========================
# SIMPLE CHUNKING 
# =========================

def split_text(text, chunk_size=700, overlap=120):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# =========================
# PROCESS PDFS
# =========================

DATA_FOLDER = "data"

all_chunks = []
all_metadata = []
all_ids = []

chunk_id = 0

for filename in os.listdir(DATA_FOLDER):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(DATA_FOLDER, filename)

        print(f"\nProcessing PDF: {filename}")

        # Extract text
        raw_text = extract_text_from_pdf(pdf_path)
        print("Text extracted")

        # Clean text
        cleaned_text = clean_text(raw_text)
        print("Text cleaned")

        # Chunk text
        chunks = split_text(cleaned_text)
        print(f"Total chunks created: {len(chunks)}")

        # Store chunks
        for chunk in chunks:

            if len(chunk.strip()) < 100:
                continue

            all_chunks.append(chunk)

            all_metadata.append({
                "source": filename
            })

            all_ids.append(str(chunk_id))

            chunk_id += 1


# =========================
# CREATE EMBEDDINGS
# =========================

print("\nCreating Embeddings...")

embeddings = model.encode(
    all_chunks,
    show_progress_bar=True
).tolist()

print("Embeddings created!")


# =========================
# STORE IN CHROMADB
# =========================

print("\nStoring in ChromaDB...")

collection.add(
    documents=all_chunks,
    embeddings=embeddings,
    metadatas=all_metadata,
    ids=all_ids
)

print("\nSUCCESS!")
print(f"Stored {len(all_chunks)} chunks in ChromaDB")