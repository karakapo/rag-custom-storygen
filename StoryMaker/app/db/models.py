from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float, ARRAY, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import enum
from db.database import Base



class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    story_type = Column(String(10), nullable=False, default="rag")  # Rag or freestyle
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, nullable=False, default=1)  # Her hikaye için 1 nolu yazar
    
    # Story generation metadata
    original_prompt = Column(Text, nullable=True)
    generation_time = Column(Float, nullable=True)  # Time taken to generate in seconds
    
    

    def __repr__(self):
        return f"<Story {self.title}>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"

