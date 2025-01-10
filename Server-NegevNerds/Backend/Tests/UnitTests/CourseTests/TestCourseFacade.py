import unittest
from unittest.mock import MagicMock
from Backend.BusinessLayer.Course.CourseFacade import CourseFacade
from Backend.BusinessLayer.Util.Exceptions import CourseAlreadyExists, CourseIsNotExist


class TestCourseFacade(unittest.TestCase):

    def setUp(self):
        # Set up the mock objects for the test
        self.course_facade = CourseFacade()  # Instantiate the CourseFacade
        self.course = MagicMock()  # Mock the Course object
        self.course_facade.courses = {}  # Mock an empty courses dictionary

    def test_open_course_success(self):
        """Test case for successfully creating a new course."""
        course_id = "CS101"
        course_name = "Computer Science 101"
        course_topics = ["Algorithms", "Data Structures"]

        # Call the method to open the course
        result = self.course_facade.open_course(course_id, course_name, course_topics)

        # Assert the course was added to the courses dictionary
        self.assertTrue(result)
        self.assertIn(course_id, self.course_facade.courses)
        self.assertEqual(self.course_facade.courses[course_id].course_id, course_id)

    def test_open_course_already_exists(self):
        """Test case for when the course already exists."""
        course_id = "CS101"
        self.course_facade.courses[course_id] = self.course  # Add an existing course

        with self.assertRaises(CourseAlreadyExists):
            self.course_facade.open_course(course_id, "New Course", ["Algorithms"])

    def test_remove_student_from_course(self):
        """Test case for removing a student from a course."""
        course_id = "CS101"
        user_id = "user123"
        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Mock the addStudent function
        self.course.removeStudent = MagicMock()
        self.course.removeStudent(user_id)

        # Call the remove_student_from_course function
        self.course_facade.remove_student_from_course(course_id, user_id)

        # Check if removeStudent was called
        self.course.removeStudent.assert_called_with(user_id)

    def test_remove_student_from_course_course_not_found(self):
        """Test case for when trying to remove a student from a non-existing course."""
        course_id = "CS101"
        user_id = "user123"

        with self.assertRaises(CourseIsNotExist):
            self.course_facade.remove_student_from_course(course_id, user_id)

    def test_add_exam_to_course(self):
        """Test case for adding an exam to a course."""
        course_id = "CS101"
        course_name = "Computer Science 101"
        exam_name = "Final Exam"
        link = "/path/to/exam.pdf"
        year = 2023
        semester = "Fall"
        moed = "A"

        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Mock the add_exam function of the course
        self.course.add_exam = MagicMock()

        # Call the add_exam_to_course function
        self.course_facade.add_exam_to_course(course_id, course_name, link, year, semester, moed)

        # Check if the add_exam method was called
        self.course.add_exam.assert_called_with(course_name, link, year, semester, moed)

    def test_remove_exam_from_course(self):
        """Test case for removing an exam from a course."""
        course_id = "CS101"
        year = 2023
        semester = "Fall"
        moed = "A"
        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Mock the remove_exam method of the course
        self.course.remove_exam = MagicMock()

        # Call the remove_exam_from_course function
        self.course_facade.remove_exam_from_course(course_id, year, semester, moed)

        # Check if remove_exam method was called
        self.course.remove_exam.assert_called_with(year, semester, moed)

    def test_remove_course(self):
        """Test case for removing a course."""
        course_id = "CS101"
        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Call the remove_course function
        self.course_facade.remove_course(course_id)

        # Check if course was removed from the courses dictionary
        self.assertNotIn(course_id, self.course_facade.courses)

    def test_remove_course_not_found(self):
        """Test case for trying to remove a non-existing course."""
        course_id = "CS101"

        with self.assertRaises(CourseIsNotExist):
            self.course_facade.remove_course(course_id)

    def test_add_course_topic(self):
        """Test case for adding a topic to a course."""
        course_id = "CS101"
        course_topic = "New Topic"
        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Mock the add_course_topic function
        self.course.add_course_topic = MagicMock()

        # Call the add_course_topic function
        self.course_facade.add_course_topic(course_id, course_topic)

        # Check if the add_course_topic was called
        self.course.add_course_topic.assert_called_with(course_topic)

    def test_get_course_success(self):
        """Test case for retrieving an existing course."""
        course_id = "CS101"
        self.course_facade.courses[course_id] = self.course  # Add a course to the facade

        # Call the get_course function
        result = self.course_facade.get_course(course_id)

        # Verify the course returned is the correct one
        self.assertEqual(result, self.course)

    def test_get_course_not_found(self):
        """Test case for trying to retrieve a non-existing course."""
        course_id = "CS101"

        with self.assertRaises(CourseIsNotExist):
            self.course_facade.get_course(course_id)


if __name__ == '__main__':
    unittest.main()
