from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import VECTOR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/docker_assistant")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)  # e.g., filename
    embedding = Column(Vector(768))  # Assuming 768 dimensions for nomic-embed-text

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()