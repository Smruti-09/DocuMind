from backend.app.database.connection import engine
from backend.app.database.base import Base

# Import models so SQLAlchemy knows about them
from backend.app.database.document import Document

# Create all registered tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")