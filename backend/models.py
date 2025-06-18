from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, nullable=False, default=1)  # Default author ID since auth is removed
    status = Column(String(20), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    
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


# Example usage for RAG-based story generation:
"""
from database import db
from models import Story, StoryComponent, StoryComponentType, StoryStatus
import numpy as np

def create_story_with_components(prompt: str):
    with db.get_session() as session:
        # Create story with initial status
        story = Story(
            author_id=1,  # Default author ID
            status="generating",
            original_prompt=prompt
        )
        session.add(story)
        session.commit()

        # Update story with generated content
        story.title = "The Quest for the Holy Grail"
        story.content = "Once upon a time in Camelot..."
        story.status = "published"
        story.published_at = datetime.utcnow()
        story.content_embedding = np.random.rand(1536).tolist()
        story.title_embedding = np.random.rand(1536).tolist()
        
        session.commit()
        return story

# Query examples for RAG:
def find_similar_stories(embedding: list, limit: int = 5):
    with db.get_session() as session:
        # This is a simplified example. In practice, you'd use a vector similarity search
        stories = session.query(Story).filter(
            Story.status == "published"
        ).limit(limit).all()
        return stories
""" 