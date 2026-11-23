from backend.app.services.pdf_processor import extract_text_from_pdf
from backend.app.services.chunking import split_text_into_chunks
from backend.app.services.embedding import generate_embeddings
from backend.app.retrieval.vector_store import store_chunks


def index_document(file_path: str, document_id: int):

    # 1. Extract text
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise ValueError("No readable text found in PDF")

    # 2. Split text into chunks
    chunks = split_text_into_chunks(text)

    # 3. Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 4. Store in ChromaDB
    total_chunks = store_chunks(
        chunks,
        embeddings,
        document_id
    )

    return {
        "document_id": document_id,
        "total_chunks": total_chunks,
        "status": "indexed"
    }