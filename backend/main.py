from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import time

from db.database import db
from db.models import Story, StoryType
from services.story_writer_with_rag import create_story
from services.free_story_writer import write_free_story
from rag.vectorstore import save_to_qdrant, client
from schemas.schemas import StoryRequest,StoryResponse,StoryType as StoryTypeSchema
from services.title_generator import generate_title

load_dotenv()

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse buraya frontend domainini ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    with db.get_session() as session:
        yield session


@app.post("/story/create/2", response_model=StoryResponse)
async def story_create_with_rag(prompt: StoryRequest, session: Session = Depends(get_db)):
    start_time = time.time()
    story = None  # Hikaye değişkenini try bloğu dışında başlat
    try:
        # Başlangıç hikaye kaydını oluştur
        story = Story(
            status="generating",
            story_type=StoryType.RAG,
             author_id=1,
            original_prompt=prompt.prompt,
            generation_model="gemini-2.0-flash",
            generation_parameters={
                "temperature": 0.85,
                "model": "gemini-2.0-flash"
            }
        )
        session.add(story)
        session.commit()

       
        story_content = await create_story(prompt)
        
        
        
        content = story_content["content"].strip()
        
        default_title = generate_title(prompt)
        
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
            story_type=StoryTypeSchema.RAG,
            created_at=story.created_at,
            published_at=story.published_at,
            author_id=story.author_id
        )

    except Exception as e:
        session.rollback()
        if story:
            story.status = "failed"
            story.generation_time = time.time() - start_time
            session.commit()
        raise HTTPException(status_code=500, detail=f"Hikaye oluşturulurken hata oluştu: {str(e)}")


@app.post("/story/create/1", response_model=StoryResponse)
async def free_story_create(prompt: StoryRequest, session: Session = Depends(get_db)):
    start_time = time.time()
    story = None
    try:
        # Free story writer kullanarak hikaye içeriğini oluştur
        story_result = write_free_story(
            user_prompt=prompt.prompt,
            name=prompt.name,
            age=prompt.age,
            gender=prompt.gender,
            genre=prompt.genre
        )
        
        # Hata ayıklama günlüğü
        print("Free hikaye içeriği alındı:", story_result)
        
        # İçeriği temizle
        content = story_result["story"].strip()
        # İçeriğin ilk birkaç kelimesinden varsayılan başlık oluştur
        default_title = generate_title(prompt)
        
        # Hikayeyi veritabanına kaydet
        story = Story(
            status="published",
            story_type=StoryType.FREE_WRITER,
            title=default_title,
            content=content,
            author_id=1,
            original_prompt=prompt.prompt,
            generation_model="free_writer",
            generation_parameters={
                "name": prompt.name,
                "age": prompt.age,
                "gender": prompt.gender,
                "genre": prompt.genre
            },
            published_at=datetime.utcnow(),
            generation_time=time.time() - start_time
        )
        session.add(story)
        session.commit()
        
        return StoryResponse(
            id=story.id,
            prompt=prompt.prompt,
            content=content,
            title=default_title,
            story_type=StoryTypeSchema.FREE_WRITER,
            created_at=story.created_at,
            published_at=story.published_at,
            author_id=story.author_id
        )

    except Exception as e:
        session.rollback()
        if story:
            story.status = "failed"
            story.generation_time = time.time() - start_time
            session.commit()
        raise HTTPException(status_code=500, detail=f"Free hikaye oluşturulurken hata oluştu: {str(e)}")


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
        story_type=StoryTypeSchema(story.story_type.value),
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
            story_type=StoryTypeSchema(story.story_type.value),
            created_at=story.created_at,
            published_at=story.published_at,
            author_id=story.author_id
        )
        for story in stories
    ]

@app.get("/stories/rag", response_model=List[StoryResponse])
async def get_rag_stories(session: Session = Depends(get_db)):
    """Get all RAG stories"""
    stories = session.query(Story).filter(
        Story.status == "published",
        Story.story_type == StoryType.RAG
    ).order_by(Story.created_at.desc()).all()
    
    return [
        StoryResponse(
            id=story.id,
            prompt=story.original_prompt,
            content=story.content,
            title=story.title,
            story_type=StoryTypeSchema.RAG,
            created_at=story.created_at,
            published_at=story.published_at
        )
        for story in stories
    ]

@app.get("/stories/free-writer", response_model=List[StoryResponse])
async def get_free_writer_stories(session: Session = Depends(get_db)):
    """Get all Free Writer stories"""
    stories = session.query(Story).filter(
        Story.status == "published",
        Story.story_type == StoryType.FREE_WRITER
    ).order_by(Story.created_at.desc()).all()
    
    return [
        StoryResponse(
            id=story.id,
            prompt=story.original_prompt,
            content=story.content,
            title=story.title,
            story_type=StoryTypeSchema.FREE_WRITER,
            created_at=story.created_at,
            published_at=story.published_at
        )
        for story in stories
    ]


