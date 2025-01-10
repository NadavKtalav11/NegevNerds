import threading
import uuid

from Backend.BusinessLayer.Course.Question import Question
from Backend.BusinessLayer.Course.enums import Moed, Semester
from Backend.BusinessLayer.Util.Exceptions import QuestionAlreadyInExam, QuestionDoesNotMeetExamFields, QuestionNotFound
from Backend.DataLayer.DTOs.ExamDTO import ExamDTO
from Backend.DataLayer.Exam.ExamRepository import ExamRepository
from Backend.DataLayer.Questions.QuestionRepository import QuestionRepository


class Exam:
    def __init__(self, exam_id, course_id, link, year, semester, moed):
        """
        Initialize an Exam instance.
        """
        self.id = exam_id
        self.course_id = course_id
        self.link = link
        self.year = year
        self.semester = Semester(semester)  # Ensuring semester is an Enum
        self.moed = Moed(moed)
        self.questions_list = {}  # <Question number, Question>

        self.questions_lock = threading.Lock()

    @classmethod
    def create(cls, exam_id, course_id, link, year , semester , moed):
        """
        Class method to create a new user and save to database
        Returns:
            User: Newly created user instance
        """
        exam = cls(
            exam_id=exam_id,
            course_id=course_id,
            link=link,
            year=year,
            semester=semester,
            moed=moed,
        )
        exam_repo = ExamRepository()
        exam_repo.add_exam(exam)
        return exam

    def to_dto(self):
        """
        Converts the Exam instance to an ExamDTO.
        :return: ExamDTO instance.
        """
        # Change this line to use 'to_dict' instead of 'to_dto' for questions
        question_dtos = [question.to_dict() for question in self.questions_list.values()]
        return ExamDTO(
            exam_id=self.id,
            course_id=self.course_id,
            link=self.link,
            year=self.year,
            semester=self.semester,
            moed=self.moed,
            questions_list=question_dtos,

        )

    def generate_question_id(self):
        return "question" + str(uuid.uuid4())

    def add_question(self,question_number,is_american,question_topics, pdf__question_path, pdf__answer_path , question_text):
        """
        Add a question to the exam.
        """
        with self.questions_lock:
            print("4.1.1_david")
            # Check if the fields match
            question = Question.create(exam_id=self.id, year=self.year, semester=self.semester, moed=self.moed,
                                       question_number=question_number, is_american=is_american,
                                       question_topics=question_topics, link_to_question=pdf__question_path,
                                       link_to_answer=pdf__answer_path, link_to_exam=self.link,
                                       question_id=self.generate_question_id(), question_text=question_text)

            if question is not None:
                self.questions_list[question_number] = question
            else :
                raise Exception("error while creating question")
            return question.id

    def check_add_question_possibility(self, year, semester, moed, question_number,question_text ):
        # Ensure exam details match
        if year != self.year or semester != self.semester or moed != self.moed:
            raise QuestionDoesNotMeetExamFields(question_number)

        # Ensure the question does not already exist
        #TODO
        question_repo = QuestionRepository()
        if question_repo.is_exist(year, semester.value, moed.value, question_text):
            raise QuestionAlreadyInExam(f"Question {question_number} already exists in this exam.")

        return True

    def get_question_path(self , question_number):
        question = self.get_question(question_number)
        if (question is None):
            raise QuestionNotFound
        return question.link_to_question

    def get_answer_path(self , question_number):
        question = self.get_question(question_number)
        if (question is None):
            raise QuestionNotFound
        return question.link_to_answer
    def get_all_exam_question(self):
        question_repo = QuestionRepository()
        return question_repo.get_question_by_exam_id(exam_id=self.id)


    def upload_full_exam_pdf(self, exam_path):
        try:
            # Update the in-memory link property
            self.link = exam_path

            # Update the record in the database
            exam_repo = ExamRepository()  # Assuming you have an ExamRepository for database operations
            exam_repo.update_exam_link(self.id, self.link)

            return {"status": "success", "message": "File uploaded successfully and database updated.", "link": self.link}
        except Exception as e:
            print(f"Error in Exam.upload_full_exam_pdf: {str(e)}")
            return {"status": "error", "message": str(e)}


    def remove_question(self, question_number):
        """
        Remove a question from the questions list if it exists.
        """
        with self.questions_lock:
            if question_number in self.questions_list:
                question_id = self.questions_list[question_number].id
                question_repo = QuestionRepository()
                question_repo.delete_question(question_id=question_id)
                del self.questions_list[question_number]  # Remove the question completely
            else:
                raise QuestionNotFound(question_number)

    def get_question(self, question_number):
        """
        Retrieve a question by its number.
        """
        with self.questions_lock:
            if question_number in self.questions_list:
                return self.questions_list[question_number]
            question_repo = QuestionRepository()
            question = question_repo.get_question_by_number(exam_id=self.id, question_number=question_number)
            if question is not None:
                self.questions_list[question_number] = question
            return question

    def get_questions_by_keywords(self, keywords):
        questions = []
        for keyword in keywords:
            for question in self.questions_list.values():
                if keyword in question.get_question_topics():
                    questions.append(question)
        return questions

    # def add_comment(self, question_number, comment_id, writer_name, prev_id, comment_text):
    #     """
    #     Add a Comment to the comments list of a specific question.
    #     """
    #     self.get_question(question_number).add_comment(comment_id, writer_name, prev_id, comment_text)

    # def remove_comment(self, question_number, comment_id):
    #     """
    #     Remove a Comment from the comments list of a specific question.
    #     """
    #     self.get_question(question_number).remove_comment(comment_id)
    
    # def edit_course_name(self, new_course_name):
    #     """Edit the course name."""
    #     self.course_name = new_course_name

    def edit_link(self, new_link):
        """Edit the exam link."""
        self.link = new_link

    def edit_year(self, new_year):
        """Edit the year of the exam."""
        if isinstance(new_year, int):
            self.year = new_year
        else:
            raise ValueError("Year must be an integer.")

    def edit_semester(self, new_semester):
        """Edit the semester of the exam."""
        try:
            if isinstance(new_semester, Semester):
                self.semester = new_semester
            else:
                self.semester = Semester(new_semester)
        except ValueError:
            # Raise a more descriptive error if the value is not valid
            raise ValueError(f"Invalid value for semester. Must be one of {[s.value for s in Semester]}.")

    def edit_moed(self, new_moed):
        """Edit the moed of the exam."""
        valid_moeds = {'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'}
        if new_moed in valid_moeds:
            self.moed = Moed(new_moed)
        else:
            raise ValueError("Invalid value for moed. Must be one of {'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'}.")

    def get_questions_by_specific(self, question_number=None):
        """
        Return list of questions dtos.
        """
        questions = []
        if question_number is None:
            for question in self.get_all_exam_question():
                questions.append(question.to_dto(course_id=self.course_id))
        else:
            question= self.get_question(question_number=question_number)
            if question is not None:
                questions.append(question.to_dto(course_id=self.course_id))
        return questions  # Will return an empty list if no question was found

    def __str__(self):
        """
        String representation of the Exam instance.
        """
        return (f"Exam(ID: {self.id}, Course: {self.course_id}, Year: {self.year}, "
                f"Semester: {self.semester}, Moed: {self.moed}, "
                f"Questions: {len(self.questions_list)})")