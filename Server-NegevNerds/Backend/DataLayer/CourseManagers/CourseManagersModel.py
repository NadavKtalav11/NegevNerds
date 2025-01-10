from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..Base import Base


class CourseManagersModel(Base):

    __tablename__ = 'course_managers'


    # Primary key
    course_id = Column(String,  ForeignKey('courses.course_id'), primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True, nullable=False)

    course = relationship('CourseModel', back_populates='managers')
    manager = relationship('UserModel', back_populates='course_managers')
