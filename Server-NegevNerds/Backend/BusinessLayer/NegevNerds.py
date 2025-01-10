import mimetypes

from Backend.BusinessLayer.Course.CourseFacade import CourseFacade
from Backend.BusinessLayer.Notifications.NotificationFacade import NotificationFacade
from Backend.BusinessLayer.PDFAnalyzer.FileManager import FileManager
from Backend.BusinessLayer.PDFAnalyzer.QuestionAnalyzer import QuestionAnalyzer
from Backend.BusinessLayer.User.UserFacade import UserFacade
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.BusinessLayer.PDFAnalyzer.PDFAnalyzerFacade import PDFAnalyzerFacade
from Backend.BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.CourseManagers.CourseManagersRepository import CourseManagersRepository
from Backend.DataLayer.Comment.CommentRepository import CommentRepository
from Backend.DataLayer.QuestionTopics.QuestionTopicsRepository import QuestionTopicsRepository
from Backend.DataLayer.WordsQuestions.WordsQuestionsRepository import WordsQuestionsRepository
from Backend.DataLayer.Questions.QuestionRepository import QuestionRepository
from Backend.DataLayer.Reaction.ReactionRepository import ReactionRepository





import threading
import os

class NegevNerds:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, mkdir):
        if cls._instance is None:
            with cls._lock:  # Ensure thread-safe instance creation
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
                    resolved_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), mkdir, "files"))
                    print(f"Resolved base directory for NegevNerds: {resolved_dir}")
                    #Initialize critical attributes in __new__
                    cls._instance._user_facade = UserFacade()
                    cls._instance._course_facade = CourseFacade()
                    cls._instance._pdfFacade = PDFAnalyzerFacade()
                    cls._instance._file_manager = FileManager(resolved_dir)
                    cls._instance._system_managers = []
                    cls._instance._initialized = True
                    cls._instance._notification_facade = NotificationFacade()
        return cls._instance

    def __init__(self, mkdir):
        # Prevent reinitialization
        if not hasattr(self, '_initialized'):
            resolved_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), mkdir, "files"))

            self._user_facade = UserFacade()
            self._course_facade = CourseFacade()
            self._pdfFacade = PDFAnalyzerFacade()
            self._file_manager = FileManager(resolved_dir)
            self._system_managers = []
            self._initialized = True
            self._notification_facade = NotificationFacade()

    # Getter methods for accessing the facades and file manager
    @property
    def userFacade(self):
        return self._user_facade

    @property
    def courseFacade(self):
        return self._course_facade

    @property
    def fileManager(self):
        return self._file_manager

    @property
    def system_managers(self):
        return self._system_managers


    def is_system_manager(self, user_id):
        """Checks if the user is a system manager."""
        return user_id in self.system_managers

    def register(self, email, password, password_confirm, first_name, last_name):
        try:
            return self.userFacade.register(email, password, password_confirm, first_name, last_name)
        except Exception as e:
            return None, {"Error": str(e)}  # Always return a tuple


    def registerWithoutAuth(self, email, password, first_name, last_name):
        """Register a new user."""
        try:
            return self.userFacade.registerWithoutAuth(email, password, first_name, last_name)

        except Exception as e:
            return f"Error: {e}"


    def register_authentication_part(self, email, auth_code):
        """Register a new user."""
        try:
            return self.userFacade.register_authentication_part(email, auth_code)
        except Exception as e:
            return f"Error: {e}"
        
    def register_termOfUse_part(self,email, password, first_name, last_name):
        """Register a new user."""
        try:
            return self.userFacade.register_termOfUse_part(email, password, first_name, last_name)
        except Exception as e:
            return f"Error: {e}"

    # def login(self, email, password):
    #     """Log the user in."""
    #     try:
    #         user_firstName, user_lastName, user_id, message = self.userFacade.login(email, password)
    #         return user_firstName, user_lastName, user_id, message  # Return the result from the facade
    #     except Exception as e:
    #         return f"Error: {e}"

    # def login(self, email, password):
    #     """Log the user in."""
    #     try:
    #         user_firstName, user_lastName, user_id, message = self.userFacade.login(email, password)
    #         return user_firstName, user_lastName, user_id, {"status": "success", "message": message}
    #     except Exception as e:
    #         # logging.error(f"Unexpected error during login: {str(e)}")
    #         return None, None, None, {"status": "error", "message": str(e)}
    
    def login(self, email, password):
        try:
            user_firstName, user_lastName, user_id, message = self.userFacade.login(email, password)
            if user_firstName is None or user_lastName is None or user_id is None:
                return None, None, None, {"status": "error", "message": "Incorrect email or password."}

            return user_firstName, user_lastName, user_id, {"status": "success", "message": message}
        except UserOrPasswordIncorrectError as e:
            # return None, None, None, {"status": "error", "message": "}
            return None, None, None, {"status": "error", "message": e.message}

        except Exception as e:
            return None, None, None, {"status": "error", "message": str(e)}



    def logout(self, user_id):
        """Log the user out."""
        try:
            result = self.userFacade.logout(user_id)
            return result  # Return the result from the facade
        except Exception as e:
            return f"Error: {e}"

    def edit_profile(self, email, **kwargs):
        """Edit the user's profile."""
        try:
            result = self.userFacade.editUserProfile(email, **kwargs)
            return result
        except Exception as e:
            return f"Error: {e}"

    def registerToCourse(self, course_id, user_id):
        """Add the user to course and add the course to user."""
        try:
            # Register the user to the course using Coursefacade
            self.courseFacade.register_to_course(course_id, user_id)
            # Register the course to the user using Userfacade
            self.userFacade.registerToCourse(course_id, user_id)
            print("User successfully registered to the course", user_id, course_id)
            return "User successfully registered to the course."
        except Exception as e:
            return f"Error: {e}"

    def removeStudentFromCourse(self, course_id, user_id):
        """Remove the user from the course and remove the course from user."""
        try:
            # Remove the user from the course using Coursefacade
            self.courseFacade.remove_student_from_course(course_id, user_id)
            # Remove the course from the user using Userfacade
            user = self.userFacade.getUser_by_id(user_id)
            if user:
                user.removeCourse(course_id)
            else:
                raise UserDoesnotExistsError(user_id)
            return "User successfully removed from the course."
        except Exception as e:
            return f"Error: {e}"

    def get_user_name(self, user_id):
        """Get the user full name."""
        try:
            result = self.userFacade.get_user_name(user_id)
            return result
        except Exception as e:
            print(f"Error in NegevNerds.get_user_name: {str(e)}")
            return {"status": "error", "message": str(e)}

    def open_course(self, user_id, course_id, name, syllabus_content_pdf):
        """Opens a new course in the system and saves the syllabus file."""
        try:
            # Check if the course already exists using CourseFacade
            if self.courseFacade.open_course_possibility(course_id, name):
                # Save the syllabus to the course folder using FileManager
                syllabus = self._pdfFacade.extract_syllabus_topic_total(syllabus_content_pdf)
                # syllabus_file_path = self.fileManager.save_syllabus_file(course_id, syllabus_content)
                # self.courseFacade.set_syllabus_of_course(course_id, syllabus_file_path)
                self.courseFacade.open_course(course_id,name,syllabus )
                self.courseFacade.add_manager_to_course(course_id, user_id)  # Add the user as a manager
                self.userFacade.registerToCourse(course_id, user_id)  # Add the user as a student
                return f"Course {name} opened successfully "
            else:
                raise Exception("Failed to create course.")
        except Exception as e:
            return f"Error: {e}"
    
    def check_exam_full_pdf(self, course_id, year, semester, moed):
        """Opens a new course in the system and saves the syllabus file."""
        try:
            return self.courseFacade.check_exam_full_pdf(course_id, year, semester, moed)
        except Exception as e:
            return f"Error: {e}"
    
    def checkExistSolution(self, course_id, year, semester, moed,question_number):
        """Opens a new course in the system and saves the syllabus file."""
        try:
            return self.courseFacade.checkExistSolution(course_id, year, semester, moed,question_number)
        except Exception as e:
            return f"Error: {e}"
    
    def get_exam_pdf_link(self, course_id, year, semester, moed):
        try:
            result = self.courseFacade.check_exam_full_pdf(course_id, year, semester, moed)
            return result
        except Exception as e:
            print(f"Error in NegevNerds.get_exam_pdf_link: {str(e)}")
            return {"status": "error", "message": str(e)}

    
    def upload_full_exam_pdf(self, course_id, year, semester, moed, pdf_file):
        try:
            exam_path = self._file_manager.save_exam_file1(course_id, year, semester, moed, pdf_file)
            result = self.courseFacade.upload_full_exam_pdf(course_id, year, semester, moed, exam_path)
            return {"status": "success", "message": "File uploaded and saved successfully.", "link": exam_path}
        except Exception as e:
            print(f"Error in NegevNerds.upload_full_exam_pdf: {str(e)}")
            return {"status": "error", "message": str(e)}
        
    def uploadSolution(self, course_id, year, semester, moed, question_number,solution_file):
        try:
            answer_path = ""
            if solution_file is not None:
                if self.is_photo(answer_path):
                    answer_path = self.fileManager.save_photo_answer_file(
                        course_id=course_id,
                        year=year,
                        semester=semester,
                        moed=moed,
                        question_number=question_number,
                        photo_file=solution_file
                    )
                else:
                    answer_path = self.fileManager.save_answer_file_pdf(
                        course_id=course_id,
                        year=year,
                        semester=semester,
                        moed=moed,
                        question_number=question_number,
                        pdf_answer=solution_file
                    )
            result = self.courseFacade.uploadSolution(course_id, year, semester, moed, question_number, answer_path)
            return {"status": "success", "message": "File uploaded and saved successfully.", "link": answer_path}
        except Exception as e:
            print(f"Error in NegevNerds.upload_full_exam_pdf: {str(e)}")
            return {"status": "error", "message": str(e)}

    def remove_course(self, course_id, user_id):
        """Remove an existing course from the system and delete its corresponding folder."""
        try:
            # Check if the user is a system manager or the course manager
            if self.is_system_manager(user_id) or self.courseFacade.is_course_manager(course_id, user_id):
                # Remove the course using CourseFacade
                if self.courseFacade.remove_course(course_id):
                    # Delete the course folder using FileManager
                    self.fileManager.delete_course_folder(course_id)
                    return f"Course {course_id} removed successfully."
                else:
                    raise Exception("Failed to remove course.")
            else:
                raise UserIsNotCourseManager(course_id)
        except Exception as e:
            return f"Error: {e}"

    def search_exam_by_specifics(self, course_id, year: int, semester=None, moed=None):
        """Search for exams by course ID and optionally filter by year, semester, and moed."""
        try:
            # Fetch all exams for the course from coursefacade
            exams = self.courseFacade.search_exam_by_specifics(course_id, year, semester, moed)
            return exams
        except Exception as e:
            raise Exception(f"Failed to search exams: {e}")

    def search_all_course_exams(self, course_id):
        """Search for all the exams in the system for specific course"""
        try:
            # Fetch all exams for the course from coursefacade
            exams = self.courseFacade.search_all_course_exams(course_id)
            return exams
        except Exception as e:
            raise Exception(f"Failed to search exams: {e}")

    def edit_exam_course_name(self, course_id, year, semester, moed, new_course_name):
        """Editing exam's course name """
        try:
            self.courseFacade.edit_exam_course_name(course_id, year, semester, moed, new_course_name)
            return "The exams' course name was updated successfully."
        except Exception as e:
            raise Exception(f"Failed to edit exam's course name {e}")

    def edit_exam_link(self, course_id, year, semester, moed, new_link):
        """Editing exam's link """
        try:
            self.courseFacade.edit_exam_link(course_id, year, semester, moed, new_link)
            return "The exams' link was updated successfully."
        except Exception as e:
            raise Exception(f"Failed to edit exam's link {e}")

    def edit_exam_year(self, course_id, year, semester, moed, new_year):
        """Editing exam's year """
        try:
            self.courseFacade.edit_exam_year(course_id, year, semester, moed, new_year)
            return "The exams' year was updated successfully."
        except Exception as e:
            raise Exception(f"Failed to edit exam's link {e}")

    def edit_exam_semester(self, course_id, year, semester, moed, new_semester):
        """Editing exam's semester """
        try:
            self.courseFacade.edit_exam_semester(course_id, year, semester, moed, new_semester)
            return "The exams' semester was updated successfully."
        except Exception as e:
            raise Exception(f"Failed to edit exam's link {e}")

    def edit_exam_moed(self, course_id, year, semester, moed, new_moed):
        """Editing exam's moed """
        try:
            self.courseFacade.edit_exam_moed(course_id, year, semester, moed, new_moed)
            return "The exams' moed was updated successfully."
        except Exception as e:
            raise Exception(f"Failed to edit exam's link {e}")

    def get_question_path(self, course_id, year, semester, moed, question_number):
        try:
            return self.courseFacade.get_link_to_question(course_id, year, semester, moed, question_number)
        except (CourseIsNotExist, ExamIsNotExist) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to get path: {e}")

    def get_answer_path(self, course_id, year, semester, moed, question_number):
        try:
            return self.courseFacade.get_link_to_answer(course_id, year, semester, moed, question_number)
        except (CourseIsNotExist, ExamIsNotExist) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to get path: {e}")

    def add_comment(self, course_id, year, semester, moed, question_number, writer_name, writer_id,prev_id,
                    comment_text):
        """
                Add a comment to a question discussion.
        """
        try:
            comment_writers = self.courseFacade.add_comment(course_id=course_id, year=year, semester=semester,
                                                           moed=moed, question_number=question_number,
                                                          writer_name=writer_name, 
                                                          writer_id=writer_id,prev_id=prev_id, comment_text=comment_text)
            for commenter in comment_writers:
                self._notification_facade.send_notification(sender_id=writer_id, receiver_id=commenter,message=f"{writer_id}- add comment in discussion which you take part in the past", need_approval=False)
            return "Comment added successfully."
        except (CourseIsNotExist, ExamIsNotExist, QuestionNotFound) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to add comment: {e}")

    def add_reaction(self, course_id, year, semester, moed, question_number, comment_id, user_id, emoji):
        """
            Add a reaction to a comment.
        """
        try:
            receiver_id = self.courseFacade.add_reaction(course_id=course_id, year=year, semester=semester,
                                          moed=moed, question_number=question_number,
                                          comment_id=comment_id, user_id=user_id, emoji=emoji)

            self._notification_facade.send_notification(sender_id=user_id, receiver_id=receiver_id ,message= f"{user_id} add reaction to your comment- {comment_id}", need_approval=False )
            return "Reaction added successfully."
        except (CourseIsNotExist, ExamIsNotExist, QuestionNotFound, CommentNotFound) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to add reaction: {e}")

    def remove_reaction(self, course_id, year, semester, moed, question_number, comment_id, reaction_id):
        """
            Remove a reaction from a comment.
        """
        try:
            self.courseFacade.remove_reaction(course_id=course_id, year=year, semester=semester,
                                          moed=moed, question_number=question_number,
                                          comment_id=comment_id, reaction_id=reaction_id)
            return "Reaction removed successfully."
        except (CourseIsNotExist, ExamIsNotExist, QuestionNotFound, CommentNotFound, ReactionNotFound) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to remove reaction: {e}")

    def is_photo(self, file):
        """
        Check if the given file is a valid photo (JPEG, JPG, PNG).

        :param file: The uploaded file object.
        :return: True if the file is a valid photo, False otherwise.
        """
        if file:
            # Get the MIME type of the file
            mime_type, _ = mimetypes.guess_type(file.filename)
            # Allowed photo MIME types
            allowed_photo_types = {"image/jpeg", "image/png"}  # Covers JPG, JPEG, and PNG
            return mime_type in allowed_photo_types
        return False


    def search_free_text(self , text, course_id = None):
        if course_id is None:
            search_dtos = self._pdfFacade.search_free_text(text=text)
            ques_dtos = self.courseFacade.get_questions_dto_by_search_dtos(dtos=search_dtos)
            return ques_dtos
        else:
            ids = self._pdfFacade.search_free_text_from_course(text=text, course_id=course_id)
            dtos = self.courseFacade.get_questions_dto_by_ids(ids, course_id)
            return dtos





    def add_question(self, course_id, year, semester, moed, question_number, is_american, question_topics,  question_file, answer_file):
        """
        Add a question to a course exam with an associated PDF file.

        ining question details.
        :return: Path to the saved PDF file.
        """
        try:
            # Get course name for filename generation
            question_analyzer = QuestionAnalyzer()
            if self.is_photo(question_file):
                question_text= question_analyzer.extract_text_from_image(question_file)
            else:
                question_text = question_analyzer.extract_text_from_pdf_file(question_file)
            if self.courseFacade.check_valid_question(course_id=course_id,year=year,semester=semester, moed=moed, question_number=question_number,question_text=question_text):
                # Save the PDF file with a custom name
                print(f"Base directory: {self.fileManager._base_dir}")

                if self.is_photo(question_file):
                    question_path= self.fileManager.save_photo_question_file(
                        course_id=course_id,
                        year=year,
                        semester=semester,
                        moed=moed,
                        question_number=question_number,
                        photo_file=question_file
                    )

                else :
                    question_path = self.fileManager.save_question_file_pdf(
                        course_id=course_id,
                        year=year,
                        semester=semester,
                        moed=moed,
                        question_number=question_number,
                        pdf_question=question_file
                    )
                answer_path = ""
                if answer_file is not None:
                    if self.is_photo(answer_file):
                        answer_path = self.fileManager.save_photo_answer_file(
                            course_id=course_id,
                            year=year,
                            semester=semester,
                            moed=moed,
                            question_number=question_number,
                            photo_file=answer_file
                        )
                    else:
                        answer_path = self.fileManager.save_answer_file_pdf(
                            course_id=course_id,
                            year=year,
                            semester=semester,
                            moed=moed,
                            question_number=question_number,
                            pdf_answer=answer_file
                        )
                # Add the question to the course
                question_id = self.courseFacade.add_question(course_id=course_id, year=year, semester=semester, moed=moed,
                                                             question_number=question_number,is_american=is_american,
                                                             question_topics=question_topics,pdf_question_path=question_path, pdf_answer_path=answer_path, question_text=question_text)
                if self.is_photo(question_file):
                    self._pdfFacade.perform_information_retrival_question_photo(text=question_text, question_id=question_id, course_id = course_id)
                else:
                    self._pdfFacade.perform_information_retrival_question_pdf(pdf_question_path=question_path,question_id=question_id, course_id = course_id)

            return "Question added successfully."
        except (CourseIsNotExist, ExamIsNotExist, TopicNotFound, QuestionAlreadyInExam) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to add question with PDF: {e}")
        
    def is_user_manager(self, course_id, user_id):
        """Delegates to CourseManagersRepository to check if user is a course manager."""
        try:
            course_managers_repo = CourseManagersRepository()
            # return course_managers_repo.is_user_manager(course_id, user_id)
            return course_managers_repo.is_exist(course_id, user_id)
        except Exception as e:
            raise Exception(f"Error in NegevNerds.is_user_manager: {str(e)}")
    
    def get_comments_metadata(self, question_id):
        try:         
            comment_repo = CommentRepository()
            comments_metaData = comment_repo.get_comments_metadata_by_question_id(question_id)
            return comments_metaData
        except Exception as e:
            raise Exception(f"Error in NegevNerds delete_question: {str(e)}")

    def delete_question(self, course_id, year, semester, moed, question_number):
        """
        Deletes a question from the course, ensuring all related data is removed.
        """
        try:
            # Get the course and ensure it exists
            question_id, question_details, pathQuestion, pathAnswer = self.courseFacade.checkExistQuestion(course_id, year, semester, moed, question_number)
            if not question_id:
                raise Exception(
                    f"Question {question_number} does not exist in the exam for course {course_id}, "
                    f"Year: {year}, Semester: {semester}, Moed: {moed}."
                )           
            comment_repo = CommentRepository()
            comments_Ids = comment_repo.get_comment_ids_by_question_id(question_id)
            reactions_repo = ReactionRepository()
            reactions_repo.delete_reactions_by_comment_ids(comments_Ids)
            comment_repo.delete_comments_by_question_id(question_id)
            words_questions_repo = WordsQuestionsRepository()
            words_questions_repo.delete_question_words_from_all_tables(question_id)
            question_topics_repo = QuestionTopicsRepository()
            question_topics_repo.delete_topics_by_question_id(question_id)
            question_repo = QuestionRepository()
            question_repo.delete_question(question_id)
            self.fileManager.delete_file(pathQuestion)
            if pathAnswer != "":
                self.fileManager.delete_file(pathAnswer)

        except Exception as e:
            raise Exception(f"Error in NegevNerds delete_question: {str(e)}")

    def delete_comment(self, course_id, year, semester, moed, question_number, comment_id):
        """
            delete comment.
        """
        try:
            self.courseFacade.delete_comment(course_id=course_id, year=year, semester=semester,
                                           moed=moed, question_number=question_number,
                                           comment_id=comment_id)
            return "Comment deleted successfully."
        except (CourseIsNotExist, ExamIsNotExist, QuestionNotFound, CommentNotFound) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to delete comment: {e}")

    # def delete_comment(self, comment_id):
    #     """
    #     Deletes a comment from the question, ensuring all related data is removed.
    #     """
    #     try:
    #         # Get the course and ensure it exists
    #         # question_id, question_details = self.courseFacade.checkExistQuestion(course_id, year, semester, moed, question_number)
    #         # if not question_id:
    #         #     raise Exception(
    #         #         f"Question {question_number} does not exist in the exam for course {course_id}, "
    #         #         f"Year: {year}, Semester: {semester}, Moed: {moed}."
    #         #     )
    #         reactions_repo = ReactionRepository()
    #         reactions_repo.delete_reactions_by_comment_id(comment_id)
    #         comment_repo = CommentRepository()
    #         replies_to_comment = comment_repo.get_replies_by_comment_id(comment_id)
    #         comment_prev = comment_repo.get_prev_id_by_comment_id(comment_id)
    #         comment_repo.update_replies_prev_id(replies_to_comment, comment_prev)
    #         comment_repo.delete_comment(comment_id)
    #
    #
    #     except Exception as e:
    #         raise Exception(f"Error in NegevNerds delete_question: {str(e)}")



    def get_user_courses(self, user_id):
        courses_ids = self.userFacade.get_user_courses(user_id)
        return self._course_facade.get_courses_DTO(courses_ids)

    def get_course_topics(self, course_id):
        return self._course_facade.get_course_topics(course_id)

    def get_all_courses(self):
        return self._course_facade.get_all_courses()

    def get_course(self, course_id):
        return self._course_facade.get_course_DTO(course_id)

    # def add_question(self, course_id, year, semester, moed, questionDTO):
    #     """Adds a question to an exam in the specified course.
    #     If the exam does not exist, it creates a new one."""
    #     try:
    #         self.coursefacade.add_question(
    #             course_id, year, semester, moed, questionDTO)
    #         return "Question added successfully."
    #     except Exception as e:
    #         raise Exception(f"Failed to add question: {e}")

    def upload_answer(self, course_id, year, semester, moed, question_number, pdf_answer):
        try:
            if self.is_photo(pdf_answer):
                self.fileManager.save_photo_answer_file(
                    course_id,
                    year,
                    semester,
                    moed,
                    question_number,
                    pdf_answer
                )
            else:
                self.fileManager.save_answer_file_pdf(
                    course_id,
                    year,
                    semester,
                    moed,
                    question_number,
                    pdf_answer
                )
            return "Answer added successfully to the question."
        except (CourseIsNotExist, ExamIsNotExist) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to upload answer: {e}")



    def search_question_by_specifics(self, course_id, year=None, semester=None, moed=None, question_number=None):
        """Search for questions based on the provided specifics for the course."""
        try:
            print(
                f"Received data: {{'course_id': '{course_id}', 'year': '{year}', 'semester': '{semester}', 'moed': '{moed}', 'question_number': '{question_number}'}}")

            # Fetch questions based on the specifics from the course
            questions = self._course_facade.search_question_by_specifics(course_id,year, semester, moed, question_number)

            print(f"Found questions: {questions}")

            return questions
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise Exception(f"Failed to search questions: {e}")

    def get_user_notifications(self, user_id):
        """Search for questions based on the provided specifics for the course."""
        # try:

            # Fetch questions based on the specifics from the course
        notifications = self._notification_facade.get_user_notifications(user_id)
        return notifications

        # except Exception as e:
        #     print(f"Error occurred: {str(e)}")
        #     raise Exception(f"Failed to search questions: {e}")

    def get_user_last_notifications(self, user_id, number_of_notifications):
        """Search for questions based on the provided specifics for the course."""
        # try:

            # Fetch questions based on the specifics from the course
        notifications = self._notification_facade.get_user_last_notifications(user_id=user_id, number_of_notifications=number_of_notifications)
        return notifications
        # except Exception as e:
        #     print(f"Error occurred: {str(e)}")
        #     raise Exception(f"Failed to search questions: {e}")


