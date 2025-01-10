import unittest
import os
from io import BytesIO
from Backend.BusinessLayer.PDFAnalyzer.FileManager import FileManager  # Importing the FileManager class


class TestFileManager(unittest.TestCase):
    def setUp(self):
        """Setup method that runs before each test to prepare the test environment."""
        self.base_dir = './test_files'  # The directory where test files will be stored
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)  # Create the directory if it doesn't exist
        self.file_manager = FileManager(base_dir=self.base_dir)  # Instantiate the FileManager with the test directory

    def tearDown(self):
        """Cleanup method that runs after each test to remove test files and directories."""
        # Walk through the test directory and remove files and subdirectories
        for root, dirs, files in os.walk(self.base_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))  # Remove the files
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))  # Remove the directories
        os.rmdir(self.base_dir)  # Remove the test directory itself

    def test_create_course_folder(self):
        """Test creating a course folder in the file system."""
        course_id = "CS101"
        course_folder = self.file_manager.create_course_folder(course_id)
        self.assertTrue(os.path.exists(course_folder))  # Assert that the course folder is created

    def test_save_syllabus_file(self):
        """Test saving a syllabus file in the course folder and replacing an existing one."""
        course_id = "CS101"
        syllabus_content = b"Sample syllabus content"  # Sample syllabus content as bytes

        # Save the syllabus file for the first time
        syllabus_file_path = self.file_manager.save_syllabus_file(course_id, syllabus_content)

        # Assert that the syllabus file exists
        self.assertTrue(os.path.exists(syllabus_file_path))
        self.assertTrue(syllabus_file_path.endswith(".pdf"))  # Assert that the file is a PDF

        # Save a new syllabus to replace the existing one
        new_syllabus_content = b"Updated syllabus content"  # Updated content as bytes
        updated_syllabus_file_path = self.file_manager.save_syllabus_file(course_id, new_syllabus_content)

        # Assert that the new syllabus file exists and has replaced the old one
        self.assertTrue(os.path.exists(updated_syllabus_file_path))
        self.assertTrue(updated_syllabus_file_path.endswith(".pdf"))  # Assert that the file is a PDF

        # Check if the new syllabus file path is the same as the previous one (it should replace the old one)
        self.assertEqual(syllabus_file_path, updated_syllabus_file_path)

    def test_save_exam_file(self):
        """Test saving an exam file in the course's year folder."""
        course_id = "CS101"
        exam_content = b"Sample exam content"  # Sample exam content as bytes
        year = 2023
        semester = "Summer"
        moed = "A"
        exam_file_path = self.file_manager.save_exam_file(course_id, year, semester, moed, exam_content)

        # Assert that the exam file exists in the correct folder
        self.assertTrue(os.path.exists(exam_file_path))
        self.assertTrue(exam_file_path.endswith(".pdf"))  # Assert that the file is a PDF

    def test_save_question_file(self):
        """Test saving a question file inside the corresponding exam folder."""
        course_id = "CS101"
        year = 2023
        semester = "Summer"
        moed = "A"
        question_content = b"Sample question content"  # Sample question content as bytes
        question_number = 1
        question_file_path = self.file_manager.save_question_file(course_id, year, semester, moed, question_content,
                                                                  question_number)

        # Assert that the question file exists in the correct folder
        self.assertTrue(os.path.exists(question_file_path))
        self.assertTrue(question_file_path.endswith(".pdf"))  # Assert that the file is a PDF

    def test_create_course_folder_existing(self):
        """Test that the course folder is not recreated if it already exists."""
        course_id = "CS101"
        self.file_manager.create_course_folder(course_id)  # Create the folder once
        course_folder = self.file_manager.create_course_folder(course_id)  # Try to create it again
        self.assertTrue(os.path.exists(course_folder))  # Assert that the folder still exists

    def test_invalid_file_content(self):
        """Test saving a file with invalid content (empty file)."""
        course_id = "CS101"
        invalid_content = b""  # Invalid (empty) content
        with self.assertRaises(Exception):  # Expecting an error when trying to save an empty file
            self.file_manager.save_syllabus_file(course_id, invalid_content)


if __name__ == "__main__":
    unittest.main()  # Run all the tests
