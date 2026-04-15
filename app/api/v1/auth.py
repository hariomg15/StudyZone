from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependecies import get_db, get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user_data)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return auth_service.get_current_user_profile(current_user)
