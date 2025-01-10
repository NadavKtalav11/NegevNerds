import json
from Backend.BusinessLayer import NegevNerds


import threading

from Backend.BusinessLayer.Course import enums
from Backend.DataLayer.DTOs.QuestionDTO import QuestionDTO



class ServiceLayer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, negev_nerds: NegevNerds):
        if cls._instance is None:
            with cls._lock:  # Ensure thread-safe instance creation
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
                    # Initialize attributes in __new__
                    cls._instance.negev_nerds = negev_nerds
                    cls._instance._initialized = True
        return cls._instance

    def __init__(self, negev_nerds: NegevNerds = None):
        # Prevent reinitialization
        if not hasattr(self, '_initialized'):
            if negev_nerds is None:
                negev_nerds = NegevNerds.NegevNerds("../")
            self.negev_nerds = negev_nerds
            self._initialized = True
            
    def register(self, email, password, password_confirm, first_name, last_name):
        try:
            password, result = self.negev_nerds.register(email, password, password_confirm, first_name, last_name)

            if "Error" in result:
                return {
                    "status": "error",
                    "message": result["Error"]
                }
            return {
                "status": "success",
                "message": result.get("message", "Registration successful"),
                "password": password
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

        
        

    def registerWithoutAuth(self, email, password, first_name, last_name):
        """Handle user registration and return JSON."""
        user_id = None
        try:
            user_id, result = self.negev_nerds.registerWithoutAuth(email, password, first_name, last_name)

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })
            return user_id, json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return user_id, json.dumps({
                "status": "error",
                "message": str(e)
            })
    
    def register_authentication_part(self, email, auth_code):
        """Handle user authentication code part in the registration and return JSON."""
        try:
            result = self.negev_nerds.register_authentication_part(email, auth_code)

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
        
    def register_termOfUse_part(self, email, password, first_name, last_name):
        """Handle user acception of the term of use in the registration and return JSON."""
        try:
            userid ,result = self.negev_nerds.register_termOfUse_part(email, password, first_name, last_name)

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result,
                    "user_id": userid
            
                })
            return json.dumps({
                "status": "success",
                "message": result,
                "user_id": userid

            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

        
    # def login(self, email, password):
    #     """Handle user login and return JSON."""
    #     try:
    #         user_firstName, user_lastName, user_id, message = self.negev_nerds.login(email, password)

    #         return json.dumps({
    #             "status": "success",
    #             "message": message,  # Pass the string message
    #             "user_id": user_id,
    #             "first_name": user_firstName,
    #             "last_name": user_lastName
    #         })
    #     except Exception as e:
    #         return json.dumps({
    #             "status": "error",
    #             "message": str(e)
    #         })
    def login(self, email, password):
        try:
            user_firstName, user_lastName, user_id, result = self.negev_nerds.login(email, password)

            if result.get("status") == "error" or user_firstName is None or user_id is None:
                return json.dumps({
                    "status": "error",
                    "message": result["message"],
                    "user_id": None
                })

            return json.dumps({
                "status": "success",
                "message": result["message"],
                "user_id": user_id,
                "first_name": user_firstName,
                "last_name": user_lastName
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e),
                "user_id": None
            })



    # def login(self, email, password):
    #     """Handle user login and return JSON."""
    #     try:
    #         user_firstName, user_lastName, userid, result = self.negev_nerds.login(email, password)

    #         if result.get('status') == 'error':
    #             return json.dumps({
    #                 "status": "error",
    #                 "message": result['message'],
    #                 "user_id": None

    #             })
    #         return json.dumps({
    #             "status": "success",
    #             "message": result,
    #             "user_id": userid,
    #             "first_name": user_firstName,
    #             "last_name":user_lastName
                

    #         })
        # except Exception as e:
        #     return json.dumps({
        #         "status": "error",
        #         "message": str(e)
        #     })

    def logout(self, user_id):
        """Handle user logout and return JSON."""
        try:
            result = self.negev_nerds.logout(user_id)

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })



    def register_to_course(self, course_id, user_id):
        """Handle user registration to a course and return JSON response."""
        try:
            result = self.negev_nerds.registerToCourse(course_id, user_id)

            # If result contains "Error", return it in the JSON response
            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })

            # Return the success message in JSON format
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            # In case of exception, return the error message
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def remove_student_from_course(self, course_id, user_id):
        """Handle removing a user from a course and return JSON response."""
        try:
            result = self.negev_nerds.removeStudentFromCourse(course_id, user_id)

            # If result contains "Error", return it in the JSON response
            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })

            # Return the success message in JSON format
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            # In case of exception, return the error message
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def open_course(self, user_id, course_id, course_name, syllabus_content_pdf):
        """Handle course creation and save syllabus, return JSON response."""
        try:
            result = self.negev_nerds.open_course(user_id, course_id, course_name, syllabus_content_pdf )

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })

            return json.dumps({
                "status": "success",
                "message": result
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def remove_course(self, course_id, user_id):
        """Handle course removal and return JSON response."""
        try:
            result = self.negev_nerds.remove_course(course_id, user_id)

            if "Error" in result:
                return json.dumps({
                    "status": "error",
                    "message": result
                })
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })


    def search_free_text(self, text, course_id =None):
        """Handle user logout and return JSON."""
        try:
            result = self.negev_nerds.search_free_text(text=text, course_id=course_id)

            questions_dict = [question.to_dict() for question in result]

            if not questions_dict:
                return json.dumps({
                    "status": "error",
                    "message": "No questions found for the given criteria."
                })

            return json.dumps({
                "status": "success",
                "message": questions_dict
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })


    def search_question_by_specifics(self, course_id, year=None, semester=None, moed=None, question_number=None):
        """Search for questions by specific criteria."""
        try:
            result = self.negev_nerds.search_question_by_specifics(course_id, year, semester, moed, question_number)
            print(result)

            questions_dict = [question.to_dict() for question in result]

            if not questions_dict:
                return json.dumps({
                    "status": "error",
                    "message": "No questions found for the given criteria."
                })

            return json.dumps({
                "status": "success",
                "data": questions_dict  # מחזירים את רשימת השאלות כ-JSON
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def search_exam_by_specifics(self, course_id, year: int, semester=None, moed=None):
        """Search for exams by course ID and optionally filter by year, semester, and moed. Return JSON."""
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.search_exam_by_specifics(course_id, year, semester, moed)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "No exams found for the given criteria."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def search_all_course_exams(self, course_id):
        """Search for exams by course ID and optionally filter by year, semester, and moed. Return JSON."""
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.search_all_course_exmas(course_id)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "No exams found for the given criteria."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def edit_exam_course_name(self, user_id, course_id, year, semester, moed, new_course_name):
        """Editing exam's course name """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.edit_exam_course_name(user_id, course_id, year, semester, moed, new_course_name)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "Something went wrong"
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def edit_exam_link(self, course_id, year, semester, moed, new_link):
        """Editing exam's link """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.edit_exam_link(course_id, year, semester, moed, new_link)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "Something went wrong."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def edit_exam_year(self, course_id, year, semester, moed, new_year):
        """Editing exam's year """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.edit_exam_year(course_id, year, semester, moed, new_year)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "Something went wrong."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def edit_exam_semester(self, course_id, year, semester, moed, new_semester):
        """Editing exam's semester """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.edit_exam_semester(course_id, year, semester, moed, new_semester)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "Something went wrong."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def edit_exam_moed(self, course_id, year, semester, moed, new_moed):
        """Editing exam's moed """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.edit_exam_moed(course_id, year, semester, moed, new_moed)

            # Check if any exams are found
            if not result:
                return json.dumps({
                    "status": "error",
                    "message": "Something went wrong."
                })
            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def add_comment(self, course_id, year, semester, moed, question_number,
                     writer_name,
                     writer_id
                     , prev_id,
                     comment_text):
        """
        Handles adding a comment to a question discussion.
        :return: JSON response indicating success or failure.
        """
        try:

            result = self.negev_nerds.add_comment(course_id, year, semester, moed, question_number,
                                                  writer_name,writer_id, prev_id, comment_text)
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def add_reaction(self, course_id, year, semester, moed, question_number, comment_id, user_id, emoji):
        """
        Handles adding a reaction to a comment.
        :return: JSON response indicating success or failure.
        """
        try:
            result = self.negev_nerds.add_reaction(course_id, year, semester, moed, question_number,
                                                  comment_id, user_id, emoji)
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
        
    def get_comments_metadata(self, question_id):
        """
        Fetch metadata for all comments of a question.
        :param question_id: ID of the question.
        :return: JSON string with success or error message.
        """
        try:
            result = self.negev_nerds.get_comments_metadata(question_id)
            return json.dumps({
                "status": "success",
                "message": result  # List of metadata dictionaries
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })


    def remove_reaction(self, course_id, year, semester, moed, question_number, comment_id, reaction_id):
        """
        Handles removing a reaction from a comment.
        :return: JSON response indicating success or failure.
        """
        try:

            result = self.negev_nerds.remove_reaction(course_id, year, semester, moed, question_number,
                                                  comment_id, reaction_id)
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def add_question(self, course_id, year, semester, moed, question_number, is_american,
                     question_topics
                     ,question_file,
                     answer_file = None):
        """
        Handles adding a question to an exam.
        :return: JSON response indicating success or failure.
        """
        try:
            
            result = self.negev_nerds.add_question(course_id, year, semester, moed, question_number
                                                   ,is_american,question_topics, question_file,answer_file )
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
    
    

    def upload_answer(self, course_id, year, semester, moed, questionNumber, pdf_answer):
        """
        Handles uploading an answer to an existing question.
        :return: JSON response indicating success or failure.
        """
        try:

            result = self.negev_nerds.upload_answer(course_id, year, semester, moed, questionNumber, pdf_answer)
            return json.dumps({
                "status": "success",
                "message": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_question_path(self, course_id, year, semester, moed, questionNumber):
        try:
            return self.negev_nerds.get_question_path(course_id, year, semester, moed, questionNumber)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
    
    def is_user_manager(self, course_id, user_id):
        """Service layer to check if the user is a course manager."""
        try:
            return self.negev_nerds.is_user_manager(course_id, user_id)
        except Exception as e:
            raise Exception(f"Service layer error in is_user_manager: {str(e)}")

    def get_answer_path(self, course_id, year, semester, moed, questionNumber):
        try:
            return self.negev_nerds.get_answer_path(course_id, year, semester, moed, questionNumber)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def delete_question(self, course_id, year, semester, moed, question_number):
        """
        Deletes a specific question from the course and its related data.
        """
        try:
            # Call the NegevNerds logic to delete the question
            self.negev_nerds.delete_question(course_id, year, semester, moed, question_number)
            return json.dumps({
                "status": "success",
                "message": "Question deleted successfully."
            })
        except Exception as e:
            # Handle errors and return an error response
            return json.dumps({
                "status": "error",
                "message": str(e)
            })
        
    def delete_comment(self, course_id, year, semester, moed, question_number, comment_id):
        """
        Deletes a specific comment from the question and its related data.
        """
        try:
            # Call the NegevNerds logic to delete the question
            self.negev_nerds.delete_comment(course_id, year, semester, moed, question_number, comment_id)
            return json.dumps({
                "status": "success",
                "message": "Question deleted successfully."
            })
        except Exception as e:
            # Handle errors and return an error response
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_user_courses(self, user_id):
        """Editing exam's year """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.get_user_courses(user_id)

            result_dict = [dto.to_dict() for dto in result]

            print(f"Courses result from NegevNerds: {result_dict}")  # לוג להראות מה חזר

            return json.dumps({
                "status": "success",
                "data": result_dict
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_user_name(self, user_id):
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.get_user_name(user_id)

            print(f"name result from NegevNerds: {result}")  # לוג להראות מה חזר

            return json.dumps({
                "status": "success",
                "data": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_course_topics(self, course_id):
        """Editing exam's year """
        try:
            # Call the business layer method with the provided arguments
            result = self.negev_nerds.get_course_topics(course_id)

            print("res", result)
            return json.dumps({
                "status": "success",
                "data": list(result)
            }, ensure_ascii= False)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_all_courses(self):
        """Fetches all courses and returns them in JSON format."""
        try:
            # Call the business layer to get the list of courses
            courses = self.negev_nerds.get_all_courses()

            # Return the result as a dictionary, serialized to JSON
            return json.dumps({
                "status": "success",
                "data": [course.to_dict() for course in courses]
            })
        except Exception as e:
            # Return an error response as a JSON string
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_course(self, course_id):
        """Fetches all courses and returns them in JSON format."""
        try:
            # Call the business layer to get the course
            course = self.negev_nerds.get_course(course_id)

            # Return the result as a dictionary, serialized to JSON
            return json.dumps({
                "status": "success",
                "data": course.to_dict()
            })
        except Exception as e:
            # Return an error response as a JSON string
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_user_notifications(self, user_id):
        """Fetches all courses and returns them in JSON format."""
        try:
            # Call the business layer to get the course
            notifications = self.negev_nerds.get_user_notifications(user_id=user_id)

            notifications_dict = [notifications.to_dict() for notification in notifications]
            # Return the result as a dictionary, serialized to JSON
            return json.dumps({
                "status": "success",
                "data": notifications_dict
            })
        except Exception as e:
            # Return an error response as a JSON string
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def get_user_last_notifications(self, user_id, number_of_notifications):
        """Fetches all courses and returns them in JSON format."""
        try:
            # Call the business layer to get the course
            notifications = self.negev_nerds.get_user_last_notifications(user_id=user_id, number_of_notifications=number_of_notifications)

            notifications_dict = [notifications.to_dict() for notification in notifications]
            # Return the result as a dictionary, serialized to JSON
            return json.dumps({
                "status": "success",
                "data": notifications_dict
            })
        except Exception as e:
            # Return an error response as a JSON string
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    def check_exam_full_pdf(self, course_id, year, semester, moed):
        
        try:
            # Call the Negev Nerds business logic to check for the exam
            result = self.negev_nerds.check_exam_full_pdf(course_id, year, semester, moed)

            # Parse the result from the Negev Nerds logic
            if result.get("status") == "success":
                return json.dumps({
                    "status": "success",
                    "message": result.get("message", "Operation successful."),
                    "has_link": result.get("has_link"),
                    "link": result.get("link", None)
                })
            else:
                # Handle known failures returned by Negev Nerds
                return json.dumps({
                    "status": "error",
                    "message": result.get("message", "Unknown error occurred.")
                })

        except Exception as e:
            # Handle unexpected errors gracefully
            print(f"Error in check_exam_full_pdf: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": "An unexpected error occurred.",
                "error": str(e)
            })
        
    def checkExistSolution(self, course_id, year, semester, moed,question_number):
        
        try:
            # Call the Negev Nerds business logic to check for the exam
            result = self.negev_nerds.checkExistSolution(course_id, year, semester, moed,question_number)

            # Parse the result from the Negev Nerds logic
            if result.get("status") == "success":
                return json.dumps({
                    "status": "success",
                    "message": result.get("message", "Operation successful."),
                    "has_link": result.get("has_link"),
                    "link": result.get("link", None)
                })
            else:
                # Handle known failures returned by Negev Nerds
                return json.dumps({
                    "status": "error",
                    "message": result.get("message", "Unknown error occurred.")
                })

        except Exception as e:
            # Handle unexpected errors gracefully
            print(f"Error in check_exam_full_pdf: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": "An unexpected error occurred.",
                "error": str(e)
            })
        
    def upload_full_exam_pdf(self, course_id, year, semester, moed, pdf_file):
        try:
            result = self.negev_nerds.upload_full_exam_pdf(course_id, year, semester, moed, pdf_file)

            if result.get("status") == "success":
                return json.dumps({
                    "status": "success",
                    "message": result.get("message", "File uploaded successfully."),
                    "has_link": result.get("has_link", False),
                    "link": result.get("link", None)
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": result.get("message", "An error occurred while uploading the file.")
                })
        except Exception as e:
            print(f"Error in serviceLayer.upload_full_exam_pdf: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": "An unexpected error occurred in the service layer.",
                "error": str(e)
            })
    
    def uploadSolution(self, course_id, year, semester, moed,question_number, solution_file):
        try:
            result = self.negev_nerds.uploadSolution(course_id, year, semester, moed,question_number, solution_file)

            if result.get("status") == "success":
                return json.dumps({
                    "status": "success",
                    "message": result.get("message", "File uploaded successfully."),
                    "has_link": result.get("has_link", False),
                    "link": result.get("link", None)
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": result.get("message", "An error occurred while uploading the file.")
                })
        except Exception as e:
            print(f"Error in serviceLayer.upload_full_exam_pdf: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": "An unexpected error occurred in the service layer.",
                "error": str(e)
            })
    def get_exam_pdf_link(self, course_id, year, semester, moed):
        try:
            result = self.negev_nerds.get_exam_pdf_link(course_id, year, semester, moed)

            if result.get("status") == "success":
                return json.dumps({
                    "success": True,
                    "has_link": result.get("has_link", False),
                    "message": result.get("message", "Operation successful."),
                    "link": result.get("link", None)  # Link will be used only if needed
                })
            else:
                return json.dumps({
                    "success": False,
                    "message": result.get("message", "Unknown error occurred.")
                })
        except Exception as e:
            print(f"Error in get_exam_pdf_link: {str(e)}")
            return json.dumps({
                "success": False,
                "message": "An unexpected error occurred.",
                "error": str(e)
            })

    def initialize_system(self, file_path="init.json"):
        """
        Initialize the system with predefined data from a JSON file.
        """
        print("Initializing the system with predefined data...")

        # Load initialization data from the JSON file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                init_data = json.load(file)

            # Extract users and courses
            users = init_data.get("users", [])
            courses = init_data.get("courses", [])

            usersId = []

            # Register users
            for i in range(len(users)):
                curr_user_id, _ = self.registerWithoutAuth(users[i]['email'], users[i]['password'], users[i]['first_name'], users[i]['last_name'])
                usersId.append(curr_user_id)
                print(f"Registering user {users[i]['email']}: {curr_user_id}")
                res = self.login(users[i]['email'],users[i]['password'])
                print("logIn " ,res)
                res = self.logout(users[i]['email'])
                print("logOut ", res)

            # Create courses and enroll users
            for i in range(len(courses)):
                # Create the course
                course = courses[i]
                response = self.open_course(usersId[i], course['courseId'], course['name'], course['syllabus_content_pdf'])
                print(f"Creating course {course['name']}: {response}")

            res = self.register_to_course(courses[1]["courseId"], usersId[0])
            print(f"register {users[0]['first_name']} to course  {courses[1]['name']}: {res}")

            res = self.register_to_course(courses[0]["courseId"], usersId[1])
            print(f"register {users[1]['first_name']} to course  {courses[0]['name']}: {res}")

            res = self.register_to_course(courses[0]["courseId"], usersId[3])
            print(f"register {users[3]['first_name']} to course  {courses[0]['name']}: {res}")

            res = self.register_to_course(courses[1]["courseId"], usersId[2])
            print(f"register {users[2]['first_name']} to course  {courses[1]['name']}: {res}")

            res = self.register_to_course(courses[1]["courseId"], usersId[3])
            print(f"register {users[3]['first_name']} to course  {courses[1]['name']}: {res}")

            res = self.register_to_course(courses[2]["courseId"], usersId[0])
            print(f"register {users[0]['first_name']} to course  {courses[2]['name']}: {res}")

            res = self.register_to_course(courses[2]["courseId"], usersId[1])
            print(f"register {users[1]['first_name']} to course  {courses[2]['name']}: {res}")

            res = self.register_to_course(courses[2]["courseId"], usersId[2])
            print(f"register {users[2]['first_name']} to course  {courses[2]['name']}: {res}")

            res = self.register_to_course(courses[2]["courseId"], usersId[3])
            print(f"register {users[3]['first_name']} to course  {courses[2]['name']}: {res}")
            # res = self.add_question(courses[0]["courseId"], 2023, "קיץ", "ב", 3,
            #                         False, ["math", "algebra"],"ex2.pdf",None)
            #
            # print(" add question -", res)
            # res = self.add_question(courses[2]["courseId"], 2023,'סתיו' ,'ב' ,1, False, ["Symbolic"],
            #                         "Backend/SWE_2023_A_b/202201B-1.pdf",
            #                           "Backend/SWE_2023_A_b/202201B - Solution-1.pdf")
            # print(" add question -", res)
            print("System initialization complete.")
        except FileNotFoundError:
            print(f"Error: Initialization file {file_path} not found.")
        except json.JSONDecodeError:
            print("Error: Failed to parse the initialization file.")
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")



