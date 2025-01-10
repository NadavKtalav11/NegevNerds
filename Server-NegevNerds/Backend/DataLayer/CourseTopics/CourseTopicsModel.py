from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..Base import Base


class CourseTopicsModel(Base):

    __tablename__ = 'course_topics'

    # Primary key
    course_id = Column(String,  ForeignKey('courses.course_id'), primary_key=True, nullable=False)
    topic = Column(String, primary_key=True, nullable=False)

    course = relationship('CourseModel', back_populates='topics')
