from fastapi import APIRouter, Depends, HTTPException, status ,Query
from sqlalchemy.orm import Session, joinedload ,selectinload

from app.core.dependecies import get_db, get_current_user_optional, require_teacher
from app.models.course import Course,Section, Lecture, Note
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole  
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.schemas.content import SectionCreate, SectionResponse, LectureCreate, LectureResponse, NoteResponse, CourseContentResponse,NoteCreate

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(require_teacher)):
    if course_data.is_free:
        course_data.price = 0.0
    if not course_data.is_free and course_data.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be greater than 0 for paid courses")   
    
    new_course = Course(
        title=course_data.title,
        description=course_data.description,
        price=course_data.price,
        is_free=course_data.is_free,
        thumbnail=course_data.thumbnail,
        is_published=course_data.is_published,
        teacher_id=current_user.id

    ) 
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    course=(
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == new_course.id)
        .first()
    )

    return course

@router.get("/", response_model=list[CourseResponse])
def list_courses(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    if current_user and current_user.role in ["teacher", "admin"]:
        courses = (
            db.query(Course)
            .options(joinedload(Course.teacher))
            .all()
        )
    else:
        courses = (
            db.query(Course)
            .options(joinedload(Course.teacher))
            .filter(Course.is_published == True)
            .all()
        )
    return courses

@router.get("/search", response_model=list[CourseResponse])
def search_courses( 
    q : str = Query(...,min_length=1),
    db:Session = Depends(get_db)
):

    courses = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(
            Course.is_published == True,
            Course.title.ilike(f"%{q}%")   
        )
        .all()
    )
    return courses


@router.get("/my/created", response_model=list[CourseResponse])
def get_my_created_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    courses = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.teacher_id == current_user.id)
        .all()
    )
    return courses

@router.patch("/{course_id}/publish", response_model=CourseResponse)
def publish_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to publish this course")
    
    course.is_published = True
    db.commit()
    db.refresh(course)

    course=(
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )
    return course

@router.patch("/{course_id}/unpublish", response_model=CourseResponse)
def unpublish_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to unpublish this course")
    
    course.is_published = False
    db.commit()
    db.refresh(course)

    course=(
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )
    return course


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    course = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if not course.is_published:
        is_owner = current_user and (current_user.role == UserRole.admin or course.teacher_id == current_user.id)
        if not is_owner:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Course is not published")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id :int, 
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
  
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if current_user.role != "admin" and course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this course")
    
    update_data =course_data.model_dump(exclude_unset=True)

    if "is_free" in update_data and update_data["is_free"] is True:
        update_data["price"] = 0.0

    if "price" in update_data and update_data["price"] is not None and update_data["price"] <0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Price must be greater than or equal to 0"
        )
    
    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    course = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )

    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_teacher)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    # Only teacher who created the course or admin can delete
    if course.teacher_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this course")
    
    db.delete(course)
    db.commit()
    return "deleted"


# Additional endpoints for sections, lectures, and notes can be implemented similarly, ensuring proper authorization and data validation.
@router.post("/{course_id}/sections" , response_model=SectionResponse,status_code=status.HTTP_201_CREATED)
def create_section(
    course_id: int,
    section_data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    if current_user.role != UserRole.admin and course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add section to this course")
    
    new_section = Section(
        course_id = course_id,
        title=section_data.title,
        order_num =section_data.order_num    
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section

@router.post("/sections/{section_id}/lectures", response_model=LectureResponse, status_code=status.HTTP_200_OK)
def add_lecture(
    section_id: int,
    lecture_data: LectureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    section = db.query(Section).filter(Section.id == section_id).first()
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    if current_user.role != UserRole.admin and section.course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add lecture to this section")
    
    lecture = Lecture(
        title=lecture_data.title,
        video_url=lecture_data.video_url,
        duration=lecture_data.duration,
        is_preview=lecture_data.is_preview,
        order_num=lecture_data.order_num,
        section_id=section_id
    )

    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return lecture

@router.post("/sections/{section_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def add_note(
    section_id: int,
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    section = db.query(Section).filter(Section.id == section_id).first()

    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    if current_user.role != UserRole.admin and section.course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add note to this section")
    
    note = Note(
        title=note_data.title,
        pdf_url=note_data.pdf_url,
        section_id=section_id
    )

    db.add(note)
    db.commit()
    db.refresh(note)
    return note
    
  
@router.get("/{course_id}/content", response_model=CourseContentResponse, status_code=status.HTTP_200_OK)
def get_course_content(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    course = (
        db.query(Course)
        .options(
            selectinload(Course.sections).selectinload(Section.lectures),
            selectinload(Course.sections).selectinload(Section.notes)
        )
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if not course.is_published:
        is_owner = current_user and (current_user.role == UserRole.admin or course.teacher_id == current_user.id)
        if not is_owner:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Course is not published")

    if course.is_free:
        return course
    
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not free course. Please complete payment to access it.",
        )

    if current_user.role in [UserRole.teacher, UserRole.admin]:
        if current_user.role == UserRole.teacher and course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this course content")
        return course

    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.course_id == course_id, Enrollment.user_id == current_user.id)
        .first()
    )

    if enrollment is None :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This is not free course. Please complete payment to access it.",
        )
    
    return course
