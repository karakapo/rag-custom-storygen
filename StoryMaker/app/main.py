from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import story, story_create,auth
from core import config



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(story.router)
app.include_router(story_create.router)
app.include_router(auth.router)
