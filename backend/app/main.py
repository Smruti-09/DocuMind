
from fastapi import FastAPI

app = FastAPI(
    title="Document Intelligence Assistant",
    description="A document question-answering application powered by RAG.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Document Intelligence Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
