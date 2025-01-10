import unittest
from Backend.BusinessLayer.Course.Question import Question
from Backend.BusinessLayer.Course.Comment import Comment
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.DataLayer.DTOs.QuestionDTO import QuestionDTO

class TestQuestion(unittest.TestCase):
    def setUp(self):
        """
        Set up a Question instance for testing.
        """
        self.question = Question(
            year=2024,
            question_id=1,
            semester="Spring",
            moed="A",
            question_number=1,
            question_topics=["Sorting", "Graphs"],
            is_american=False,
            link_to_question="http://example.com/question1",
            link_to_exam="http://example.com/exam"
        )

    def test_to_dto(self):
        """
        Test conversion of Question to QuestionDTO.
        """
        dto = self.question.to_dto()
        self.assertIsInstance(dto, QuestionDTO)
        self.assertEqual(dto.question_id, self.question.id)
        self.assertEqual(dto.year, self.question.year)
        self.assertEqual(dto.semester, self.question.semester)
        self.assertEqual(dto.moed, self.question.moed)
        self.assertEqual(dto.question_number, self.question.question_number)
        self.assertEqual(dto.question_topics, self.question.question_topics)
        self.assertEqual(dto.is_american, self.question.is_american)
        self.assertEqual(dto.link_to_question, self.question.link_to_question)

    def test_add_question_topic(self):
        """
        Test adding a topic to the question.
        """
        self.question.add_question_topic("Dynamic Programming")
        self.assertIn("Dynamic Programming", self.question.question_topics)

    def test_remove_question_topic(self):
        """
        Test removing a topic from the question.
        """
        self.question.remove_question_topic("Graphs")
        self.assertNotIn("Graphs", self.question.question_topics)

    def test_remove_nonexistent_question_topic(self):
        """
        Test removing a topic that does not exist.
        """
        initial_length = len(self.question.question_topics)
        self.question.remove_question_topic("Nonexistent")
        self.assertEqual(len(self.question.question_topics), initial_length)

    def test_add_comment(self):
        """
        Test adding a Comment to the question.
        """
        self.question.add_comment(
            comment_id=1,
            writer_name="User1",
            prev_id=None,
            comment_text="This is a test Comment."
        )
        self.assertEqual(len(self.question.comments), 1)
        self.assertIsInstance(self.question.comments[0], Comment)

    def test_remove_comment(self):
        """
        Test removing a Comment from the question.
        """
        self.question.add_comment(
            comment_id=1,
            writer_name="User1",
            prev_id=None,
            comment_text="This is a test Comment."
        )
        # Remove the Comment and ensure it is removed
        self.question.remove_comment(1)
        self.assertEqual(len(self.question.comments), 0)

    def test_remove_comment_not_found(self):
        """
        Test removing a non-existent Comment raises CommentNotFound exception.
        """
        with self.assertRaises(CommentNotFound) as context:
            self.question.remove_comment(999)  # ID that does not exist
        self.assertIn("Comment with ID '999' not found", str(context.exception))

    def test_remove_nonexistent_comment(self):
        """
        Test removing a nonexistent Comment raises CommentNotFound exception.
        """
        with self.assertRaises(CommentNotFound) as context:
            self.question.remove_comment(999)  # Nonexistent Comment ID
        self.assertIn("Comment with ID '999' not found", str(context.exception))

    def test_str_representation(self):
        """
        Test string representation of the Question instance.
        """
        result = str(self.question)
        self.assertIn("Question(ID: 1", result)
        self.assertIn("Year: 2024", result)
        self.assertIn("Semester: Spring", result)
        self.assertIn("Moed: A", result)

if __name__ == "__main__":
    unittest.main()
