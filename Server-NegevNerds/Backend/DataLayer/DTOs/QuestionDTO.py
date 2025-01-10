from Backend.BusinessLayer.Course.enums import Semester, Moed

class QuestionDTO:
    def __init__(self, question_id, year, semester, moed, question_number, question_topics,
                 is_american, link_to_question, comments_list, course_id):
        """
        Data Transfer Object for the Question class.
        """
        self.question_id = question_id
        self.year = year
        self.semester = Semester(semester)  # Convert to Enum
        self.moed = Moed(moed)              # Convert to Enum
        self.question_number = question_number
        self.question_topics = question_topics
        self.is_american = is_american
        self.link_to_question = link_to_question
        self.comments_list = comments_list
        self.course_id = course_id

    def to_dict(self):
        """
        Converts the QuestionDTO instance to a dictionary.

        :return: Dictionary representation of the QuestionDTO.
        """
        return {
            "question_id": self.question_id,
            "year": self.year,
            "semester": self.semester.value if hasattr(self.semester, 'value') else self.semester,
            "moed": self.moed.value if hasattr(self.moed, 'value') else self.moed,
            "question_number": self.question_number,
            "question_topics": self.question_topics,
            "is_american": self.is_american,
            "course_id": self.course_id,
            "link_to_question": self.link_to_question,
            "comments_list": [
                comment.to_dict() if hasattr(comment, "to_dict") else comment
                for comment in self.comments_list
            ],
        }

