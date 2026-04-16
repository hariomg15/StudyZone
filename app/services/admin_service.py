from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories import admin_repository


def get_admin_stats(db: Session, admin_access_code: str | None):
    if admin_access_code != settings.teacher_signup_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin access code"
        )

    return admin_repository.get_admin_stats_counts(db)
