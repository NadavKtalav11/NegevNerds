import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.Base import Base
from Backend.DataLayer.CourseTopics.CourseTopicsModel import CourseTopicsModel
from Backend.DataLayer.QuestionTopics.QuestionTopicsModel import QuestionTopicsModel


class QuestionTopicsRepository:

    def __init__(self, db_path=None, session=None):
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
        # print(f"Resolved database path: {db_path}")
        self.engine = create_engine(f'sqlite:///{db_path}')

        # Ensure all tables are created
        Base.metadata.create_all(self.engine)
        if session is None:
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.Session = session

    def add_Topic_to_Question(self, question_id, topic):

        session = self.Session()
        try:
            association = QuestionTopicsModel(question_id=question_id, topic=topic)
            session.add(association)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_question_topics(self, question_id, topics, session):

        try:
            for topic in topics:
                association = QuestionTopicsModel(question_id=question_id, topic=topic)
                session.add(association)
            #session.commit()
        except Exception as e:
            session.rollback()
            raise e


    def remove_topic_from_question(self, topic, question_id):
        session = self.Session()
        try:
            association = session.query(QuestionTopicsModel).filter_by(topic=topic, question_id=question_id).first()
            if association:
                session.delete(association)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_question_topics(self, question_id):

        session = self.Session()
        try:
            associations = session.query().filter_by(question_id=question_id).all()
            return [association.topic for association in associations]
        except Exception as e:
            raise e
        finally:
            session.close()

    def is_exist(self, topic, question_id):

        session = self.Session()
        try:
            manager = session.query(QuestionTopicsModel).filter_by(topic=topic, question_id=question_id).first()
            return manager is not None
        except Exception as e:
            raise e
        finally:
            session.close()
    

    def delete_topics_by_question_id(self, question_id):
        """
        Deletes all topic associated with a specific question ID.

        Args:
            question_id (str): The ID of the question whose topics should be deleted.
        """
        session = self.Session()
        try:
            # Query to find all comments for the given question_id
            topics = session.query(QuestionTopicsModel).filter_by(question_id=question_id).all()
            
            if not topics:
                raise ValueError(f"No topics found for question ID {question_id}")

            # Delete all retrieved comments
            for topic in topics:
                session.delete(topic)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()




