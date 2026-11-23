import chromadb

# Persistent ChromaDB storage
client = chromadb.PersistentClient(
    path="chroma_db"
)

# Create or access collection
collection = client.get_or_create_collection(
    name="document_chunks"
)


def store_chunks(chunks, embeddings, document_id):

    ids = [
        f"doc_{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(chunks)