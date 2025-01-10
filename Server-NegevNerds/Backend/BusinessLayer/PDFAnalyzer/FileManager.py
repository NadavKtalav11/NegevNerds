import os
import shutil


import threading
import os

class FileManager:
  
    _instance = None
    _lock = threading.Lock()

    # def __new__(cls, base_dir='./NegevNerds/files'):
    #     if not cls._instance:
    #         with cls._lock:
    #             # Double-checked locking pattern
    #             if not cls._instance:
    #                 cls._instance = super().__new__(cls)
                    # Initialize attributes here
    #                 cls._instance._base_dir = base_dir
    #                 cls._instance._initialized = True
    #                 # Ensure the base directory exists
    #                 os.makedirs(base_dir, exist_ok=True)
    #     return cls._instance

    # def __init__(self, base_dir='./NegevNerds/files'):
    #     # This method might be called multiple times, so we use the _initialized check
    #     if not hasattr(self, '_initialized'):
    #         self._base_dir = base_dir
    #         self._initialized = True
    #         os.makedirs(self._base_dir, exist_ok=True)
    
    def __new__(cls, base_dir=None):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    # Set base directory, defaulting to './files' if not provided
                    cls._instance._base_dir = os.path.abspath(base_dir or './files')
                    cls._instance._initialized = True
                    os.makedirs(cls._instance._base_dir, exist_ok=True)
                    print(f"FileManager base directory: {cls._instance._base_dir}")
        return cls._instance

    def __init__(self, base_dir=None):
        if not hasattr(self, '_initialized'):
            self._base_dir = os.path.abspath(base_dir or './files')
            self._initialized = True
            os.makedirs(self._base_dir, exist_ok=True)

    def create_course_folder(self, course_id):
        """Creates a folder for the course if it doesn't exist."""
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")

        # Create the course folder if it doesn't exist
        if not os.path.exists(course_folder):
            os.makedirs(course_folder)

        return course_folder

    def delete_course_folder(self, course_id):
        """Deletes the folder for a course."""
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        if os.path.exists(course_folder):
            shutil.rmtree(course_folder)  # Removes the directory and all its contents
            return True
        else:
            return False

    def get_question_path(self, link_to_question):
        return os.path.join(self._base_dir, link_to_question)

    def get_answer_path(self, course_id, year, semester, moed, question_number):
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))
        exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
        answers_folder = os.path.join(exam_folder, "answers")
        answer_file_path = os.path.join(answers_folder, f"answer_{question_number}.pdf")
        return answer_file_path
      
    # def get_question_path(self, course_id, year, semester, moed, question_number):
    #     course_folder = os.path.join(self._base_dir, f"course_{course_id}")
    #     year_folder = os.path.join(course_folder, str(year))
    #     exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
    #     questions_folder = os.path.join(exam_folder, "questions")
    #     question_file_path = os.path.join(questions_folder, f"question_{question_number}.pdf")
    #     return question_file_path
    #
    # def get_answer_path(self, course_id, year, semester, moed, question_number):
    #     course_folder = os.path.join(self._base_dir, f"course_{course_id}")
    #     year_folder = os.path.join(course_folder, str(year))
    #     exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
    #     answers_folder = os.path.join(exam_folder, "answers")
    #     answer_file_path = os.path.join(answers_folder, f"answer_{question_number}.pdf")
    #     return answer_file_path

    def save_syllabus_file(self, course_id, syllabus_content):
        """Saves the syllabus file in the course folder, replacing the existing one if present."""

        # Check if the syllabus content is empty
        if not syllabus_content:
            raise ValueError("Syllabus content cannot be empty.")  # Raise an exception if the content is empty

        # Create the course folder if it doesn't exist
        course_folder = self.create_course_folder(course_id)

        # Define the file path for the syllabus
        syllabus_file_path = os.path.join(course_folder, f"syllabus_{course_id}.pdf")

        # Check if the file already exists and remove it if so
        if os.path.exists(syllabus_file_path):
            os.remove(syllabus_file_path)  # Delete the existing syllabus file

        # Save the new syllabus content as a PDF file
        with open(syllabus_file_path, 'wb') as file:
            file.write(syllabus_content)

        return syllabus_file_path

    def save_exam_file(self, course_id, year, semester, moed, exam_content):
        """Saves the exam file in the course's year folder."""

        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))

        # Create the year folder if it doesn't exist
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        # Save the exam file in the year folder
        exam_file_path = os.path.join(year_folder, f"exam_{course_id}_{year}_{semester}_{moed}.pdf")
        with open(exam_file_path, 'wb') as file:
            file.write(exam_content)

        return exam_file_path
    
    def save_exam_file1(self, course_id, year, semester, moed, pdf_file):
        """Saves the exam file in the course's year folder."""
        try:
            # Define folder paths
            course_folder = os.path.join(self._base_dir, f"course_{course_id}")
            year_folder = os.path.join(course_folder, str(year))

            # Create the year folder if it doesn't exist
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            # Define the file path
            exam_file_path = os.path.join(year_folder, f"exam_{course_id}_{year}_{semester}_{moed}.pdf")

            # Read the file content and write it to the desired location
            with open(exam_file_path, 'wb') as file:
                file.write(pdf_file.read())  # Read the content from the FileStorage object

            return exam_file_path
        except Exception as e:
            raise Exception(f"Failed to save exam file: {str(e)}")


    # def save_question_file(self, course_id, year, semester, moed, question_number, question_content_pdf):
    #     """Saves a question file inside the corresponding exam folder."""

    #     course_folder = os.path.join(self._base_dir, f"course_{course_id}")
    #     year_folder = os.path.join(course_folder, str(year))
    #     exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")

        # Create the exam folder if it doesn't exist
        # if not os.path.exists(exam_folder):
        #     os.makedirs(exam_folder)

        # # Create the questions folder inside the exam folder if it doesn't exist
        # question_folder = os.path.join(exam_folder, f"questions")
        # if not os.path.exists(question_folder):
        #     os.makedirs(question_folder)

        # # Save the question file inside the questions folder
        # question_file_path = os.path.join(question_folder, f"question_{question_number}.pdf")
        # with open(question_file_path, 'w') as file:
        #     file.write(question_content_pdf)

        # return question_file_path


    # def save_answer_file(self, course_id, year, semester, moed, question_number, answer_content_pdf):
        # """Saves an answer file corresponding to a question inside the corresponding exam folder."""

        # course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        # year_folder = os.path.join(course_folder, str(year))
        # exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")

        # # Create the exam folder if it doesn't exist
        # if not os.path.exists(exam_folder):
        #     os.makedirs(exam_folder)

        # # Create the answers folder inside the exam folder if it doesn't exist
        # answer_folder = os.path.join(exam_folder, f"answers")
        # if not os.path.exists(answer_folder):
        #     os.makedirs(answer_folder)

        # # Save the answer file inside the answers folder
        # answer_file_path = os.path.join(answer_folder, f"answer_{question_number}.pdf")
        # with open(answer_file_path, 'w') as file:
        #     file.write(answer_content_pdf)

        # return answer_file_path

    def save_question_file_pdf(self, course_id, year, semester, moed, question_number, pdf_question):
        """
        Saves the question PDF file to the appropriate directory.
        """
        # Construct the file path
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))
        exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
        question_folder = os.path.join(exam_folder, "questions")

        # Create directories if they do not exist
        os.makedirs(question_folder, exist_ok=True)


        question_file_path = os.path.join(question_folder, f"question_{question_number}.pdf")
        # with open(question_file_path, 'wb') as f:
        #     f.write(file_content)

        pdf_question.seek(0)

        pdf_question.save(question_file_path)


        return question_file_path

    def save_photo_question_file(self, course_id, year, semester, moed, question_number, photo_file):
        """
        Saves the question photo file (e.g., JPEG, PNG) to the appropriate directory.

        :param course_id: Course identifier
        :param year: Year of the exam
        :param semester: Semester of the exam
        :param moed: Moed of the exam
        :param question_number: Question number
        :param photo_file: File-like object representing the photo
        :return: Full path to the saved photo file
        """
        # Construct the file path
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))
        exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
        question_folder = os.path.join(exam_folder, "questions")

        # Create directories if they do not exist
        os.makedirs(question_folder, exist_ok=True)

        # Determine the file extension (e.g., 'jpg', 'png') from the uploaded photo file
        photo_extension = photo_file.filename.rsplit('.', 1)[-1].lower()
        if photo_extension not in ["jpg", "jpeg", "png"]:
            raise ValueError("Unsupported file format. Only JPEG and PNG are allowed.")

        # Construct the file name and path
        photo_file_path = os.path.join(question_folder, f"question_{question_number}.{photo_extension}")

        # Save the photo file to disk
        photo_file.seek(0)  # Ensure the file pointer is at the beginning
        photo_file.save(photo_file_path)

        return photo_file_path

    def save_answer_file_pdf(self, course_id, year, semester, moed, question_number, pdf_answer):
        """
        Saves the answer PDF file to the appropriate directory.
        """
        # Construct the file path

        pdf_answer.seek(0)


        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))
        exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
        answer_folder = os.path.join(exam_folder, "answers")

        # Create directories if they do not exist
        os.makedirs(answer_folder, exist_ok=True)

        # Define the file path
        answer_file_path = os.path.join(answer_folder, f"answer_{question_number}.pdf")

        # Save the file using FileStorage's save() method
        pdf_answer.save(answer_file_path)

        return answer_file_path


    def save_photo_answer_file(self, course_id, year, semester, moed, question_number, photo_file):
        """
        Saves the question photo file (e.g., JPEG, PNG) to the appropriate directory.

        :param course_id: Course identifier
        :param year: Year of the exam
        :param semester: Semester of the exam
        :param moed: Moed of the exam
        :param question_number: Question number
        :param photo_file: File-like object representing the photo
        :return: Full path to the saved photo file
        """
        # Construct the file path
        course_folder = os.path.join(self._base_dir, f"course_{course_id}")
        year_folder = os.path.join(course_folder, str(year))
        exam_folder = os.path.join(year_folder, f"exam_{year}_{semester}_{moed}")
        question_folder = os.path.join(exam_folder, "answers")

        # Create directories if they do not exist
        os.makedirs(question_folder, exist_ok=True)

        # Determine the file extension (e.g., 'jpg', 'png') from the uploaded photo file
        photo_extension = photo_file.filename.rsplit('.', 1)[-1].lower()
        if photo_extension not in ["jpg", "jpeg", "png"]:
            raise ValueError("Unsupported file format. Only JPEG and PNG are allowed.")

        # Construct the file name and path
        photo_file_path = os.path.join(question_folder, f"answer{question_number}.{photo_extension}")

        # Save the photo file to disk
        photo_file.seek(0)  # Ensure the file pointer is at the beginning
        photo_file.save(photo_file_path)

        return photo_file_path


    import os

    def delete_file(self, file_path):
        """
        Deletes a file (PDF or photo) from the specified path.

        :param file_path: Full path to the file to be deleted
        :return: Boolean indicating whether the file was successfully deleted
        :raises: FileNotFoundError if the file does not exist
        """
        try:
            # Check if the file exists
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file
                print(f"File deleted successfully: {file_path}")
                return True
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False
