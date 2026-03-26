from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.dependecies import get_db, get_current_user,require_teacher
from app.models.course import Course
from app.models.user import User, UserRole  
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate


router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
    current_user: User | None = Depends(get_current_user)
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


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter(Course.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
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
    return