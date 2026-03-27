from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload

from app.core.dependecies import get_db, get_current_user, require_teacher
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole
from app.schemas.enrollment import EnrollmentResponse, MyEnrollmentCourseResponse, EnrolledStudentInfo, CourseStudentEnrollmentResponse

router=APIRouter()

@router.post("/{course_id}", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses."
        )
   
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    if not course.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot enroll in an unpublished course"
        )
    
    #AGAR course hai toh check karenge ki user already enrolled hai ya nahi
    existing_enrollment = db.query(Enrollment).filter(Enrollment.user_id == current_user.id, Enrollment.course_id == course_id).first()
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course."
        )
    
    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment   



@router.get("/my",response_model=list[MyEnrollmentCourseResponse])
def get_my_enrollments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
     if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can view their enrollments."
        )
     
     enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course).joinedload(Course.teacher))
        .filter(Enrollment.user_id == current_user.id)
        .all()
     )

     return enrollments

@router.get("/course/{course_id}" , response_model=list[CourseStudentEnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.teacher != UserRole.admin and course.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view enrollments for this course."
        )

    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.student))
        .filter(Enrollment.course_id == course_id)
        .all()
    )

    return enrollments