from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.repositories import course_repository, enrollment_repository


def enroll_in_course(db: Session, course_id: int, current_user):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses."
        )

    course = course_repository.get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot enroll in an unpublished course"
        )

    if not course.is_free:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not free course. Please complete payment to access it."
        )

    existing_enrollment = enrollment_repository.get_enrollment_by_user_and_course(
        db,
        current_user.id,
        course_id,
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course."
        )

    return enrollment_repository.create_enrollment(db, current_user.id, course_id)


def get_my_enrollments(db: Session, current_user):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view their enrollments."
        )

    return enrollment_repository.get_my_enrollments(db, current_user.id)


def get_course_enrollments(db: Session, course_id: int, current_user):
    course = course_repository.get_course_by_id(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if current_user.role != UserRole.admin and course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view enrollments for this course."
        )

    return enrollment_repository.get_course_enrollments(db, course_id)
