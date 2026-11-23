from backend.app.retrieval.retriever import retrieve_relevant_chunks

question = "What are the core innovations of TATTVA?"

results = retrieve_relevant_chunks(
    question=question,
    document_id=2,
    top_k=10
)

print(f"\nTotal retrieved chunks: {len(results)}")

for i, item in enumerate(results, start=1):
    print("\n" + "=" * 60)
    print(f"RESULT {i}")
    print(f"Chunk index: {item['metadata']['chunk_index']}")
    print(f"Distance: {item['distance']}")
    print(item["text"][:500])