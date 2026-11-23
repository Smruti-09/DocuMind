from pathlib import Path

from backend.app.services.pdf_processor import extract_text_from_pdf
from backend.app.services.chunking import split_text_into_chunks

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "documents"

pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

if not pdf_files:
    print("No PDF found!")
else:
    text = extract_text_from_pdf(str(pdf_files[0]))

    chunks = split_text_into_chunks(text)

    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- CHUNK {index} ---")
        print(chunk)