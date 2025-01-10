import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.Base import Base
from Backend.DataLayer.CourseTopics.CourseTopicsModel import CourseTopicsModel


class CourseTopicsRepository:

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

    def add_Topic_to_course(self, course_id, topic):

        session = self.Session()
        try:
            association = CourseTopicsModel(course_id=course_id, topic=topic)
            session.add(association)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_topics_to_course(self, course_id, topics, session):


        try:
            for topic in topics:
                association = CourseTopicsModel(course_id=course_id, topic=topic)
                session.add(association)
            #session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def remove_topic_from_course(self, topic, course_id):
        session = self.Session()
        try:
            association = session.query(CourseTopicsModel).filter_by(topic=topic, course_id=course_id).first()
            if association:
                session.delete(association)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_course_topics(self, course_id):

        session = self.Session()
        try:
            associations = session.query().filter_by(course_id=course_id).all()
            return [association.course.to_business_model() for association in associations]
        except Exception as e:
            raise e
        finally:
            session.close()


    def is_exist(self, topic, course_id):

        session = self.Session()
        try:
            manager = session.query(CourseTopicsModel).filter_by(topic=topic, course_id=course_id).first()
            return manager is not None
        except Exception as e:
            raise e
        finally:
            session.close()



