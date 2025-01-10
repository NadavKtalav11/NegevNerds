from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..Base import Base


class UserCoursesModel(Base):

    __tablename__ = 'user_courses'


    # Primary key
    user_id = Column(String,  ForeignKey('users.user_id'), primary_key=True, nullable=False)
    course_id = Column(String, ForeignKey('courses.course_id'), primary_key=True, nullable=False)

    user = relationship('UserModel', back_populates='courses')
    course = relationship('CourseModel', back_populates='users')





