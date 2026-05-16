# 📚 RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask questions from PDF documents and get AI-generated answers with contextual retrieval.

# 🚀 Features
📄 PDF text extraction using PyMuPDF
🧹 Text cleaning and preprocessing
✂️ Chunking of documents for better retrieval
🔎 Vector embeddings using Sentence Transformers
🗄️ Vector storage using ChromaDB
🤖 Question answering using NVIDIA LLM API
💬 Simple Streamlit UI for interaction
📚 Source tracking for transparency


PDF Files
   ↓
Text Extraction (PyMuPDF)
   ↓
Cleaning & Preprocessing
   ↓
Chunking (700–800 tokens)
   ↓
Embeddings (SentenceTransformer)
   ↓
Vector Database (ChromaDB)
   ↓
User Query
   ↓
Similarity Search
   ↓
Top Relevant Chunks
   ↓
LLM (NVIDIA API)
   ↓
Final Answer + Sources

# 🛠️ Tech Stack
Python
Streamlit
ChromaDB
PyMuPDF
SentenceTransformers (bge-small-en-v1.5)
NVIDIA LLM API
Regex (text cleaning)

# 📂 Project Structure

RAG_PROJECT/
│
├── data/                 # PDF files
├── chroma_db/           # Vector database (ignored in git)
├── ingest.py            # PDF ingestion & embedding creation
├── rag.py               # CLI-based RAG pipeline
├── app.py               # Streamlit UI
├── requirements.txt     # Dependencies
└── README.md

# ⚙️ Installation

1. Clone repository
git clone https://github.com/Santhu021/rag_chatbot.git
cd rag-chatbot

2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install dependencies
pip install -r requirements.txt

# 🚀 How to Run
Step 1: Add PDFs

Place your PDF files inside:

data/

Step 2: Run ingestion

python ingest.py

This will:

Extract text
Chunk it
Generate embeddings
Store in ChromaDB

Step 3: Run Streamlit app

streamlit run app.py

Step 4: Ask Questions

Example:

What is gradient descent?
Explain CNN
What is reinforcement learning?

# 📊 Key Concepts Used
Retrieval-Augmented Generation (RAG)
Vector similarity search
Embeddings
Chunking strategy
Prompt engineering
Context-aware LLM responses

# 🎯 Future Improvements
Add chat history memory
Improve reranking of retrieved chunks
Add streaming responses
Deploy on cloud (AWS / HuggingFace Spaces)
Add multi-document filtering

# 👨‍💻 Author

Built as part of AI/ML project demonstrating full-stack RAG pipeline implementation.

# 📌 Note
.venv/, chroma_db/, and .env are ignored using .gitignore
API keys are not included for security reasons