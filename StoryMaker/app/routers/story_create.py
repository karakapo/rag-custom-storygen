
from fastapi import APIRouter, HTTPException, Depends
import datetime
import time 
from typing import List, Optional

from utils.auth import get_current_user
from schemas.schemas import Story, StoryType, StoryResponse, StoryRequest
from sqlalchemy.orm import Session
from db.database import get_db
from services.story_writer_with_rag import create_story
from services.free_story_writer import write_free_story
from services.title_generator import generate_title


router = APIRouter(
    prefix="/story",
    tags=["storyCreate"]
)


@router.post("create/2", response_model=StoryResponse)
async def story_create_with_rag(prompt: StoryRequest,current_user: dict = Depends(get_current_user) ,session: Session = Depends(get_db)):
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


@router.post("create/1", response_model=StoryResponse)
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