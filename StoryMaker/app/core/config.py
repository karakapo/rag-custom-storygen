from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
   API_PREFIX: str = "/api"
   
   DEBUG: bool = False 

   DATABASE_URL: str = "sqlite:///./test.db"

   QDRANT_URL:  str = os.getenv("QDRANT_URL")
   QDRANT_KEY: str = os.getenv("QDRANT_KEY")

   ALLOWED_ORIGINS: str = ""

   GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

   JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
   ALGORITHM: str = os.getenv("ALGORITHM")
   ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)




   @field_validator("ALLOWED_ORIGINS")
   def parse_allowed_origins(cls, v: str) -> List[str]:
      return v.split(",") if v else []

   class Config:
      env_file = ".env"
      env_file_encoding = "utf-8"
      case_sensitive = True


settings = Settings()