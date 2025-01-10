import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.CourseManagers.CourseManagersModel import CourseManagersModel
from Backend.DataLayer.UserCourses.UserCoursesModel import Base, UserCoursesModel


class CourseManagersRepository:
    """Repository for handling User database operations"""
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

    def add_manager_to_course(self, user_id, course_id):
        """
        Add a user to a course

        Args:
            user_id (str): ID of the user
            course_id (str): ID of the course
        """
        session = self.Session()
        try:
            association = CourseManagersModel(user_id=user_id, course_id=course_id)
            session.add(association)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_manager_from_course(self, user_id, course_id):
        """
        Remove a user from a course

        Args:
            user_id (str): ID of the user
            course_id (str): ID of the course
        """
        session = self.Session()
        try:
            association = session.query(CourseManagersModel).filter_by(user_id=user_id, course_id=course_id).first()
            if association:
                session.delete(association)
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_managers_for_course(self, course_id):
        """
        Get all users for a given course

        Args:
            course_id (str): ID of the course

        Returns:
            List[User]: List of business layer User objects
        """
        session = self.Session()
        try:
            associations = session.query(CourseManagersModel).filter_by(course_id=course_id).all()
            return [association.user.to_business_model() for association in associations]
        except Exception as e:
            raise e
        finally:
            session.close()


    def is_exist(self, course_id,user_id ):

        session = self.Session()
        try:
            manager = session.query(CourseManagersModel).filter_by(user_id=user_id, course_id=course_id).first()
            return manager is not None
        except Exception as e:
            raise e
        finally:
            session.close()
    
   

