from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


def get_admin_stats_counts(db: Session):
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == "student").count()
    total_teachers = db.query(User).filter(User.role == "teacher").count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    total_courses = db.query(Course).count()
    total_published_courses = (
        db.query(Course)
        .filter(Course.is_published == True)
        .count()
    )
    total_enrollments = db.query(Enrollment).count()

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_admins": total_admins,
        "total_courses": total_courses,
        "total_published_courses": total_published_courses,
        "total_enrollments": total_enrollments,
    }
