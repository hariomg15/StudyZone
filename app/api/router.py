from fastapi import APIRouter
from app.api.v1 import auth, users, courses, enrollements, questions

api_router=APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(enrollements.router, prefix="/enrollements", tags=["enrollements"])
# api_router.include_router(questions.router, prefix="/questions", tags=["questions"])


#ssare routes import ho gye 