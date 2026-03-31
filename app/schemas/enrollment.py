from pydantic import BaseModel
from app.schemas.course import CourseResponse
from app.db.base import Base

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    

    class Config:
        from_attributes = True

class MyEnrollmentCourseResponse(BaseModel):
    id: int
    course: CourseResponse

    class Config:
        from_attributes = True

class EnrolledStudentInfo(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class CourseStudentEnrollmentResponse(BaseModel):
    id: int
    student: EnrolledStudentInfo

    class Config:
        from_attributes = True
    
