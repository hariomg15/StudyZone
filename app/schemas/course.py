from pydantic import BaseModel, Field

class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    price: float | None = None
    is_free: bool = Field(False)
    thumbnail: str | None = None
    is_published: bool = Field(False)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    title: str = Field(None, min_length=2, max_length=255)
    description:str|None=None
    price: float|None=None
    is_free: bool|None=None
    thumbnail: str|None=None
    is_published: bool|None=None

class Teacherinfo(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        from_attribute = True

class CourseResponse(CourseBase):
    id: int
    teacher_id: int
    teacher: Teacherinfo

    class Config:
        from_attribute = True