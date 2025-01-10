from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..Base import Base


class QuestionTopicsModel(Base):

    __tablename__ = 'question_topics'

    # Primary key
    question_id = Column(String,  ForeignKey('questions.question_id'), primary_key=True, nullable=False)
    topic = Column(String, primary_key=True, nullable=False)

    question = relationship('QuestionModel', back_populates='topics')
