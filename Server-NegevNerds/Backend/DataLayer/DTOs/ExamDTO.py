class ExamDTO:
    def __init__(self, exam_id, course_id, link, year, semester, moed, questions_list):
        """
        Data Transfer Object for the Exam class."""

        self.exam_id = exam_id
        self.course_id = course_id
        self.link = link
        self.year = year
        self.semester = semester
        self.moed = moed
        self.questions_list = questions_list

    def to_dict(self):
        """
        Converts the ExamDTO instance to a dictionary.

        :return: Dictionary representation of the ExamDTO.
        """
        return {
            "exam_id": self.exam_id,
            "course_id": self.course_id,
            "link": self.link,
            "year": self.year,
            "semester": self.semester,
            "moed": self.moed.name if hasattr(self.moed, 'name') else self.moed,
            "questions_list": [
                question.to_dict() if hasattr(question, "to_dict") else question
                for question in self.questions_list
            ],
        }

    # Getters
    def get_exam_id(self):
        return self.exam_id

    def get_course_id(self):
        return self.course_id

    def get_link(self):
        return self.link

    def get_year(self):
        return self.year

    def get_semester(self):
        return self.semester

    def get_moed(self):
        return self.moed

    def get_questions_list(self):
        return self.questions_list

    # Setters
    def set_exam_id(self, exam_id):
        self.exam_id = exam_id

    def set_course_id(self, course_id):
        self.course_id= course_id

    def set_link(self, link):
        self.link = link

    def set_year(self, year):
        self.year = year

    def set_semester(self, semester):
        self.semester = semester

    def set_moed(self, moed):
        self.moed = moed

    def set_questions_list(self, questions_list):
        self.questions_list = questions_list
