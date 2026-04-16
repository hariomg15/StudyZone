from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.course import Course, Section, Lecture, Note


def create_course(db: Session, **course_data):
    course = Course(**course_data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_course_with_teacher(db: Session, course_id: int):
    return (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )


def list_all_courses_with_teacher(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .offset(skip)
        .limit(limit)
        .all()
    )



def list_published_courses_with_teacher(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.is_published == True)
        .offset(skip)
        .limit(limit)
        .all()
    )



def search_published_courses(db: Session, q: str, skip: int = 0, limit: int = 10):
    return (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(
            Course.is_published == True,
            Course.title.ilike(f"%{q}%")
        )
        .offset(skip)
        .limit(limit)
        .all()
    )



def get_courses_by_teacher(db: Session, teacher_id: int):
    return (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.teacher_id == teacher_id)
        .all()
    )


def save_course(db: Session, course):
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course):
    db.delete(course)
    db.commit()


def create_section(db: Session, *, course_id: int, title: str, order_num: int):
    section = Section(
        course_id=course_id,
        title=title,
        order_num=order_num,
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def get_section_by_id(db: Session, section_id: int):
    return db.query(Section).filter(Section.id == section_id).first()


def create_lecture(db: Session, *, section_id: int, title: str, video_url: str, duration: int | None, is_preview: bool, order_num: int):
    lecture = Lecture(
        title=title,
        video_url=video_url,
        duration=duration,
        is_preview=is_preview,
        order_num=order_num,
        section_id=section_id,
    )
    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return lecture


def create_note(db: Session, *, section_id: int, title: str, pdf_url: str):
    note = Note(
        title=title,
        pdf_url=pdf_url,
        section_id=section_id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_course_with_content(db: Session, course_id: int):
    return (
        db.query(Course)
        .options(
            selectinload(Course.sections).selectinload(Section.lectures),
            selectinload(Course.sections).selectinload(Section.notes),
        )
        .filter(Course.id == course_id)
        .first()
    )
