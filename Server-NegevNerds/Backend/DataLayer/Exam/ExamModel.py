from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..Base import Base
from ...BusinessLayer.Course.enums import Moed, Semester


class ExamModel(Base):
    __tablename__ = 'exams'

    # Primary key
    year = Column(Integer, primary_key=True)
    semester = Column(String, primary_key=True)
    moed = Column(String, primary_key=True)

    exam_id = Column(String, unique=True)
    course_id = Column(String, ForeignKey('courses.course_id'),  nullable=False)
    link = Column(String, nullable=True)

    course = relationship('CourseModel', back_populates='exams')
    questions = relationship('QuestionModel', back_populates='exam', cascade='all, delete')




    def to_business_model(self):
        from Backend.BusinessLayer.Course.Exam import Exam

        exam = Exam(
            exam_id=self.exam_id,
            semester=Semester(self.semester),
            moed=Moed(self.moed),
            year=self.year,
            link=self.link,
            course_id=self.course_id
        )
        return exam

    @classmethod
    def from_business_model(cls, exam):
        return cls(
            exam_id=exam.exam_id,
            semester=exam.semester.value,
            moed=exam.moed.value,
            year=exam.year,
            link=exam.link,
            course_id=exam.course_id
        )
