from datetime import datetime


class CommentDTO:
    def __init__(self, comment_id, writer_name, date, prev_id, comment_text, deleted, reactions):
        """
        Data Transfer Object for the Comment class.
        """
        self.comment_id = comment_id
        self.writer_name = writer_name
        self.date = date
        self.prev_id = prev_id
        self.comment_text = comment_text
        self.deleted = deleted
        self.reactions = reactions

    def to_dict(self):
        """
        Converts the CommentDTO instance to a dictionary.

        :return: Dictionary representation of the CommentDTO.
        """
        return {
            "comment_id": self.comment_id,
            "writer_name": self.writer_name,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "prev_id": self.prev_id,
            "comment_text": self.comment_text,
            "deleted": self.deleted,
            "reactions": [
                reaction.to_dict() if hasattr(reaction, "to_dict") else reaction
                for reaction in self.reactions
            ],
        }