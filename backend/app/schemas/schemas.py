from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class StoryType(str, Enum):
    RAG = "rag"
    FREE_WRITER = "free_writer"

class StoryRequest(BaseModel):
    prompt: str = Field(..., description="Hikaye oluşturma için prompt")
    name: Optional[str] = Field(None, description="Karakter adı")
    age: Optional[int] = Field(None, description="Karakter yaşı")
    gender: Optional[str] = Field(None, description="Karakter cinsiyeti")
    genre: Optional[str] = Field("Genel", description="Hikaye türü")

class StoryResponse(BaseModel):
    id: int
    prompt: str
    content: str
    title: str
    story_type: StoryType
    created_at: datetime
    published_at: Optional[datetime] = None
    author_id: int

    class Config:
        from_attributes = True

# Prompt optimize istek/yanıtı (varsa kullanılır)
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    optimized_prompt: str

class StoryBase(BaseModel):
    title: str
    genre: str
    characters: List[str]
    setting: str
    plot_points: List[str]

class StoryCreate(BaseModel):
    name: str
    age: int
    genre: str
    preferences: str

class Story(StoryBase):
    id: str
    content: str
    created_at: datetime
    updated_at: datetime

class StoryComponentType(str, Enum):
    MAIN_CHARACTER = "main_character"
    ENVIRONMENT = "environment"
    MAIN_CONFLICT = "main_conflict"
    MORAL = "moral"
    PLOT = "plot"
    CHARACTER_GOAL = "character_goal"
    GENRE = "genre"
    FINAL_TYPE = "final_type"

class ComponentResponse(BaseModel):
    id: int
    type: str
    content: str
    is_generated: bool
    confidence_score: Optional[float] = None

class ImportItem(BaseModel):
    category: str = Field(..., description="Category of the story component")
    name: str = Field(..., description="Name/identifier of the component")
    content: str = Field(..., description="Content of the component")