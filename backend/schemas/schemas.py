from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    EDITOR = "editor"

class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StoryRequest(BaseModel):
    prompt: str = Field(..., description="Hikaye oluşturma için prompt")
    user_id: int = Field(..., description="Hikayeyi oluşturan kullanıcının ID'si")

class StoryResponse(BaseModel):
    id: int
    prompt: str
    content: str
    title: str
    user_id: int
    created_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    services: dict
    timestamp: datetime

# Kullanıcı giriş isteği için ayrı model
# class UserLoginRequest(BaseModel):
#     username: str
#     password: str

# Kullanıcı yanıtı
# class UserResponse(BaseModel):
#     message: str
#     data: Optional[dict] = None
#     error: Optional[str] = None

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

# Çakışan StoryResponse tanımı kaldırıldı. Eğer farklı bir amaç içinse yeniden adlandırılabilir.
# class StoryResponse(BaseModel):
#     optimized_prompt: str
#     story: str

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