
from fastapi import APIRouter, Depends, HTTPException, status

from utils.auth import create_jwt_token, verify_jwt_token, hash_password, verify_password
from schemas.schemas import Login,Register
from db.database import SessionLocal
from utils.auth import get_user_by_username
from db.models import User
from utils.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@router.post("/register")
async def register(user: Register):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )
        hashed_pw = hash_password(user.password)
        db_user = User(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            password=hashed_pw
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"msg": "User registered successfully"}
    finally:
        db.close()
      



@router.post("/login")
async def login(user: Login):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token_data = {"sub": db_user.username}
    token = create_jwt_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}