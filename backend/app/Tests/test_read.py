
from backend.app.database.connection import SessionLocal
from backend.app.database.document import Document

db = SessionLocal()

try:
    documents = db.query(Document).all()

    print("Total documents:", len(documents))

    for document in documents:
        print("----------------------")
        print("ID:", document.id)
        print("Filename:", document.filename)
        print("File path:", document.file_path)
        print("Status:", document.status)
        print("Uploaded at:", document.uploaded_at)

finally:
    db.close()
