from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, JSON, Float, ARRAY
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    EDITOR = "editor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    stories = relationship("Story", back_populates="author")

    def __repr__(self):
        return f"<User {self.username}>"

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
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

    # Relationships
    author = relationship("User", back_populates="stories")
    

    def __repr__(self):
        return f"<Story {self.title}>"


# Example usage for RAG-based story generation:
"""
from database import db
from models import Story, StoryComponent, StoryComponentType, StoryStatus
import numpy as np

def create_story_with_components(user_id: int, prompt: str):
    with db.get_session() as session:
        # Create story with initial status
        story = Story(
            author_id=user_id,
            status=StoryStatus.GENERATING,
            original_prompt=prompt
        )
        session.add(story)
        session.commit()

        # Create story components
        components = [
            StoryComponent(
                story_id=story.id,
                component_type=StoryComponentType.MAIN_CHARACTER,
                content="A brave knight named Arthur",
                is_generated=True,
                embedding=np.random.rand(1536).tolist(),  # Example embedding
                confidence_score=0.95
            ),
            StoryComponent(
                story_id=story.id,
                component_type=StoryComponentType.ENVIRONMENT,
                content="Medieval kingdom of Camelot",
                is_generated=True,
                embedding=np.random.rand(1536).tolist(),
                confidence_score=0.92
            ),
            # Add other components...
        ]
        
        session.add_all(components)
        session.commit()

        # Update story with generated content
        story.title = "The Quest for the Holy Grail"
        story.content = "Once upon a time in Camelot..."
        story.status = StoryStatus.PUBLISHED
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
            Story.status == StoryStatus.PUBLISHED
        ).limit(limit).all()
        return stories

def find_similar_components(component_type: StoryComponentType, embedding: list, limit: int = 2):
    with db.get_session() as session:
        # This is a simplified example. In practice, you'd use a vector similarity search
        components = session.query(StoryComponent).filter(
            StoryComponent.component_type == component_type
        ).limit(limit).all()
        return components
""" 