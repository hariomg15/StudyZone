from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
import app.models

# Base.metadata.create_all(bind=engine)  


app=FastAPI(title=settings.app_name, version=settings.api_v1_str,
            description="Industry grade Caoching Platform API built with FastAPI")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def prince_jaiswal():
    return {"message": "Welcome to the StudyZone API!"}