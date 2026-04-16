from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import UserRole
from app.repositories import course_repository, enrollment_repository


def create_course(db: Session, course_data, current_user):
    if course_data.is_free:
        course_data.price = 0.0

    if not course_data.is_free and course_data.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0 for paid courses",
        )

    created_course = course_repository.create_course(
        db,
        title=course_data.title,
        description=course_data.description,
        price=course_data.price,
        is_free=course_data.is_free,
        thumbnail=course_data.thumbnail,
        is_published=course_data.is_published,
        teacher_id=current_user.id,
    )

    return course_repository.get_course_with_teacher(db, created_course.id)


def list_courses(db: Session, current_user=None, skip: int = 0, limit: int = 10):
    if current_user and current_user.role in [UserRole.teacher, UserRole.admin]:
        return course_repository.list_all_courses_with_teacher(db, skip=skip, limit=limit)
    return course_repository.list_published_courses_with_teacher(db, skip=skip, limit=limit)

def search_courses(db: Session, q: str, skip: int = 0, limit: int = 10):
    return course_repository.search_published_courses(db, q, skip=skip, limit=limit)


def get_my_created_courses(db: Session, current_user):
    return course_repository.get_courses_by_teacher(db, current_user.id)


def publish_course(db: Session, course_id: int, current_user):
    course = course_repository.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to publish this course",
        )

    course.is_published = True
    course_repository.save_course(db, course)
    return course_repository.get_course_with_teacher(db, course_id)


def unpublish_course(db: Session, course_id: int, current_user):
    course = course_repository.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to unpublish this course",
        )

    course.is_published = False
    course_repository.save_course(db, course)
    return course_repository.get_course_with_teacher(db, course_id)


def get_course(db: Session, course_id: int, current_user=None):
    course = course_repository.get_course_with_teacher(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if not course.is_published:
        is_owner = current_user and (
            current_user.role == UserRole.admin or course.teacher_id == current_user.id
        )
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Course is not published",
            )

    return course


def update_course(db: Session, course_id: int, course_data, current_user):
    course = course_repository.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if current_user.role != UserRole.admin and course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this course",
        )

    update_data = course_data.model_dump(exclude_unset=True)

    if "is_free" in update_data and update_data["is_free"] is True:
        update_data["price"] = 0.0

    if "price" in update_data and update_data["price"] is not None and update_data["price"] < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than or equal to 0",
        )

    for field, value in update_data.items():
        setattr(course, field, value)

    course_repository.save_course(db, course)
    return course_repository.get_course_with_teacher(db, course_id)


def delete_course(db: Session, course_id: int, current_user):
    course = course_repository.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this course",
        )

    course_repository.delete_course(db, course)

    return "deleted"


def create_section(db: Session, course_id: int, section_data, current_user):
    course = course_repository.get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if current_user.role != UserRole.admin and course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add section to this course",
        )

    return course_repository.create_section(
        db,
        course_id=course_id,
        title=section_data.title,
        order_num=section_data.order_num,
    )


def add_lecture(db: Session, section_id: int, lecture_data, current_user):
    section = course_repository.get_section_by_id(db, section_id)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found",
        )

    if current_user.role != UserRole.admin and section.course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add lecture to this section",
        )

    return course_repository.create_lecture(
        db,
        section_id=section_id,
        title=lecture_data.title,
        video_url=lecture_data.video_url,
        duration=lecture_data.duration,
        is_preview=lecture_data.is_preview,
        order_num=lecture_data.order_num,
    )


def add_note(db: Session, section_id: int, note_data, current_user):
    section = course_repository.get_section_by_id(db, section_id)
    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found",
        )

    if current_user.role != UserRole.admin and section.course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add note to this section",
        )

    return course_repository.create_note(
        db,
        section_id=section_id,
        title=note_data.title,
        pdf_url=note_data.pdf_url,
    )


def get_course_content(db: Session, course_id: int, current_user=None):
    course = course_repository.get_course_with_content(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if not course.is_published:
        is_owner = current_user and (
            current_user.role == UserRole.admin or course.teacher_id == current_user.id
        )
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Course is not published",
            )

    if course.is_free:
        return course

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not free course. Please complete payment to access it.",
        )

    if current_user.role in [UserRole.teacher, UserRole.admin]:
        if current_user.role == UserRole.teacher and course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this course content",
            )
        return course

    enrollment = enrollment_repository.get_enrollment_by_user_and_course(
        db,
        current_user.id,
        course_id,
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not free course. Please complete payment to access it.",
        )

    return course
