from fastapi import FastAPI, HTTPException, Depends, Request, status
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Local imports
from database import db
from models import Story
from services.story_writer_with_rag import create_story
from rag.vectorstore import save_to_qdrant, client
from schemas.schemas import (
    StoryRequest, 
    StoryResponse,
    HealthResponse
)

load_dotenv()
app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:3000"],  # Frontend'in çalışacağı adresler
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    with db.get_session() as session:
        yield session


@app.post("/story/create", response_model=StoryResponse)
async def story_create_with_rag(prompt: StoryRequest, session: Session = Depends(get_db)):
    start_time = time.time()
    story = None  # Hikaye değişkenini try bloğu dışında başlat
    try:
        # Başlangıç hikaye kaydını oluştur
        story = Story(
            author_id=1,  # Default user ID since auth is removed
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

        # RAG kullanarak hikaye içeriğini oluştur
        story_content = await create_story(prompt)
        
        # Hata ayıklama günlüğü
        print("Hikaye içeriği alındı:", story_content)
        
        # İçeriği temizle ve hikayeyi güncelle
        content = story_content["content"].strip()
        # İçeriğin ilk birkaç kelimesinden varsayılan başlık oluştur
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
            created_at=story.created_at,
            published_at=story.published_at
        )

    except Exception as e:
        session.rollback()
        if story:
            story.status = "failed"
            story.generation_time = time.time() - start_time
            session.commit()
        raise HTTPException(status_code=500, detail=f"Hikaye oluşturulurken hata oluştu: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Hikaye silinirken hata oluştu: {str(e)}")

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
        created_at=story.created_at,
        published_at=story.published_at
    )

@app.get("/stories", response_model=List[StoryResponse])
async def get_all_stories(session: Session = Depends(get_db)):
    stories = session.query(Story).filter(Story.status == "published").all()
    return [
        StoryResponse(
            id=story.id,
            prompt=story.original_prompt,
            content=story.content,
            title=story.title,
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
                "postgresql": "bağlı"
            },
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Servis sağlıksız: {str(e)}")

