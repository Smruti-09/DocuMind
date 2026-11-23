
from backend.app.database.connection import SessionLocal
from backend.app.database.document import Document

# Create a database session
db = SessionLocal()

try:
    # Create a document record
    new_document = Document(
        filename="machine_learning.pdf",
        file_path="documents/machine_learning.pdf",
        status="uploaded"
    )

    # Add the record
    db.add(new_document)

    # Save changes to PostgreSQL
    db.commit()

    # Refresh to get database-generated values
    db.refresh(new_document)

    print("Document inserted successfully!")
    print("Document ID:", new_document.id)
    print("Filename:", new_document.filename)
    print("Status:", new_document.status)

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()
