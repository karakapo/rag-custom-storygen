from fastapi import FastAPI, HTTPException, Depends, Request, status
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import time
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from jose import JWTError, jwt
from passlib.context import CryptContext

# Local imports
from database import db
from models import Story, User, UserRole
from services.story_writer_with_rag import create_story
from rag.vectorstore import save_to_qdrant, client
from schemas.schemas import (
    StoryRequest, 
    StoryResponse,
    HealthResponse,
    UserCreate,
    UserResponse,
    Token,
    UserLogin
)
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
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
async def story_create_endpoint(prompt: StoryRequest, session: Session = Depends(get_db)):
    start_time = time.time()
    story = None  # Hikaye değişkenini try bloğu dışında başlat
    try:
        # Kullanıcı kontrolü
        user = session.query(User).filter(User.id == prompt.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        # Başlangıç hikaye kaydını oluştur
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
                "postgresql": "bağlı"
            },
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Servis sağlıksız: {str(e)}")

@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, session: Session = Depends(get_db)):
    # Email kontrolü
    db_user = session.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Bu email adresi zaten kayıtlı"
        )
    
    # Kullanıcı adı kontrolü
    db_user = session.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Bu kullanıcı adı zaten alınmış"
        )
    
    # Yeni kullanıcı oluştur
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=UserRole.USER
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        role=db_user.role.value,
        created_at=db_user.created_at
    )

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin, session: Session = Depends(get_db)):
    # Email ile kullanıcıyı bul
    user = session.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Erişim tokeni oluştur
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role.value,
        created_at=current_user.created_at
    )

