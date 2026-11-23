import shutil
from pathlib import Path


from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.database.document import Document
from backend.app.services.indexing_service import index_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Directory where uploaded PDFs will be stored
UPLOAD_DIR = PROJECT_ROOT / "documents"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Generate a unique filename
    import uuid
    unique_filename = f"{uuid.uuid4()}_{Path(file.filename).name}"

    file_path = UPLOAD_DIR / unique_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_document = Document(
            filename=Path(file.filename).name,
            file_path=str(file_path),
            status="uploaded"
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        index_result = index_document(
            file_path=str(file_path),
            document_id=new_document.id
        )

        new_document.status = "indexed"
        db.commit()

        return {
            "message": "Document uploaded successfully",
            "document_id": new_document.id,
            "filename": new_document.filename,
            "status": new_document.status,
            "total_chunks": index_result["total_chunks"]
        }

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Document upload failed"
        )

    finally:
        file.file.close()

@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(
        Document.uploaded_at.desc()
    ).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status,
            "uploaded_at": doc.uploaded_at
        }
        for doc in documents
    ]