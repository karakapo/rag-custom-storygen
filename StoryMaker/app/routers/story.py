
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schemas.schemas import Story, StoryType, StoryResponse, StoryRequest
from sqlalchemy.orm import Session
from db.database import get_db



router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)







@router.delete("/{story_id}")
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

@router.get("/{story_id}", response_model=StoryResponse)
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

@router.get("/stories", response_model=List[StoryResponse])
async def get_all_stories(session: Session = Depends(get_db)):
    stories = session.query(Story).filter(Story.status == "published").all()
    return [
        StoryResponse(
            id=story.id,
            prompt=story.original_prompt,
            content=story.content,
            title=story.title,
            created_at=story.created_at,
            published_at=story.published_at,
            author_id=story.author_id
        )
        for story in stories
    ]

@router.get("/rag", response_model=List[StoryResponse])
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
            created_at=story.created_at,
            published_at=story.published_at
        )
        for story in stories
    ]

@router.get("/free-writer", response_model=List[StoryResponse])
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
            created_at=story.created_at,
            published_at=story.published_at
        )
        for story in stories
    ]

