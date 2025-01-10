import unittest
from Backend.BusinessLayer.Course.Course import Course
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.BusinessLayer.Course.Exam import Exam
from Backend.BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.QuestionDTO import QuestionDTO


class TestCourse(unittest.TestCase):

    def setUp(self):
        """Create a course instance for testing"""
        self.course = Course(course_id=1, name="Math", course_topics=["Algebra", "Calculus"])
        # Create two exams for testing
        self.course.add_exam( link="midterm_link", year=2024, semester=Semester.FALL, moed=Moed.A)
        self.course.add_exam( link="final_link", year=2024, semester=Semester.SPRING, moed=Moed.B)

        # Add questions to exams
        question1 = QuestionDTO(question_id=None, year=2024, semester=Semester.FALL, moed=Moed.A,
                                question_number=1, question_topics=["Algebra"], is_american=False,
                                link_to_question="link1")
        question2 = QuestionDTO(question_id=None, year=2024, semester=Semester.FALL, moed=Moed.A,
                                question_number=2, question_topics=["Calculus"], is_american=True,
                                link_to_question="link2")
        question3 = QuestionDTO(question_id=None, year=2024, semester=Semester.SPRING, moed=Moed.B,
                                question_number=1, question_topics=["Geometry"], is_american=False,
                                link_to_question="link3")

        self.course.exams[2024][0].add_question(question1)  # Add to Midterm
        self.course.exams[2024][0].add_question(question2)  # Add to Midterm
        self.course.exams[2024][1].add_question(question3)  # Add to Final

    def test_add_course_topic(self):
        """Test adding a new course topic"""
        self.course.add_course_topic("Geometry")
        self.assertIn("Geometry", self.course.get_topics())

    def test_remove_course_topic(self):
        """Test removing an existing course topic"""
        self.course.remove_course_topic("Calculus")
        self.assertNotIn("Calculus", self.course.get_topics())

    def test_add_student(self):
        """Test adding a student to the course"""
        self.course.add_student(1001)
        self.assertIn(1001, self.course.get_students())

    def test_remove_student(self):
        """Test removing a student from the course"""
        self.course.add_student(1002)
        self.course.remove_student(1002)
        self.assertNotIn(1002, self.course.get_students())

    def test_add_exam(self):
        """Test adding an exam to the course"""
        self.course.remove_exam(2024, Semester.FALL, Moed.A)

        self.course.add_exam( link="exam_link", year=2024, semester=Semester.FALL, moed=Moed.A)

        exams = self.course.get_exams(2024, Semester.FALL, Moed.A)
        self.assertEqual(len(exams), 1)
        self.assertEqual(exams[0].course_name, "Midterm")

    def test_remove_exam(self):
        """Test removing an exam from the course"""
        self.course.remove_exam(2024, Semester.FALL, Moed.A)
        exams = self.course.get_exams(2024, Semester.FALL, Moed.A)
        self.assertEqual(len(exams), 0)

    def test_add_manager(self):
        """Test adding a manager to the course"""
        self.course.add_manager(1)
        self.assertIn(1, self.course.get_managers())

    def test_remove_manager(self):
        """Test removing a manager from the course"""
        self.course.add_manager(1)
        self.course.remove_manager(1)
        self.assertNotIn(1, self.course.get_managers())

    def test_get_exam(self):
        """Test retrieving a specific exam"""
        # Retrieving the added exam
        exam = self.course.get_exam(2024, Semester.SPRING, Moed.B)

        # Assert that the exam's attributes are correct
        self.assertEqual(exam.course_name, "Final")
        self.assertEqual(exam.year, 2024)
        self.assertEqual(exam.semester, Semester.SPRING)
        self.assertEqual(exam.moed, Moed.B)

    def test_get_exams_by_year(self):
        """Test retrieving exams by year"""
        exams = self.course.get_exams(2024)
        self.assertEqual(len(exams), 2)

    def test_add_course_topic_duplicate(self):
        """Test that adding a duplicate topic raises an exception"""
        with self.assertRaises(TopicAlreadyExist):
            self.course.add_course_topic("Algebra")

    def test_remove_course_topic_not_found(self):
        """Test removing a non-existing topic raises an exception"""
        with self.assertRaises(TopicNotFound):
            self.course.remove_course_topic("Trigonometry")

    def test_remove_student_not_found(self):
        """Test removing a student who is not enrolled in the course raises an exception"""
        with self.assertRaises(UserIsNotRegisterToCourse):
            self.course.remove_student(9999)

    def test_add_student_duplicate(self):
        """Test adding a duplicate student raises an exception"""
        self.course.add_student(1001)
        with self.assertRaises(UserAlreadyRegisterToCourse):
            self.course.add_student(1001)

    def test_add_exam_duplicate(self):
        """Test adding a duplicate exam raises an exception"""
        self.course.remove_exam(2024, Semester.FALL, Moed.A)

        self.course.add_exam( link="exam_link", year=2024, semester=Semester.FALL, moed=Moed.A)

        with self.assertRaises(ExamAlreadyExists):
            self.course.add_exam( link="exam_link", year=2024, semester=Semester.FALL,
                                 moed=Moed.A)

    def test_get_questions_by_specific_no_criteria(self):
        """Test retrieving all questions when no criteria are given"""
        result = self.course.get_questions_by_specific()  # לא הזנו קריטריונים
        self.assertEqual(len(result), 3)  # צריכה לחזור 3 שאלות

    def test_get_questions_by_specific_year(self):
        """ Test retrieving questions by year """
        result = self.course.get_questions_by_specific(year=2024)
        self.assertEqual(len(result), 3)  # Should return 3 questions (from both exams)
        self.assertEqual(result[0].question_number, 1)

    def test_get_questions_by_specific_year_and_semester(self):
        """ Test retrieving questions by year and semester """
        result = self.course.get_questions_by_specific(year=2024, semester=Semester.FALL)
        self.assertEqual(len(result), 2)  # Should return 2 questions from Fall semester
        self.assertEqual(result[0].question_number, 1)  # First question should be number 1

    def test_get_questions_by_specific_year_semester_and_moed(self):
        """ Test retrieving questions by year, semester and moed """
        result = self.course.get_questions_by_specific(year=2024, semester=Semester.FALL, moed=Moed.A)
        self.assertEqual(len(result), 2)  # Should return 2 questions from Fall and Moed A
        self.assertEqual(result[0].question_number, 1)

    def test_get_questions_by_specific_question_number(self):
        """ Test retrieving a specific question by its number """
        result = self.course.get_questions_by_specific(year=2024, semester=Semester.FALL, moed=Moed.A, question_number=1)
        self.assertEqual(len(result), 1)  # Should return 1 question
        self.assertEqual(result[0].question_number, 1)  # Should be question 1

    def test_get_questions_by_specific_invalid_question(self):
        """Test retrieving a non-existing question returns an empty list"""
        result = self.course.get_questions_by_specific(question_number=99)
        self.assertEqual(len(result), 0)  # Should return an empty list for non-existing question


if __name__ == "__main__":
    unittest.main()
