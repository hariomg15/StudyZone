from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependecies import get_db, get_current_user_optional, require_teacher
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.schemas.content import (
    SectionCreate,
    SectionResponse,
    LectureCreate,
    LectureResponse,
    NoteCreate,
    NoteResponse,
    CourseContentResponse,
)
from app.services import course_service

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.create_course(db, course_data, current_user)


@router.get("/", response_model=list[CourseResponse])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    return course_service.list_courses(db, current_user, skip=skip, limit=limit)



@router.get("/search", response_model=list[CourseResponse])
def search_courses(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return course_service.search_courses(db, q, skip=skip, limit=limit)


@router.get("/my/created", response_model=list[CourseResponse])
def get_my_created_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.get_my_created_courses(db, current_user)


@router.patch("/{course_id}/publish", response_model=CourseResponse)
def publish_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.publish_course(db, course_id, current_user)


@router.patch("/{course_id}/unpublish", response_model=CourseResponse)
def unpublish_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.unpublish_course(db, course_id, current_user)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    return course_service.get_course(db, course_id, current_user)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.update_course(db, course_id, course_data, current_user)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    course_service.delete_course(db, course_id, current_user)
    return None


@router.post("/{course_id}/sections", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(
    course_id: int,
    section_data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.create_section(db, course_id, section_data, current_user)


@router.post("/sections/{section_id}/lectures", response_model=LectureResponse, status_code=status.HTTP_200_OK)
def add_lecture(
    section_id: int,
    lecture_data: LectureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.add_lecture(db, section_id, lecture_data, current_user)


@router.post("/sections/{section_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def add_note(
    section_id: int,
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    return course_service.add_note(db, section_id, note_data, current_user)


@router.get("/{course_id}/content", response_model=CourseContentResponse, status_code=status.HTTP_200_OK)
def get_course_content(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    return course_service.get_course_content(db, course_id, current_user)
