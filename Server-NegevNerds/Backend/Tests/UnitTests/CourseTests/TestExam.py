import unittest
from Backend.BusinessLayer.Course.Exam import Exam
from Backend.BusinessLayer.Util.Exceptions import QuestionDoesNotMeetExamFields, QuestionAlreadyInExam, QuestionNotFound
from Backend.BusinessLayer.Course.enums import Semester, Moed
from Backend.DataLayer.DTOs.QuestionDTO import QuestionDTO


class TestExam(unittest.TestCase):

    def setUp(self):
        """ Set up a basic exam instance for the tests. """
        self.exam = Exam(
            exam_id=1,
            course_name="Math",
            link="exam_link",
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A
        )

    def test_create_exam(self):
        """ Test creating an exam and its basic attributes """
        self.assertEqual(self.exam.course_name, "Math")
        self.assertEqual(self.exam.year, 2024)
        self.assertEqual(self.exam.semester, Semester.FALL)
        self.assertEqual(self.exam.moed, Moed.A)

    def test_generate_question_id(self):
        """ Test generating question IDs """
        self.assertEqual(self.exam.generate_question_id(), 1)

    def test_add_question(self):
        """ Test adding a question to the exam """
        question_dto = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        self.exam.add_question(question_dto)
        self.assertEqual(len(self.exam.questions_list), 1)
        self.assertIn(1, self.exam.questions_list)

    def test_add_question_duplicate(self):
        """ Test adding a duplicate question number raises an exception """
        question_dto1 = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        question_dto2 = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Geometry"],
            is_american=False,
            link_to_question="link2"
        )

        self.exam.add_question(question_dto1)

        with self.assertRaises(QuestionAlreadyInExam):
            self.exam.add_question(question_dto2)

    def test_add_question_field_mismatch(self):
        """ Test adding a question with mismatched fields raises an exception """
        question_dto = QuestionDTO(
            question_id=None,
            year=2025,  # Mismatched year
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )

        with self.assertRaises(QuestionDoesNotMeetExamFields):
            self.exam.add_question(question_dto)

    def test_get_questions_by_specific(self):
        """ Test searching for questions with specific criteria (year, semester, moed, question_number) """

        # Adding multiple questions to the exam
        question_dto1 = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        question_dto2 = QuestionDTO(
            question_id=None,
            year=2024,  # Same year as question_dto1
            semester=Semester.FALL,  # Same semester as question_dto1
            moed=Moed.A,  # Same moed as question_dto1
            question_number=2,
            question_topics=["Geometry"],
            is_american=False,
            link_to_question="link2"
        )

        self.exam.add_question(question_dto1)  # Adding the first question
        self.exam.add_question(question_dto2)  # Adding the second question

        # Test search for specific question by number
        result = self.exam.get_questions_by_specific(question_number=1)
        self.assertEqual(len(result), 1)  # Should return exactly 1 question
        self.assertEqual(result[0].question_number, 1)  # Ensure it's the right question

        # Test search for all questions (no filter)
        result_all = self.exam.get_questions_by_specific()
        self.assertEqual(len(result_all), 2)  # Should return 2 questions

    def test_remove_question(self):
        """ Test removing a question from the exam """
        question_dto = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        self.exam.add_question(question_dto)
        self.exam.remove_question(1)
        self.assertNotIn(1, self.exam.questions_list)

    def test_remove_question_not_found(self):
        """ Test removing a question that doesn't exist raises an exception """
        with self.assertRaises(QuestionNotFound):
            self.exam.remove_question(99)

    def test_get_question(self):
        """ Test getting a question by its number """
        question_dto = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        self.exam.add_question(question_dto)
        question = self.exam.get_question(1)
        self.assertEqual(question.question_number, 1)
        self.assertEqual(question.question_topics, ["Algebra"])

    def test_get_question_not_found(self):
        """ Test trying to get a non-existent question raises an exception """
        with self.assertRaises(QuestionNotFound):
            self.exam.get_question(99)

    def test_to_dto(self):
        """ Test converting Exam to DTO """
        question_dto = QuestionDTO(
            question_id=None,
            year=2024,
            semester=Semester.FALL,
            moed=Moed.A,
            question_number=1,
            question_topics=["Algebra"],
            is_american=False,
            link_to_question="link1"
        )
        self.exam.add_question(question_dto)
        exam_dto = self.exam.to_dto()
        self.assertEqual(exam_dto.exam_id, self.exam.id)
        self.assertEqual(len(exam_dto.questions_list), 1)

    def test_edit_course_name(self):
        """ Test editing course name """
        self.exam.edit_course_name("Advanced Math")
        self.assertEqual(self.exam.course_name, "Advanced Math")

    def test_edit_link(self):
        """ Test editing exam link """
        self.exam.edit_link("new_link")
        self.assertEqual(self.exam.link, "new_link")

    def test_edit_year(self):
        """ Test editing exam year """
        self.exam.edit_year(2025)
        self.assertEqual(self.exam.year, 2025)
        with self.assertRaises(ValueError):
            self.exam.edit_year("2025")  # Invalid value

    def test_edit_semester(self):
        """ Test editing exam semester """
        self.exam.edit_semester(Semester.SPRING)
        self.assertEqual(self.exam.semester, Semester.SPRING)
        with self.assertRaises(ValueError):
            self.exam.edit_semester("WInter")  # Invalid value

    def test_edit_moed(self):
        """ Test editing exam moed """
        self.exam.edit_moed('B')
        self.assertEqual(self.exam.moed, Moed.B)
        with self.assertRaises(ValueError):
            self.exam.edit_moed("Z")  # Invalid moed
