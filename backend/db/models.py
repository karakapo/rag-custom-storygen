from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float, ARRAY, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class StoryType(enum.Enum):
    RAG = "rag"
    FREE_WRITER = "free_writer"

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    status = Column(String(20), default="draft")
    story_type = Column(Enum(StoryType), nullable=False, default=StoryType.RAG)  # New field to distinguish story types
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    author_id = Column(Integer, nullable=False, default=1)  # Her hikaye için 1 nolu yazar
    
    # Story generation metadata
    original_prompt = Column(Text, nullable=True)
    generation_model = Column(String(50), nullable=True)  # e.g., "gemini-2.0-flash"
    generation_parameters = Column(JSON, nullable=True)  # Store generation parameters
    generation_time = Column(Float, nullable=True)  # Time taken to generate in seconds
    
    # Vector embeddings for semantic search
    content_embedding = Column(ARRAY(Float), nullable=True)  # Vector embedding of the story content
    title_embedding = Column(ARRAY(Float), nullable=True)    # Vector embedding of the title

    def __repr__(self):
        return f"<Story {self.title}>"


