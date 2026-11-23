# DocuMind – Document Intelligence Assistant

An AI-powered document question-answering system built using Retrieval-Augmented Generation (RAG). Upload PDF documents and ask natural-language questions to receive context-aware answers with source references.

## Features

- PDF document upload and text extraction
- Text chunking and semantic embedding generation
- Vector storage using ChromaDB
- Semantic search with document-specific retrieval
- Context-grounded answers using an LLM through OpenRouter
- Source chunk references for answer transparency
- Multiple document support
- React-based interactive chat interface
- PostgreSQL database for document metadata

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| Vector Database | ChromaDB |
| Embedding Model | Sentence Transformers – all-MiniLM-L6-v2 |
| PDF Processing | PyPDF |
| LLM Integration | OpenRouter, OpenAI-compatible SDK |

## Architecture

1. User uploads a PDF through the React frontend.
2. FastAPI receives and stores the document.
3. PyPDF extracts its text.
4. The text is divided into overlapping chunks.
5. Sentence Transformers generates embeddings.
6. ChromaDB stores the chunks and their embeddings.
7. The user's question is converted into an embedding.
8. Relevant chunks are retrieved using semantic similarity and document ID filtering.
9. The retrieved context is sent to the LLM.
10. The generated answer and source chunks are returned to the frontend.

## Project Structure

```text
Document Analysis/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── retrieval/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── Tests/
│   └── create_tables.py
├── frontend/
│   └── src/
├── documents/
├── evaluation/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Document Analysis"
```

### 2. Set up the Python environment

```bash
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your PostgreSQL connection URL and OpenRouter API key.

### 4. Create the PostgreSQL database

Create a database named:

```text
document_intelligence
```

### 5. Initialize database tables

```bash
python -m backend.create_tables
```

### 6. Start the backend

From the project root:

```bash
python -m uvicorn backend.app.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### 7. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

http://localhost:5173

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend welcome |
| GET | `/health` | Health check |
| POST | `/documents/upload` | Upload and index a PDF |
| GET | `/documents/` | Retrieve uploaded documents |
| POST | `/chat/{document_id}/ask` | Ask questions about a document |

## Evaluation

The MVP was manually tested for:

- PDF upload and indexing
- Semantic retrieval
- Multi-chunk question answering
- Source-grounded responses
- Missing-information handling
- Document-specific retrieval

## Current Limitations

- Supports text-based PDFs; scanned PDFs requiring OCR are not supported.
- Uses basic character-based chunking.
- Retrieval uses semantic similarity without reranking.
- Document indexing is synchronous.
- Authentication and multi-user access control are not implemented.

## Future Improvements

- OCR support for scanned documents
- Hybrid search and reranking
- Automated RAG evaluation
- Improved chunking strategies
- User authentication and document management
- Asynchronous document processing

---

**DocuMind** – Making document understanding more intelligent through Retrieval-Augmented Generation.
