class ReactionDTO:
    def __init__(self, reaction_id, user_id, emoji):
        """
        Data Transfer Object for the Reaction class.
        """
        self.reaction_id = reaction_id
        self.user_id = user_id
        self.emoji = emoji

    def to_dict(self):
        """
        Converts the ReactionDTO instance to a dictionary.

        :return: Dictionary representation of the ReactionDTO.
        """
        return {
            "reaction_id": self.reaction_id,
            "user_id": self.user_id,
            "emoji": self.emoji,
        }