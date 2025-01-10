
from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.orm import relationship

from ..Base import Base
from ...BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.Comment.CommentModel import CommentModel


class QuestionModel(Base):

    __tablename__ = 'questions'

    # Primary key
    question_id = Column(String)

    year = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    moed = Column(String, nullable=False)
    question_number = Column(Integer, nullable=False, primary_key=True)
    is_american = Column(Boolean, nullable=False)
    link_to_question = Column(String, nullable=False)
    link_to_exam = Column(String, nullable=True)
    link_to_answer = Column(String, nullable=True)
    exam_id = Column(String, ForeignKey('exams.exam_id'), primary_key=True)

    topics = relationship('QuestionTopicsModel', back_populates='question', cascade='all, delete')
    exam = relationship('ExamModel', back_populates='questions')

    comments = relationship('CommentModel',
                          back_populates='question',
                          cascade='all, delete')

    def to_business_model(self):
        from Backend.BusinessLayer.Course.Question import Question

        # Extract the string topics from the related QuestionTopicsModel instances
        business_topics = [topic.topic for topic in self.topics]  # Assuming 'name' is the string field

        # No changes for comments if they're the same as before
        business_comments = [comment.to_business_model() for comment in self.comments]

        # Create the business model
        question = Question(
            question_id=self.question_id,
            year=self.year,
            is_american=self.is_american,
            link_to_question=self.link_to_question,
            link_to_exam=self.link_to_question,
            link_to_answer=self.link_to_answer,
            semester=Semester(self.semester),
            moed=Moed(self.moed),
            question_number=self.question_number,
            text=self.text,
            question_topics=business_topics,  # List of strings
            comments=business_comments
        )
        return question

    @classmethod
    def from_business_model(cls, question, exam_id):

        return cls(
            question_id=question.id,
            year=question.year,
            is_american=question.is_american,
            link_to_question=question.link_to_question,
            link_to_exam=question.link_to_question,
            semester=question.semester.value,
            moed=question.moed.value,
            question_number=question.question_number,
            link_to_answer=question.link_to_answer,
            exam_id=question.exam_id,
            text=question.text

        )
