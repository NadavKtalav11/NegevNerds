class SearchDTO:
    def __init__(self, question_id, course_id):
        """
        Data Transfer Object for the Reaction class.
        """
        self.course_id = course_id
        self.question_id = question_id
    def __eq__(self, other):
        if not isinstance(other, SearchDTO):
            return NotImplemented
        return self.question_id == other.question_id and self.course_id == other.course_id


    def __hash__(self):
        return hash((self.course_id, self.question_id))

    def __repr__(self):
        return f"SearchDTO(course_id={self.course_id}, question_id={self.question_id})"




