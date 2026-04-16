from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment


def get_enrollment_by_user_and_course(db: Session, user_id: int, course_id: int):
    return (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )
        .first()
    )


def create_enrollment(db: Session, user_id: int, course_id: int):
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def get_my_enrollments(db: Session, user_id: int):
    return (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course).joinedload(Course.teacher))
        .filter(Enrollment.user_id == user_id)
        .all()
    )


def get_course_enrollments(db: Session, course_id: int):
    return (
        db.query(Enrollment)
        .options(joinedload(Enrollment.student))
        .filter(Enrollment.course_id == course_id)
        .all()
    )
