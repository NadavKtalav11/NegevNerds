from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ..Base import Base


class UserModel(Base):
    """
    SQLAlchemy ORM model for User
    Represents the database schema for storing user information
    """
    __tablename__ = 'users'

    # Primary key
    user_id = Column(String, primary_key=True)

    # User attributes matching the Business Layer User class
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    logged_in = Column(Boolean, default=False)

    # Define the relationship
    courses = relationship('UserCoursesModel', back_populates='user', cascade='all, delete-orphan')
    course_managers = relationship('CourseManagersModel', back_populates='manager')

    def to_business_model(self):
        from Backend.BusinessLayer.User.User import User
        """
        Convert SQLAlchemy model to Business Layer User object

        Returns:
            User: Business layer User instance
        """
        user = User(
            user_id=self.user_id,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            loggedIn=self.logged_in
        )
        #user.courses = self.courses
        user.courses = [course.course_id for course in self.courses]
        return user

    @classmethod
    def from_business_model(cls, user):
        """
        Create a UserModel instance from a Business Layer User object

        Args:
            user (User): Business layer User instance

        Returns:
            UserModel: SQLAlchemy UserModel instance
        """
        return cls(
            user_id=user.user_id,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            logged_in=user.loggedIn,

        )
