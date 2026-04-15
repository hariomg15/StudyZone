from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependecies import get_db, get_current_user, require_teacher
from app.models.user import User
from app.schemas.enrollment import (
    EnrollmentResponse,
    MyEnrollmentCourseResponse,
    CourseStudentEnrollmentResponse,
)
from app.services import enrollment_service

router = APIRouter()


@router.post("/{course_id}", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return enrollment_service.enroll_in_course(db, course_id, current_user)


@router.get("/my", response_model=list[MyEnrollmentCourseResponse])
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return enrollment_service.get_my_enrollments(db, current_user)


@router.get("/course/{course_id}", response_model=list[CourseStudentEnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return enrollment_service.get_course_enrollments(db, course_id, current_user)
