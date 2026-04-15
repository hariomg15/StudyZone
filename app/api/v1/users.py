from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.dependecies import get_db, require_admin
from app.models.user import User
from app.schemas.dashboard import AdminStatsResponse
from app.services import admin_service

router = APIRouter()


@router.get("/admin/stats", response_model=AdminStatsResponse)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    admin_access_code: str | None = Header(default=None, alias="X-Admin-Access-Code"),
):
    return admin_service.get_admin_stats(db, admin_access_code)
