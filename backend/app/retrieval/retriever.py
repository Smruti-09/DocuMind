from backend.app.services.embedding import generate_embeddings
from backend.app.retrieval.vector_store import collection


def retrieve_relevant_chunks(
    question: str,
    document_id: int,
    top_k: int = 6
):
    # Convert the user's question into an embedding
    question_embedding = generate_embeddings([question])

    # Search ChromaDB for similar chunks
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k,
        where={"document_id": document_id},
        include=["documents", "metadatas", "distances"]
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks