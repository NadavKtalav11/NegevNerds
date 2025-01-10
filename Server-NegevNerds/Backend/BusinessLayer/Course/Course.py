import threading

from Backend.BusinessLayer.Course.Exam import Exam
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.Course.CourseRepository import CourseRepository
from Backend.DataLayer.CourseManagers.CourseManagersRepository import CourseManagersRepository
from Backend.DataLayer.CourseTopics.CourseTopicsRepository import CourseTopicsRepository
from Backend.DataLayer.Exam.ExamRepository import ExamRepository


class Course:
    def __init__(self, course_id, name, course_topics=None):
        self.course_id = course_id
        self.name = name
        self.course_topics = course_topics if course_topics is not None else set()  # Default to an empty list
        self.exams = {}  # Dictionary to store exams by years
        self.managers = set() # Dictionary to store managers with manager_id as key
        self.users = []  # List of users for the course

        self.course_topics_lock = threading.Lock()
        self.exams_lock = threading.Lock()
        self.managers_lock = threading.Lock()
        self.users_lock = threading.Lock()

    @classmethod
    def create(cls, course_id, name, course_topics=None):
        """
        Class method to create a new user and save to database
        Returns:
            User: Newly created user instance
        """
        course = cls(
            course_id=course_id,
            course_topics=course_topics,
            name=name
        )
        course_repository = CourseRepository()
        course_repository.add_course(course)
        topics_repo = CourseTopicsRepository()

        # for topic in course_topics:
        #     if not topics_repo.is_exist(topic=topic, course_id=course_id):
        #         topics_repo.add_Topic_to_course(course_id=course_id, topic=topic)
        return course

    # Getters
    def get_id(self):
        return self.course_id

    def get_exams_by_year(self, year):
        exam_repo = ExamRepository()
        return exam_repo.get_all_exams_by_year_and_course(year=year, course_id=self.course_id)

    def get_name(self):
        return self.name

    def get_syllabus(self):
        return self.syllabus

    def get_topics(self):
        with self.course_topics_lock:
            return self.course_topics

    def get_all_exams(self):
        """Retrieve all exams from the exams dictionary."""
        exam_repo = ExamRepository()
        return exam_repo.get_exam_by_course(course_id=self.course_id)

    def get_questions_by_specific(self, year=None, semester=None, moed=None, question_number=None):
        """Get specific questions."""
        question_dtos = []
        if year is None:
            all_exams = self.get_all_exams()
            if all_exams is not None:
                for exam in all_exams:
                    # Only include the questions that match the specific number
                    question_dtos.extend(exam.get_questions_by_specific(question_number))
        else:
            year_exams = self.get_exams_by_year(year)
            if year_exams is not None and len(year_exams) > 0:
                # year_exams = self.exams[year]
                if semester is None:
                    for exam in year_exams:
                        question_dtos.extend(exam.get_questions_by_specific(question_number))
                elif semester is not None and moed is None:
                    for exam in year_exams:
                        if exam.semester.__str__() == semester:
                            question_dtos.extend(exam.get_questions_by_specific(question_number))
                else:
                    exam = self.get_exam(year, semester, moed)
                    if exam is not None:
                        question_dtos.extend(exam.get_questions_by_specific(question_number))
        return question_dtos

    def get_questions_by_keywords(self, keywords):
        """get questions by keywords."""
        questions = []
        for exam in self.get_all_exams():
            questions = questions + exam.get_questions_by_keywords(keywords)
        return questions

    def get_exam(self, year, semester, moed, raise_exception=True):
        """
        Retrieves a specific exam by year, semester, and moed.
        Raises an exception if not found, unless raise_exception is False.
        """
        #with self.exams_lock:
        # Convert semester and moed to Enum
        semester = Semester(semester)
        moed = Moed(moed)

        if year in self.exams:
            for exam in self.exams[year]:
                if exam.semester == semester and exam.moed == moed:
                    return exam
        exam_repo = ExamRepository()
        exam = exam_repo.get_exam_by_date(year, semester, moed)
        if exam:
            if year not in self.exams:
                self.exams[year] = []  # Create a new list for this year if it doesn't exist
            self.exams[year].append(exam)
        return exam
        # if raise_exception:
        #     raise ExamIsNotExist(year, semester, moed)

    # This handles cases where the user didn't specify 'semester' or 'moed' in the search.
    def get_exams(self, year: int, semester=None, moed=None):
        """Fetch exams by year, and optionally filter by semester and moed."""
        with self.exams_lock:
            exams = []

            if year in self.exams:
                # Iterate through exams for the specified year
                for exam in self.exams[year]:
                    # Case 1: Neither semester nor moed specified
                    if semester is None and moed is None:
                        exams.append(exam)
                    # Case 2: Only moed specified
                    elif semester is None and moed is not None:
                        if exam.moed == moed:
                            exams.append(exam)
                    # Case 3: Only semester specified
                    elif semester is not None and moed is None:
                        if exam.semester == semester:
                            exams.append(exam)
                    # Case 4: Both semester and moed specified
                    elif exam.semester == semester and exam.moed == moed:
                        exams.append(exam)
            else:
                raise ExamIsNotExist(year, semester, moed)

            return exams

    def get_managers(self):
        with self.managers_lock:
            return self.managers

    def get_users(self):
        with self.users_lock:
            return self.users

    # Setters
    def set_syllabus(self, syllabus):
        self.syllabus = syllabus

    # Methods
    def add_course_topic(self, course_topic):
        """Add a topic to the course."""
        with self.course_topics_lock:
            if course_topic not in self.course_topics:
                self.course_topics.append(course_topic)
                course_topics_repo = CourseTopicsRepository()
                course_topics_repo.add_Topic_to_course(course_id=self.course_id, topic=course_topic)
            else:
                raise TopicAlreadyExist(course_topic)

    def remove_course_topic(self, course_topic):
        """Remove a topic from the course."""
        with self.course_topics_lock:
            if course_topic in self.course_topics:
                self.course_topics.remove(course_topic)
                course_topics_repo = CourseTopicsRepository()
                course_topics_repo.remove_topic_from_course(course_id=self.course_id, topic=course_topic)
            else:
                raise TopicNotFound(course_topic)

    def add_student(self, user_id):
        """Adds a student to the course."""
        with self.users_lock:
            if user_id not in self.users:
                self.users.append(user_id)
            else:
                raise UserAlreadyRegisterToCourse()

    def remove_student(self, user_id):
        """Removes a student from the course."""
        with self.users_lock:
            if user_id in self.users:
                self.users.remove(user_id)
                course_repo = CourseRepository()
                course_repo.update_course(self)
            else:
                raise UserIsNotRegisterToCourse()

    def generate_exam_id(self, year, semester, moed):
        return f"EXAM-{self.course_id}-{year}-{semester}-{moed}"

    def add_exam(self, year, semester, moed, link=""):
        """
        Adds an exam to the course.
        """
        with self.exams_lock:
            # Convert semester and moed to Enum
            semester = Semester(semester)
            moed = Moed(moed)

            exam = self.get_exam(year, semester, moed, raise_exception=False)
            if exam is None:
                exam_id = self.generate_exam_id(year=year,semester=semester.value,moed=moed.value)
                exam = Exam.create(exam_id=exam_id, course_id=self.course_id, link=link, year=year, semester=semester, moed=moed)
                if exam is not None:
                    if year not in self.exams:
                        self.exams[year] = []
                    self.exams[year].append(exam)
            else:
                raise ExamAlreadyExists(f"Exam with year={year}, semester={semester}, moed={moed} already exists.")

    def remove_exam(self, year, semester, moed):
        """Removes an exam from the course."""
        with self.exams_lock:
            exam = self.get_exam(year, semester, moed)
            if exam is not None:
                self.exams[year].remove(exam)
            else:
                raise ExamIsNotExist(year, semester, moed)

    def check_exam_full_pdf(self, year, semester, moed):
        """
        Checks if the full exam PDF exists and returns the result.
        
        Args:
            year (int): Year of the exam.
            semester (str): Semester of the exam.
            moed (str): Exam session.
        
        Returns:
            dict: Result indicating if the PDF link exists or not.
        
        Raises:
            ExamIsNotExist: If the exam does not exist.
        """
        exam = self.get_exam(year, semester, moed)  # Retrieve the exam
        if not exam:
            raise ExamIsNotExist(f"Exam for year {year}, semester {semester}, moed {moed} does not exist.")
        exam_pdf_link = exam.link  # Check for the exam link
        if exam_pdf_link != "":
            return {
                "status": "success",
                "message": "Exam PDF found.",
                "has_link": True,
                "link": exam_pdf_link
            }
        else:
            return {
                "status": "success",
                "message": "Exam PDF is not available.",
                "has_link": False
            }
    
    def checkExistSolution(self, year, semester, moed,question_number):
        exam = self.get_exam(year, semester, moed)  # Retrieve the exam
        if not exam:
            raise ExamIsNotExist(f"Exam for year {year}, semester {semester}, moed {moed} does not exist.")
        question = exam.get_question(question_number)
        question_answer_pdf_link = question.link_to_answer  # Check for the exam link
        if question_answer_pdf_link != "":
            return {
                "status": "success",
                "message": "Exam PDF found.",
                "has_link": True,
                "link": question_answer_pdf_link
            }
        else:
            return {
                "status": "success",
                "message": "Exam PDF is not available.",
                "has_link": False
            }
    
    
    def checkExistQuestion(self, year, semester, moed,question_number):
        exam = self.get_exam(year, semester, moed)  # Retrieve the exam
        if not exam:
            raise ExamIsNotExist(f"Exam for year {year}, semester {semester}, moed {moed} does not exist.")
        question = exam.get_question(question_number)
        question_details = question.generate_question_details_name()
        if not question:
            return False
        return question.id, question_details, question.link_to_question, question.link_to_answer
        
        
    def upload_full_exam_pdf(self, year, semester, moed, exam_path):
        exam = self.get_exam(year, semester, moed)
        if not exam:
            raise Exception(f"Exam for year {year}, semester {semester}, moed {moed} does not exist.")
        return exam.upload_full_exam_pdf(exam_path)

    
    def uploadSolution(self, year, semester, moed, question_number, answer_path_path):
        exam = self.get_exam(year, semester, moed)
        if not exam:
            raise Exception(f"Exam for year {year}, semester {semester}, moed {moed} does not exist.")
        question = exam.get_question(question_number)
        return question.uploadSolution(answer_path_path)
    
    def exist_manager(self, manager_id):
        manager_repo = CourseManagersRepository()
        return manager_id in self.managers or manager_repo.is_exist(user_id=manager_id, course_id=self.course_id)

    def add_manager(self, manager_id):
        """Adds a manager to the course."""
        with self.managers_lock:
            if not self.exist_manager(manager_id):
                self.managers.add(manager_id)
                manager_repo = CourseManagersRepository()
                manager_repo.add_manager_to_course(user_id=manager_id, course_id=self.course_id)
            else:
                raise ManagerAlreadyExists(manager_id)

    def remove_manager(self, manager_id):
        """Removes a manager from the course."""
        with self.managers_lock:
            if self.exist_manager(manager_id):
                self.managers.remove(manager_id)
                manager_repo = CourseManagersRepository()
                manager_repo.remove_manager_from_course(user_id=manager_id, course_id=self.course_id)
            else:
                raise ManagerIsNotExist(manager_id)

    def edit_exam_year(self, year, semester, moed, new_year):
        with self.exams_lock:
            exam = self.get_exam(year, semester, moed)
            if exam is not None:
                self.exams[year].remove(exam)
                if not self.exams[year]:  # Clean up empty lists
                    del self.exams[year]
                exam.edit_year(new_year)
                # Add the exam to the new year's list
                if new_year not in self.exams:
                    self.exams[new_year] = []
                self.exams[new_year].append(exam)
            else:
                raise ExamIsNotExist(year, semester, moed)

    # def check_valid_question(self, course_id,year,semester, moed, question_number,pdf_question):
    #     currExam = self.get_exam(year,semester,moed)
    #     if currExam is None:
    #         self.add_exam(self.name,pdf_question,  year, semester, moed)
    #         return True
    #     else:
    #         if currExam.semester == semester and currExam.moed == moed:
    #             return currExam.check_add_question_possibility(year, semester, moed, question_number,pdf_question )

    # def check_valid_question(self, course_id, year, semester, moed, question_number, pdf_question):
    #     # Get or create the exam
    #     currExam = self.get_exam(year, semester, moed)
    #     if currExam is None:
    #         # Create the exam if it doesn't exist
    #         self.add_exam(self.name, pdf_question, year, semester, moed)
    #         return True
    #     else:
    #         # Validate the question within the exam
    #         # if currExam.semester == semester and currExam.moed == moed:
    #         #     return currExam.check_add_question_possibility(year, semester, moed, question_number, pdf_question)
    #         # raise ValueError(f"No matching exam for semester {semester} and moed {moed}.")
    #         normalized_semester = Semester.get(currExam.semester, currExam.semester)
    #         normalized_moed = Moed.get(currExam.moed, currExam.moed)

    #         if normalized_semester == semester and normalized_moed == moed:
    #             return currExam.check_add_question_possibility(year, semester, moed, question_number, pdf_question)
    #         else:
    #             raise ValueError(f"Exam found, but mismatched semester {semester} or moed {moed}.")

    def check_valid_question(self, year, semester, moed, question_number, question_text):
        # Get or create the exam
        currExam = self.get_exam(year, semester, moed)
        if currExam is None:
            # Create the exam if it doesn't exist
            self.add_exam(year=year, semester=semester, moed=moed)
            return True
        else:
            # Compare normalized values
            if currExam.semester == semester and currExam.moed == moed:
                return currExam.check_add_question_possibility(year=year, semester=semester,moed=moed,question_number=question_number, question_text=question_text)
            else:
                raise ValueError(f"Exam found, but mismatched semester {semester} or moed {moed}.")

    def add_comment(self, year, semester, moed, question_number, writer_name, writer_id,prev_id, comment_text):
        """
        Add a Comment to specific question.
        """
        exam = self.get_exam(year, semester, moed)
        if exam is None:
            raise ExamIsNotExist
        question = exam.get_question(question_number)
        if question is None:
            raise QuestionNotFound
        return question.add_comment(writer_name, writer_id,prev_id, comment_text, False)


    def get_question_path(self, year, semester, moed, question_number):
        exam = self.get_exam(year=year,semester=semester,moed=moed)
        if exam is not None:
            return exam.get_question_path(question_number)
        else:
            raise ExamIsNotExist

    def get_answer_path(self, year, semester, moed, question_number):
        exam = self.get_exam(year=year,semester=semester,moed=moed)
        if exam is not None:
            return exam.get_answer_path(question_number)
        else:
            raise ExamIsNotExist
    def add_reaction(self, year, semester, moed, question_number, comment_id, user_id, emoji):
        """
        Add a reaction to specific question.
        """
        exam = self.get_exam(year, semester, moed)
        if exam is None:
            raise ExamIsNotExist
        question = exam.get_question(question_number)
        if question is None:
            raise QuestionNotFound
        return question.add_reaction(comment_id, user_id, emoji)

    def delete_comment(self, year, semester, moed, question_number, comment_id):
        """
        Add a reaction to specific question.
        """
        exam = self.get_exam(year, semester, moed)
        if exam is None:
            raise ExamIsNotExist
        question = exam.get_question(question_number)
        if question is None:
            raise QuestionNotFound
        question.delete_comment(comment_id)

    def remove_reaction(self, year, semester, moed, question_number, comment_id, reaction_id):
        """
        Add a reaction to specific question.
        """
        exam = self.get_exam(year, semester, moed)
        if exam is None:
            raise ExamIsNotExist
        question = exam.get_question(question_number)
        if question is None:
            raise QuestionNotFound
        question.remove_reaction(comment_id, reaction_id)

    def add_question(self, year, semester, moed, question_number,is_american,question_topics,pdf__question_path, pdf__answer_path, question_text):
        exam = self.get_exam(year, semester, moed)
        return exam.add_question(question_number, is_american, question_topics, pdf__question_path,
                                 pdf__answer_path, question_text)

