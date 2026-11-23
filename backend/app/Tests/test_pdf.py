from pathlib import Path

from backend.app.services.pdf_processor import extract_text_from_pdf

# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Locate the documents folder
DOCUMENTS_DIR = PROJECT_ROOT / "documents"

# Find the first PDF automatically
pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

if not pdf_files:
    print("No PDF files found!")
else:
    file_path = pdf_files[0]

    print("Reading:", file_path.name)

    text = extract_text_from_pdf(str(file_path))

    print("\nExtracted text:")
    print(text[:2000])

    print("\nTotal characters:", len(text))