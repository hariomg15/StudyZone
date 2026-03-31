from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.dependecies import get_db, require_admin
from app.models.course import Course
from app.models.user import User
from app.models.enrollment import Enrollment
from app.schemas.dashboard import AdminStatsResponse

router = APIRouter()
@router.get("/admin/stats", response_model=AdminStatsResponse)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    admin_access_code: str | None = Header(default=None, alias="X-Admin-Access-Code"),
):
    if admin_access_code != settings.teacher_signup_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin access code",
        )

    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == "student").count()
    total_teachers = db.query(User).filter(User.role == "teacher").count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    total_courses = db.query(Course).count()
    total_published_courses = db.query(Course).filter(Course.is_published == True).count()
    total_enrollments = db.query(Enrollment).count()

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_admins": total_admins,
        "total_courses": total_courses,
        "total_published_courses": total_published_courses,
        "total_enrollments": total_enrollments
    }
