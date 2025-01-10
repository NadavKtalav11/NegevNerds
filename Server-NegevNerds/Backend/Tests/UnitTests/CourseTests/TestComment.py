import unittest
from datetime import datetime
from Backend.BusinessLayer.Course.Comment import Comment
from Backend.BusinessLayer.Util.Exceptions import UserAlreadyPostEmoji, EmojiNotFounded


class TestComment(unittest.TestCase):
    def setUp(self):
        """
        Set up a Comment instance for testing.
        """
        self.comment = Comment(
            comment_id=1,
            writer_name="TestUser",
            date=datetime(2024, 1, 1, 10, 0, 0),
            prev_id=None,
            text="This is a test Comment."
        )

    def test_add_emoji_success(self):
        """
        Test adding an emoji successfully.
        """
        self.comment.add_emoji("like", "user1")
        self.assertIn("user1", self.comment.emoji_counter_map["like"])

    def test_add_duplicate_emoji_raises_exception(self):
        """
        Test adding the same emoji by the same user raises an exception.
        """
        self.comment.add_emoji("like", "user1")
        with self.assertRaises(UserAlreadyPostEmoji):
            self.comment.add_emoji("like", "user1")

    def test_remove_emoji_success(self):
        """
        Test removing an emoji from the Comment successfully.
        """
        self.comment.add_emoji("like", "user1")
        self.comment.remove_emoji("like", "user1")  # Pass the userId as well
        self.assertNotIn("user1", self.comment.emoji_counter_map["like"])

    def test_remove_nonexistent_emoji_raises_exception(self):
        """
        Test that attempting to remove an emoji that does not exist raises an exception.
        """
        with self.assertRaises(EmojiNotFounded):
            self.comment.remove_emoji("like", "user1")  # Pass both 'like' and 'userId'

    def test_edit_text(self):
        """
        Test editing the text of a Comment.
        """
        new_text = "Updated Comment text."
        self.comment.edit_text(new_text)
        self.assertEqual(self.comment.text, new_text)

    def test_get_score(self):
        """
        Test the score calculation of the Comment based on likes and dislikes.
        """
        self.comment.add_emoji("like", "user1")
        self.comment.add_emoji("like", "user2")
        self.comment.add_emoji("dislike", "user3")
        self.assertEqual(self.comment.get_score(), 1)  # 2 likes - 1 dislike = 1

    def test_get_score_no_emojis(self):
        """
        Test calculating the score when there are no emojis.
        """
        self.assertEqual(self.comment.get_score(), 0)


if __name__ == "__main__":
    unittest.main()
