import os

from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.Course.CourseModel import Base, CourseModel
from Backend.DataLayer.CourseTopics.CourseTopicsRepository import CourseTopicsRepository


class CourseRepository:

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
        #print(f"Resolved database path: {db_path}")
        self.engine = create_engine(f'sqlite:///{db_path}')

        # Ensure all tables are created

        Base.metadata.create_all(self.engine)
        if session is None:
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.Session = session

    def add_course(self, course):

        session = self.Session()
        try:
            # Convert business model to SQLAlchemy model
            course_model = CourseModel(
                course_id=course.course_id,
                name=course.name,
            )
            course_topics_repo = CourseTopicsRepository()
            course_topics_repo.add_topics_to_course(course_id=course.course_id, topics=course.course_topics,
                                                    session=session)
            session.add(course_model)
            session.commit()

            # Get the auto-generated ID

            return
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_course_by_id(self, course_id):

        session = self.Session()
        try:
            course_model = session.query(CourseModel).filter_by(course_id=course_id).first()
            return course_model.to_business_model() if course_model else None
        finally:
            session.close()

    def get_all_courses(self):
        session = self.Session()
        try:
            course_model = session.query(CourseModel).all()
            return [course.to_business_model() for course in course_model]
        finally:
            session.close()



    def update_course(self, course):

        session = self.Session()
        try:

            course_model = session.query(CourseModel).filter_by(course_id=course.course_id).first()

            if not course_model:
                raise ValueError(f"No course found with ID {course_model.course_id}")

            # Update fields
            course_model.course_id = course.course_id
            course_model.name = course.name

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_course(self, course_id):

        session = self.Session()
        try:
            course_model = session.query(CourseModel).filter_by(course_id=course_id).first()

            if not course_model:
                raise ValueError(f"No course found with ID {course_id}")

            session.delete(course_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def is_exist(self, course_id):

        session = self.Session()
        try:
            course = session.query(CourseModel).filter_by(course_id=course_id).first()
            return course is not None
        finally:
            session.close()

