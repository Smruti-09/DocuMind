from backend.app.retrieval.retriever import retrieve_relevant_chunks
from backend.app.services.llm_service import generate_answer


def answer_question(question: str, document_id: int):

    # Retrieve relevant document chunks
    retrieved_chunks = retrieve_relevant_chunks(
        question=question,
        document_id=document_id,
        top_k=10
    )

    if not retrieved_chunks:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }

    # Combine retrieved chunks into context
    context = "\n\n".join(
        item["text"] for item in retrieved_chunks
    )

    # Generate answer using OpenRouter
    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "answer": answer,
        "sources": [
            {
                "chunk_index": item["metadata"]["chunk_index"],
                "content": item["text"]
            }
            for item in retrieved_chunks
        ]
    }