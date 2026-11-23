
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    file_path = Column(String(500), nullable=False)

    status = Column(String(50), default="uploaded")

    uploaded_at = Column(DateTime, default=datetime.now)
