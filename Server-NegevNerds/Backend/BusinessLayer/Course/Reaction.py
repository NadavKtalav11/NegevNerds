from Backend.DataLayer.Reaction.ReactionRepository import ReactionRepository
from Backend.DataLayer.DTOs.ReactionDTO import ReactionDTO

class Reaction:
    def __init__(self, reaction_id, user_id, emoji):
        """
        Initialize a Reaction instance.
        """
        self.reaction_id = reaction_id
        self.user_id = user_id
        self.emoji = emoji

    @classmethod
    def create(cls, reaction_id, user_id, emoji, comment_id):
        """
        Class method to create a new reaction and save to database
        Returns:
            Reaction: Newly created reaction instance
        """

        reaction = cls(
            reaction_id=reaction_id,
            user_id=user_id,
            emoji=emoji,
        )
        reaction_repo = ReactionRepository()
        reaction_repo.add_reaction(reaction, comment_id)

        return reaction

    def to_dto(self):
        """
        Converts the Reaction instance to a ReactionDTO.
        :return: ReactionDTO instance.
        """
        return ReactionDTO(
            reaction_id=self.reaction_id,
            user_id=self.user_id,
            emoji=self.emoji
        )