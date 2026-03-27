from pydantic import BaseModel, Field

class SectionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    order_num: int = 1

class LectureCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    video_url: str
    duration: str | None = None  # Duration in seconds
    is_preview: bool = False
    order_num: int = 1

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    pdf_url: str 

class LectureResponse(BaseModel):
    id: int
    title: str
    video_url: str | None = None
    duration: int | None = None  # Duration in seconds
    is_preview: bool
    order_num: int

    class Config:
         from_attributes = True

class NoteResponse(BaseModel):
    id: int
    title: str
    pdf_url: str 

    class Config:
         from_attributes = True

class SectionResponse(BaseModel):
    id: int
    title: str
    order_num: int
    lectures: list[LectureResponse] = []
    notes: list[NoteResponse] = []

    class Config:
         from_attributes = True

class CourseContentResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    Sections: list[SectionResponse] = []

    class Config:
         from_attributes = True