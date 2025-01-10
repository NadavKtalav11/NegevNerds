class BaseError(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, message="An error occurred", code=None):
        self.message = message
        self.code = code  # Optionally, you can include a code for each error
        super().__init__(self.message)


class UserAlreadyExistsError(BaseError):
    """Exception raised when the user already exists."""

    def __init__(self, email):
        message = f"User with email {email} already exists."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class InvalidEmailDomainError(BaseError):
    """Exception raised for invalid email domain."""

    def __init__(self, email):
        message = f"Invalid email domain for {email}. Please use a @post.bgu.ac.il or @bgu.ac.il email."
        super().__init__(message, code=400)  # 400 is commonly used for bad requests


class AuthenticationCodeError(BaseError):
    """Exception raised for authentication code errors."""

    def __init__(self, message="Authentication failed. Invalid or expired code."):
        super().__init__(message, code=401)  # 401 is commonly used for unauthorized errors


class EmailSendingError(BaseError):
    """Exception raised when email sending fails."""

    def __init__(self, message="Failed to send authentication code"):
        super().__init__(message, code=500)  # 500 can be used for server errors


class UserOrPasswordIncorrectError(BaseError):
    """Exception raised when password or email is incorrect."""

    def __init__(self):
        message = f"אימייל או סיסמה שגויים. אנא נסה שוב."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class UserDoesnotExistsError(BaseError):
    """Exception raised when the user is not exist."""

    def __init__(self, user_id):
        message = f"User with user_id {user_id} not exists."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors

class UserIsNotLoggedInError(BaseError):
    """Exception raised when tring to log out a not logged in user."""
    def __init__(self, email):
        message = f"לא ניתן להתנתק {email} מכיוון שהוא אינו מחובר."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors
        

class UserAlreadyRegisterToCourse(BaseError):
    """Exception raised when the user is already register to course."""

    def __init__(self):
        message = f"User is already registered to course."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class UserIsNotRegisterToCourse(BaseError):
    """Exception raised when the user is not register to course."""

    def __init__(self):
        message = f"User is not registered to course."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class CourseIsNotExist(BaseError):
    """Exception raised when the user is not exist."""

    def __init__(self, course_id):
        message = f"Course {course_id} is not exist."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class CourseAlreadyExists(BaseError):
    """Exception raised when the user is not exist."""

    def __init__(self, course_id):
        message = f"Course {course_id} is already exist."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors

class InvalidCourseIdFormat(BaseError):
    """Exception raised when course Id is in invalid format."""
    def __init__(self, course_id):
        message = f"הפורמט של הקורס {course_id} אינו תקין"
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors

class ManagerIsNotExist(BaseError):
    """Exception raised when the manager is not exist."""

    def __init__(self, manager_id):
        message = f"manager {manager_id} is not exist."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class ManagerAlreadyExists(BaseError):
    """Exception raised when the manager is not exist."""

    def __init__(self, manager_id):
        message = f"manager {manager_id} is already exist."
        super().__init__(message, code=409)


class ExamIsNotExist(BaseError):
    """Exception raised when the manager is not exist."""

    def __init__(self, year, semester, moed):
        message = f"exam from year- {year},semester- {semester}, moed- {moed} is not exist."
        super().__init__(message, code=409)  # 409 is commonly used for conflict errors


class ExamAlreadyExists(BaseError):
    """Exception raised when the manager is not exist."""

    def __init__(self, exam_Id):
        message = f"exam {exam_Id} is already exist."
        super().__init__(message, code=409)  # 4


class ReactionNotFound(BaseError):
    """Exception raised when the reaction does not exist."""

    def __init__(self, reaction_id):
        message = f"Reaction {reaction_id} not found."
        super().__init__(message, code=409)  # 4


class QuestionAlreadyInExam(BaseError):
    """Exception raised when the question is already part of the exam."""

    def __init__(self, question_id):
        message = f"The question with ID {question_id} is already in the exam."
        super().__init__(message, code=409)


class QuestionDoesNotMeetExamFields(BaseError):
    """Exception raised when the question does not meet the required fields for the exam."""

    def __init__(self, question_id):
        message = f"The question {question_id} does not meet the required fields for the exam."
        super().__init__(message, code=400)  # Bad Request


class QuestionNotFound(BaseError):
    """Exception raised when a question is not found in the list."""

    def __init__(self, question_id):
        message = f"Question '{question_id}' not found in the list."
        super().__init__(message, code=404)


class TopicAlreadyExist(BaseError):
    """Exception raised when a question topic is already in the course topics."""

    def __init__(self, question_topic):
        message = f"Topic '{question_topic}' is already in the course topics."
        super().__init__(message, code=404)


class TopicNotFound(BaseError):
    """Exception raised when a question topic is not found in the course topics."""

    def __init__(self, question_topic):
        message = f"Topic '{question_topic}' not found in the course topics."
        super().__init__(message, code=404)


class CommentNotFound(BaseError):
    """Exception raised when a Comment is not found in the list."""

    def __init__(self, comment_id):
        message = f"Comment with ID '{comment_id}' not found in the list."
        super().__init__(message, code=404)


class UserIsNotCourseManager(BaseError):
    """Exception raised when a Comment is not found in the list."""

    def __init__(self, course_id):
        message = f"User is not manager of course{course_id}"
        super().__init__(message, code=404)