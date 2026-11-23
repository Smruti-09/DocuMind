from pathlib import Path

from backend.app.services.indexing_service import index_document

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "documents"

pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

if not pdf_files:
    print("No PDF found!")
else:
    file_path = pdf_files[0]

    result = index_document(
        file_path=str(file_path),
        document_id=2
    )

    print(result)