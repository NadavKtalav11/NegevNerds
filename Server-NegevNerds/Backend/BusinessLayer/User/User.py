import threading

from Backend.BusinessLayer.Util.Exceptions import *
from Backend.DataLayer.User.UserRepository import UserRepository  # Import the repository
from Backend.DataLayer.UserCourses.UserCoursesRepository import UserCoursesRepository


class User:
    def __init__(self, user_id, email, password, first_name, last_name, loggedIn=False):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.loggedIn = loggedIn
        self.courses = []

        self.courses_lock = threading.Lock()

        # Create a repository instance for database operations
        self._repo = UserRepository()

    @classmethod
    def create(cls, user_id, email, password, first_name, last_name):
        """
        Class method to create a new user and save to database

        Returns:
            User: Newly created user instance
        """
        user = cls(
            user_id=user_id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user_repository = UserRepository()
        user_repository.add_user(user)

        # db.session.add(user)
        # db.session.commit()

        # Save to database and get the generated ID
        return user

    @classmethod
    def get_by_id(cls, user_id):
        """
        Retrieve a user by their ID

        Args:
            user_id (int): User's unique identifier

        Returns:
            User: User instance or None if not found
        """
        repo = UserRepository()
        return repo.get_user_by_id(user_id)

    def login(self):
        """
        Log in the user and update the database
        """
        self.loggedIn = True
        self._repo.update_user(self)

    def logout(self):
        """
        Log out the user and update the database
        """
        self.loggedIn = False
        self._repo.update_user(self)

    def registerToCourse(self, course_id):
        """
        Register user to a course and update the database

        Raises:
            UserAlreadyRegisterToCourse: If user is already registered
        """
        with self.courses_lock:
            user_courses_repo = UserCoursesRepository()
            if course_id not in self.courses and not user_courses_repo.is_exist(user_id=self.user_id, course_id=course_id):
                self.courses.append(course_id)
                user_courses_repo.add_user_to_course(user_id=self.user_id, course_id=course_id)
                self._repo.update_user(self)
            else:
                raise UserAlreadyRegisterToCourse()

    def removeCourse(self, course_id):
        with self.courses_lock:
            courses_repo = UserCoursesRepository()
            if course_id in self.courses or courses_repo.is_exist(user_id=self.user_id, course_id=course_id):
                self.courses.remove(course_id)
                self._repo.update_user(self)
                courses_repo.remove_user_from_course(user_id=self.user_id, course_id=course_id)
            else:
                raise UserIsNotRegisterToCourse()

    def editProfile(self, email=None, password=None, first_name=None, last_name=None):
        """
        Edit user profile and update the database

        Args:
            email (str, optional): New email address
            password (str, optional): New password
            first_name (str, optional): New first name
            last_name (str, optional): New last name
        """
        if email:
            self.email = email
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name

        # Update the user in the database
        self._repo.update_user(self)

    def delete(self):
        """
        Delete the user from the database
        """
        if self.user_id:
            self._repo.delete_user(self.user_id)
            # Optionally, you might want to reset the user's attributes
            self.user_id = None

    def get_courses(self):
        """
        Get the list of courses the user is registered to

        Returns:
            list: List of course IDs
        """
        with self.courses_lock:
            return self.courses

    def get_first_name(self):
        return self.first_name

    def get_user_id(self):
        return self.user_id

    def get_last_name(self):
        return self.last_name


