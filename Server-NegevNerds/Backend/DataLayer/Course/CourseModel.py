from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


from ..Base import Base


class CourseModel(Base):
    from Backend.DataLayer.UserCourses.UserCoursesModel import UserCoursesModel
    __tablename__ = 'courses'

    # Primary key
    course_id = Column(String(50),  primary_key=True,)
    name = Column(String,nullable=False)

    users = relationship('UserCoursesModel', back_populates='course', cascade='all, delete-orphan')
    topics = relationship('CourseTopicsModel', back_populates='course')
    managers = relationship('CourseManagersModel', back_populates='course')

    exams = relationship('ExamModel', back_populates='course')

    def to_business_model(self):
        from Backend.BusinessLayer.Course.Course import Course

        course = Course(
            course_id=self.course_id,
            name=self.name,
        )
        course.users = [user.user_id for user in self.users]
        course.course_topics = [topic.topic for topic in self.topics]
        course.managers = [manager.user_id for manager in self.managers]
        return course

    @classmethod
    def from_business_model(cls, course):

        return cls(
            course_id=course.course_id,
            name=course.name,
        )
