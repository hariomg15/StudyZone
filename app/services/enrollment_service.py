from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import UserRole


def enroll_in_course(db: Session, course_id: int, current_user):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses."
        )

    course = db.query(Course).filter(Course.id == course_id).first()
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

    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        )
        .first()
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course."
        )

    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


def get_my_enrollments(db: Session, current_user):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view their enrollments."
        )

    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course).joinedload(Course.teacher))
        .filter(Enrollment.user_id == current_user.id)
        .all()
    )

    return enrollments


def get_course_enrollments(db: Session, course_id: int, current_user):
    course = db.query(Course).filter(Course.id == course_id).first()

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

    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.student))
        .filter(Enrollment.course_id == course_id)
        .all()
    )

    return enrollments
