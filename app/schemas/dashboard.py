from pydantic import BaseModel  

class AdminStatsResponse(BaseModel):
    total_users: int
    total_students: int
    total_teachers: int
    total_admins: int
    total_courses: int
    total_published_courses: int
    total_enrollments: int

    class Config:
        from_attributes = True
