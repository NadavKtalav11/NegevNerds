import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.QuestionTopics.QuestionTopicsRepository import QuestionTopicsRepository
from Backend.DataLayer.Questions.QuestionModel import Base, QuestionModel


class QuestionRepository:

    def __init__(self, db_path=None):
        """
        Initialize the database engine.

        :param db_path: Path to the SQLite database. If None, uses the default path.
        """
        if db_path is None:
            # Default to a local SQLite database file in the parent directory
            db_path = os.path.join(os.path.dirname(__file__), '../../..', 'NegevNerds.db')

        # Ensure the directory exists
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Use the full path to create the SQLite engine
        #print(f"Resolved database path: {db_path}")
        self.engine = create_engine(f'sqlite:///{db_path}')

        # Ensure all tables are created

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    def add_question(self, question, exam_id):
        if isinstance(question.semester,Semester):
            question.semester =question.semester.value
        if isinstance(question.moed, Moed):
            question.moed =question.moed.value

        session = self.Session()
        try:
            # Convert business model to SQLAlchemy model
            question_model = QuestionModel(
                question_id=question.id,
                year=question.year,
                is_american=question.is_american,
                link_to_question=question.link_to_question,
                link_to_answer = question.link_to_answer,
                link_to_exam=question.link_to_exam,
                semester=question.semester,
                moed=question.moed,
                question_number=question.question_number,
                exam_id=exam_id,
                text= question.text
            )


            session.add(question_model)

            topics_repo = QuestionTopicsRepository()
            topics_repo.add_question_topics(question_id=question.id, topics=question.question_topics, session = session)
            session.commit()

            # Get the auto-generated ID

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_question_by_id(self, question_id):

        session = self.Session()
        try:
            question_model = session.query(QuestionModel).filter_by(question_id=question_id).first()
            return question_model.to_business_model() if question_model else None
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_question_by_exam_id(self, exam_id):

        session = self.Session()
        try:
            question_models = session.query(QuestionModel).filter_by(exam_id=exam_id).all()
            return [question_model.to_business_model() for question_model in question_models]
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_questions_by_ids_list(self, ids):
        session = self.Session()
        try:
            questions = []
            for curr_id in ids:
                question_model = session.query(QuestionModel).filter_by(question_id=curr_id).first()
                if question_model is not None:
                    questions.append(question_model.to_business_model())
            return questions
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_questions_by_dto(self, dto):
        session = self.Session()
        try:
            question_model = session.query(QuestionModel).filter_by(question_id=dto.question_id).first()
            if question_model is not None:
                return question_model.to_business_model()
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_question_by_number(self, exam_id, question_number):
        session = self.Session()
        try:
            question_model = session.query(QuestionModel).filter_by(exam_id=exam_id, question_number=question_number).first()
            return question_model.to_business_model() if question_model else None
        except Exception as e:
            raise e
        finally:
            session.close()


    def update_question(self, question):
        if isinstance(question.semester,Semester):
            question.semester =question.semester.value
        if isinstance(question.moed, Moed):
            question.moed =question.moed.value
        session = self.Session()
        try:
            question_model = session.query(QuestionModel).filter_by(question_id=question.id).first()

            if not question_model:
                raise ValueError(f"No question found with ID {question.id}")

            # Update fields
            question_model.question_id = question.id,
            question_model.year = question.year,
            question_model.is_american = question.is_american,
            question_model.link_to_question = question.link_to_question,
            question_model.link_to_exam = question.link_to_exam,
            question_model.link_to_answer = question.link_to_answer
            question_model.semester = question.semester,
            question_model.moed = question.moed,
            question_model.question_number = question.question_number,
            question_model.text = question.text

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_question(self, question_id):

        session = self.Session()
        try:
            question_model = session.query(QuestionModel).filter_by(question_id=question_id).first()

            if not question_model:
                raise ValueError(f"No question found with ID {question_id}")

            session.delete(question_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def is_exist(self, year, semester, moed, text):

        session = self.Session()
        try:
            curr = session.query(QuestionModel).filter_by(year=year, semester=semester,
                                                             moed=moed, text=text).first()
            return curr is not None
        except Exception as e:
            raise e
        finally:
            session.close()

    def uploadSolution(self, question_id, link_to_answer):
        """
        Update the link field of an existing exam.
        """
        session = self.Session()
        try:
            # Find the existing exam
            question_model = session.query(QuestionModel).filter_by(question_id=question_id).first()

            if not question_model:
                raise ValueError(f"No exam found with ID {question_id}")

            # Update only the link field
            question_model.link_to_answer = link_to_answer
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



