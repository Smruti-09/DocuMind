
from fastapi import FastAPI
from backend.app.routes.documents import router as documents_router
from backend.app.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Document Intelligence Assistant",
    description="A document question-answering application powered by RAG.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(chat_router)


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
