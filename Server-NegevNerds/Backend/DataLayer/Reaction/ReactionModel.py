from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey
from sqlalchemy.orm import relationship

from ..Base import Base


class ReactionModel(Base):

    __tablename__ = 'reactions'

    # Primary key
    reaction_id = Column(String, primary_key=True)

    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    emoji = Column(String, nullable=False)
    comment_id = Column(String, ForeignKey('comments.comment_id'), nullable=False)

    comment = relationship('CommentModel',
                            back_populates='reactions')

    def to_business_model(self):
        from Backend.BusinessLayer.Course.Reaction import Reaction

        reaction = Reaction(
            reaction_id=self.reaction_id,
            user_id=self.user_id,
            emoji=self.emoji,
        )
        return reaction

    @classmethod
    def from_business_model(cls, reaction):

        return cls(
            reaction_id=reaction.reaction_id,
            user_id=comment.user_id,
            emoji=comment.emoji,
        )
