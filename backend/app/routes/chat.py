from fastapi import APIRouter, HTTPException

from backend.app.schemas.chat import ChatRequest
from backend.app.services.rag_service import answer_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/{document_id}/ask")
def ask_question(
    document_id: int,
    request: ChatRequest
):
    try:
        result = answer_question(
            question=request.question,
            document_id=document_id
        )

        return {
            "document_id": document_id,
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )