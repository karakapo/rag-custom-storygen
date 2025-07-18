
from fastapi import APIRouter, Depends, HTTPException, status


from utils.auth import create_jwt_token, verify_jwt_token 
from schemas.schemas import Login


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "$2b$12$KIX/8Z8Q8Z8Q8Z8Q8Z8Q8u"
    }
}


@router.post("/login")
async def login(user: Login):
    db_user = fake_users_db.get(user.username)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token_data = {"sub": user.username}
    token = create_jwt_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}