from sqlalchemy import Column, Integer, String, Text,Boolean,Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False,index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.0)
    is_free=Column(Boolean, default=False  )
    thumbnail = Column(String(255), nullable=True)
    is_published=Column(Boolean, default=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    teacher = relationship("User", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    sections = relationship("Section", back_populates="course", cascade="all, delete-orphan")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    order_num = Column(Integer, default=1)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    course = relationship("Course", back_populates="sections")
    lectures = relationship("Lecture", back_populates="section", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="section", cascade="all, delete-orphan")

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    video_url = Column(String(255), nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    is_preview = Column(Boolean, default=False)
    order_num = Column(Integer, default=1)
    section_id = Column(Integer, ForeignKey("sections.id",ondelete="CASCADE"), nullable=False)

    section = relationship("Section", back_populates="lectures")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    pdf_url = Column(String(255), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id",ondelete="CASCADE"), nullable=False)

    section = relationship("Section", back_populates="notes")