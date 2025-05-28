from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import time

# Local imports
from database import db
from models import Story, User, UserRole
from services.story_writer_with_rag import create_story
from rag.vectorstore import save_to_qdrant, client
from schemas.schemas import (
    StoryRequest, 
    StoryResponse,
    HealthResponse
)

load_dotenv()
app = FastAPI()

# Dependency
def get_db():
    with db.get_session() as session:
        yield session

@app.post("/story/create", response_model=StoryResponse)
async def story_create_endpoint(prompt: StoryRequest, session: Session = Depends(get_db)):
    start_time = time.time()
    story = None  # Initialize story variable outside try block
    try:
        # Kullanıcı kontrolü
        user = session.query(User).filter(User.id == prompt.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        # Create initial story record
        story = Story(
            author_id=prompt.user_id,
            status="generating",
            original_prompt=prompt.prompt,
            generation_model="gemini-2.0-flash",
            generation_parameters={
                "temperature": 0.85,
                "model": "gemini-2.0-flash"
            }
        )
        session.add(story)
        session.commit()

        # Generate story content using RAG
        story_content = await create_story(prompt)
        
        # Debug logging
        print("Story content received:", story_content)
        
        # Clean and update story with generated content
        content = story_content["content"].strip()
        # Generate a default title from the first few words of the content
        default_title = content.split('\n')[0][:50] + "..." if len(content) > 50 else content
        
        story.title = default_title
        story.content = content
        story.status = "published"
        story.published_at = datetime.utcnow()
        story.generation_time = time.time() - start_time
        session.commit()

        return StoryResponse(
            id=story.id,
            prompt=prompt.prompt,
            content=story.content,
            title=story.title,
            user_id=story.author_id,
            created_at=story.created_at,
            published_at=story.published_at
        )

    except Exception as e:
        session.rollback()
        if story:
            story.status = "failed"
            story.generation_time = time.time() - start_time
            session.commit()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/story/{story_id}")
async def delete_story(story_id: int, session: Session = Depends(get_db)):
    try:
        story = session.query(Story).filter(Story.id == story_id).first()
        if not story:
            raise HTTPException(status_code=404, detail="Hikaye bulunamadı")

        session.delete(story)
        session.commit()
        return {"message": "Hikaye başarıyla silindi"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/story/{story_id}", response_model=StoryResponse)
async def get_story(story_id: int, session: Session = Depends(get_db)):
    story = session.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Hikaye bulunamadı")

    return StoryResponse(
        id=story.id,
        prompt=story.original_prompt,
        content=story.content,
        title=story.title,
        user_id=story.author_id,
        created_at=story.created_at,
        published_at=story.published_at
    )

@app.get("/user/{user_id}/stories", response_model=List[StoryResponse])
async def get_user_stories(user_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    stories = session.query(Story).filter(Story.author_id == user_id).all()
    return [
        StoryResponse(
            id=story.id,
            prompt=story.original_prompt,
            content=story.content,
            title=story.title,
            user_id=story.author_id,
            created_at=story.created_at,
            published_at=story.published_at
        )
        for story in stories
    ]

@app.get("/health", response_model=HealthResponse)
async def health_check(session: Session = Depends(get_db)):
    try:
        session.execute("SELECT 1")
        
        return HealthResponse(
            status="healthy",
            services={
                "postgresql": "connected"
            },
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Servis sağlıksız: {str(e)}")

