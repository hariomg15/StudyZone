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