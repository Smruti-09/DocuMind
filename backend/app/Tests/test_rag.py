from backend.app.services.rag_service import answer_question

question = "How does TATTVA detect and track extreme weather events?"

result = answer_question(
    question=question,
    document_id=2
)

print("\nQUESTION:")
print(question)

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nSOURCE CHUNKS:")

for source in result["sources"]:
    print("\nChunk:", source["chunk_index"])
    print(source["content"])