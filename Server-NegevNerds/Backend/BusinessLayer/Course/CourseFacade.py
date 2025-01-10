import threading
from typing import List

from Backend.BusinessLayer.Course.Course import Course
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.DataLayer.Course.CourseRepository import CourseRepository
from Backend.DataLayer.DTOs.CourseDTO import CourseDTO
import re
from Backend.BusinessLayer.Course.enums import *
import logging

from Backend.DataLayer.DTOs.SearchDTO import SearchDTO
from Backend.DataLayer.Questions.QuestionRepository import QuestionRepository

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from Backend.DataLayer.UserCourses.UserCoursesRepository import UserCoursesRepository


class CourseFacade:
    _instance = None  # Class-level attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'courses'):
            self.courses = {}  # courseId, Course
            #self.course_repository = CourseRepository()
            #self.user_courses_repository = UserCoursesRepository()

            self.courses_lock = threading.Lock()


    """--------------course functionality--------------"""

    def register_to_course(self, course_id, user_id):
        course = self.get_course(course_id)
        if course is not None:
            course.add_student(user_id)
            #user_courses_rep = UserCoursesRepository()
            #user_courses_rep.add_user_to_course(user_id=user_id, course_id=course_id)


    def get_questions_dto_by_search_dtos(self , dtos: List[SearchDTO]):
        questions_repo = QuestionRepository()
        dtos_list = []
        for dto in dtos:
            question = questions_repo.get_questions_by_dto(dto)
            dtos_list.append(question.to_dto(dto.course_id))
        return dtos_list


    def get_questions_dto_by_ids(self , ids, course_id):
        questions_repo = QuestionRepository()
        dtos_list = []
        questions = questions_repo.get_questions_by_ids_list(ids)
        for question in questions:
            dtos_list.append(question.to_dto(course_id=course_id))
        return dtos_list


    def remove_student_from_course(self, course_id, user_id):
        """Removes a student from the course."""
        course = self.get_course(course_id)
        if course is not None:
            course.remove_student(user_id)
        else:
            raise CourseIsNotExist(course_id)

    def open_course(self, course_id, name, course_topics):
        """Opens a new course"""
        with self.courses_lock:
            course = Course.create(course_id=course_id, name=name, course_topics=course_topics)
            if course is not None:
                self.courses[course_id] = course
            else:
                raise Exception("error while creating course")
    
    def open_course_possibility(self, course_id, course_name):
        """Opens a new course"""

        if self.get_course(course_id) is not None:
            raise CourseAlreadyExists(course_id)
        
        if not self.is_valid_courseID(course_id):
            raise InvalidCourseIdFormat(course_id)
        
        if not self.is_valid_course_name(course_name):
            raise Exception("שם  קורס אינו תקין.")

        return True

    def is_valid_course_name(self, name):
        """
        Validates a name to ensure it contains only Hebrew characters, digits, spaces, hyphens, and double quotes.

        Args:
        name (str): The name to validate.

        Returns:
        bool: True if the name is valid, False otherwise.
        """
        # Regular expression to allow Hebrew letters, digits, spaces, hyphens, and double quotes
        hebrew_name_regex = r'^[\u0590-\u05FF0-9\s"\-]+$'

        # Validate the name using regex
        return bool(re.match(hebrew_name_regex, name))

    def remove_course(self, course_id):
        """Remove an existing course along with its folder."""
        with self.courses_lock:
            course = self.get_course(course_id)
            if course is not None:
                del self.courses[course_id]
                course_repo = CourseRepository()
                course_repo.delete_course(course_id=course_id)
            else:
                raise CourseIsNotExist(course_id)

    def get_question_path(self, course_id, year, semester, moed, question_number):
        course = self.get_course(course_id=course_id)
        if course is not None:
            return course.get_question_path(year, semester, moed, question_number)
        else:
            raise CourseIsNotExist(course_id)

    def get_answer_path(self, course_id, year, semester, moed, question_number):
        course = self.get_course(course_id=course_id)
        if course is not None:
            return course.get_answer_path(year, semester, moed, question_number)
        else:
            raise CourseIsNotExist(course_id)

    def get_course(self, course_id):
        """
        Retrieves a course by its ID.
        """
        with self.courses_lock:
            if course_id in self.courses.keys():
                return self.courses[course_id]

            course_repo = CourseRepository()
            if course_repo.is_exist(course_id=course_id):
                course = course_repo.get_course_by_id(course_id=course_id)
                return course
            return None

    def set_syllabus_of_course(self, course_id, syllabus):
        """Set syllabus of an existing course"""

        if self.get_course(course_id) is not None:
            self.get_course(course_id).set_syllabus(syllabus)
        else:
            raise CourseIsNotExist(course_id)

    def is_course_manager(self, course_id, user_id):
        """Checks if the user is a manager of the given course."""
        course = self.get_course(course_id)
        return user_id in course.managers

    def add_manager_to_course(self, course_id, manager_id):
        """
        Adds a manager to a course.

        :param course_id: The ID of the course.
        :param manager_id: The ID of the manager to add.
        """
        course = self.get_course(course_id)
        course.add_manager(manager_id)

    def remove_manager_from_course(self, course_id, manager_id):
        """
        Removes a manager from a course.
        """
        course = self.get_course(course_id)
        course.remove_manager(manager_id)

    def add_course_topic(self, course_id, course_topic):
        course = self.get_course(course_id)
        course.add_course_topic(course_topic)

    def remove_course_topic(self, course_id, course_topic):
        course = self.get_course(course_id)
        course.remove_course_topic(course_topic)

    def get_all_courses(self):
        course_list = []
        course_repo = CourseRepository()
        for course in course_repo.get_all_courses():
            course_list.append(CourseDTO(course=course))
        return course_list

    def get_course_DTO(self, course_id):
        if self.get_course(course_id) is not None:
            course = self.get_course(course_id)
            return CourseDTO(course_id, course.get_name())
        raise CourseIsNotExist(course_id)

    def get_courses_DTO(self, courses_ids):
        dtos = []
        for course_id in courses_ids:
            course = self.get_course(course_id)
            if course is not None:
                course_dto = CourseDTO(course_id, course.get_name())
                dtos.append(course_dto)
        return dtos

    def get_course_topics(self, course_id):
        if self.get_course(course_id) is None:
            return None
        else:
            return self.get_course(course_id).get_topics()

    """--------------exams functionality--------------"""

    def add_exam_to_course(self, course_id, course_name, link, year, semester, moed):
        """
        Adds an exam to a course.
        """
        course = self.get_course(course_id)
        course.add_exam(course_name, link, year, semester, moed)

    def remove_exam_from_course(self, course_id, year, semester, moed):
        """
        Removes an exam from a course.
        """
        course = self.get_course(course_id)
        course.remove_exam(year, semester, moed)

    def sort_exams(self, exams):
        """Sort exams by year (descending), semester (ascending), and moed (ascending)."""
        return sorted(
            exams,
            key=lambda exam: (-exam.get("year", 0), exam.get("semester", ""), exam.get("moed", ""))
        )

    def search_exam_by_specifics(self, course_id, year: int, semester=None, moed=None):
        """
        Retrieves all exams for a course in specific year and optionally filters by semester and moed.

        :param course_id: The ID of the course.
        :param year: Optional filter by year.
        :param semester: Optional filter by semester.
        :param moed: Optional filter by moed.
        :return: List of exams matching the criteria.
        """
        course = self.get_course(course_id)
        exams = course.get_exams(year, semester, moed)  # Assuming Course class has this method

        sorted_exams = self.sort_exams(exams)

        return sorted_exams
    
    def is_valid_courseID(self,courseId):
        """
        Validates if a course ID is in the correct format: xxx.x.xxxx
        where x is a digit.

        Args:
            courseId (str): The course ID to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        pattern = r"^\d{3}\.\d\.\d{4}$"
        return bool(re.match(pattern, courseId))

    def search_all_course_exams(self, course_id):
        """
        Retrieves all exams for a specific course

        :param course_id: The ID of the course.
        :return: List of exams matching the criteria.
        """
        course = self.get_course(course_id)
        exams = course.get_all_exams()  # Assuming Course class has this method
        sorted_exams = self.sort_exams(exams)

        return sorted_exams

    def edit_exam_course_name(self, course_id, year, semester, moed, new_course_name):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).edit_course_name(new_course_name)

    def edit_exam_link(self, course_id, year, semester, moed, new_link):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).edit_link(new_link)

    def edit_exam_year(self, course_id, year, semester, moed, new_year):
        course = self.get_course(course_id)
        course.edit_exam_year(year, semester, moed, new_year)

    def edit_exam_semester(self, course_id, year, semester, moed, new_semester):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).edit_semester(new_semester)

    def edit_exam_moed(self, course_id, year, semester, moed, new_moed):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).edit_moed(new_moed)

    """--------------question functionality--------------"""

    def valid_question_parameters(self, year, semester, moed, question_number):
        """Validates question parameters to ensure they are correct and relevant."""
        moeds = ['א','ב','ג','ד']
        semesters =['סתיו','אביב','קיץ']
        if moed not in moeds:
            logging.error(f"{Moed} is not a valid Moed.")
            raise ValueError(f"Invalid Moed: {moed}")
        if semester not in semesters:
            logging.error(f"{semester} is not a valid Semester.")
            raise ValueError(f"Invalid Semester: {semester}")
        # Validate year
        if year < 1960:
            logging.error(f"{year} is not a valid year. Must be 1960 or later.")
            raise ValueError(f"Invalid year: {year}")

        # Validate question number
        if question_number < 0:
            logging.error(f"{question_number} is not a question number. Must be non-negative.")
            raise ValueError(f"Invalid question number: {question_number}")

        return True

    def check_valid_question(self, course_id, year, semester, moed, question_number, question_text):
        # Step 1: Validate parameters
        self.valid_question_parameters(year=year, semester=semester, moed=moed, question_number=question_number)
        semester = Semester(semester)
        moed = Moed(moed)

        # Step 2: Get the course
        course = self.get_course(course_id=course_id)
        #if not course:
        #    raise ValueError(f"Course with ID {course_id} does not exist.")

        # Step 3: Delegate further validation to the course
        return course.check_valid_question(year=year, semester=semester, moed=moed, question_number=question_number, question_text=question_text)

    def add_question(self, course_id, year, semester, moed, question_number, is_american,
                     question_topics, pdf_question_path, pdf_answer_path, question_text):
        """
        Delegates question addition to the specified Exam.
        """
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            logging.info(f"Question: {year} {semester} {moed} {question_number} was added successfully.")
            return course.add_question(year, semester, moed, question_number, is_american, question_topics,
                                       pdf_question_path, pdf_answer_path, question_text)
        except Exception as e:
            logging.error(f"Question: {year} {semester} {moed} {question_number} was not added.")
            raise Exception(f"CourseFacade Error: {str(e)}")
    
    def check_exam_full_pdf(self, course_id, year, semester, moed, ):
        """
        """
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.check_exam_full_pdf(year, semester, moed)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")
    
    def checkExistSolution(self, course_id, year, semester, moed,question_number ):
        """
        """
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.checkExistSolution(year, semester, moed,question_number)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")
    
    def checkExistQuestion(self, course_id, year, semester, moed,question_number ):
        """
        """
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.checkExistQuestion(year, semester, moed,question_number)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")
    
    
    
    def upload_full_exam_pdf(self, course_id, year, semester, moed, exam_path):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.upload_full_exam_pdf(year, semester, moed, exam_path)
        except Exception as e:
            print(f"Error in CourseFacade.upload_full_exam_pdf: {str(e)}")
            raise Exception(f"CourseFacade Error: {str(e)}")
    
    def uploadSolution(self, course_id, year, semester, moed, question_number, answer_path_path):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.uploadSolution(year, semester, moed,question_number, answer_path_path)
        except Exception as e:
            print(f"Error in CourseFacade.upload_full_exam_pdf: {str(e)}")
            raise Exception(f"CourseFacade Error: {str(e)}")
    def add_comment(self, course_id, year, semester, moed, question_number, writer_name, writer_id,prev_id, comment_text):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.add_comment(year, semester, moed, question_number, writer_name,writer_id, prev_id, comment_text)

        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")

    def add_reaction(self, course_id, year, semester, moed, question_number, comment_id, user_id, emoji):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            return course.add_reaction(year, semester, moed, question_number, comment_id, user_id, emoji)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")

    def delete_comment(self, course_id, year, semester, moed, question_number, comment_id):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            course.delete_comment(year, semester, moed, question_number, comment_id)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")

    def remove_reaction(self, course_id, year, semester, moed, question_number, comment_id, reaction_id):
        try:
            course = self.get_course(course_id)
            if not course:
                raise Exception(f"Course with ID {course_id} not found.")
            course.remove_reaction(year, semester, moed, question_number, comment_id, reaction_id)
        except Exception as e:
            raise Exception(f"CourseFacade Error: {str(e)}")

    def remove_question(self, course_id, year, semester, moed, question_number):
        """
        Delegates question removal to the specified Exam.
        """
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).remove_question(question_number)

    def add_topic_to_question(self, course_id, year, semester, moed, question_number, question_topic):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).get_question(question_number).add_topic_to_question(question_topic)

    def remove_topic_from_question(self, course_id, year, semester, moed, question_number, question_topic):
        course = self.get_course(course_id)
        course.get_exam(year, semester, moed).get_question(question_number).remove_topic_from_question(question_topic)

    def search_question_by_specifics(self, course_id, year=None, semester=None, moed=None, question_number=None):
        course = self.get_course(course_id)
        return course.get_questions_by_specific(year, semester, moed, question_number)

    def get_questions_by_keywords(self, course_id, keywords):
        course = self.get_course(course_id)
        return course.get_questions_by_keywords(keywords)

    """--------------Comment functionality--------------"""

    # def remove_comment(self, course_id, year, semester, moed, question_number, comment_id):
    #     """
    #     Delegates Comment removal to the specified Exam and Question.
    #     """
    #     course = self.get_course(course_id)
    #     course.get_exam(year, semester, moed).get_question(question_number).remove_comment(comment_id)

    def get_link_to_question(self, course_id, year, semester, moed, question_number):
        course = self.get_course(course_id)
        return course.get_exam(year, semester, moed).get_question(question_number).get_link_to_question()

    def get_link_to_answer(self, course_id, year, semester, moed, question_number):
        course = self.get_course(course_id)
        return course.get_exam(year, semester, moed).get_question(question_number).get_link_to_answer()