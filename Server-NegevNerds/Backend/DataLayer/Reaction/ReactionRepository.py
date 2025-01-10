import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.Reaction.ReactionModel import Base, ReactionModel


class ReactionRepository:

    def __init__(self, db_path=None):
        """
        Initialize the database engine.

        :param db_path: Path to the SQLite database. If None, uses the default path.
        """
        if db_path is None:
            # Default to a local SQLite database file in the parent directory
            db_path = os.path.join(os.path.dirname(__file__), '../../..', 'NegevNerds.db')

        # Ensure the directory exists
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Use the full path to create the SQLite engine
        #print(f"Resolved database path: {db_path}")
        self.engine = create_engine(f'sqlite:///{db_path}')

        # Ensure all tables are created

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_reaction(self, reaction, comment_id):

        session = self.Session()
        try:
            # Convert business model to SQLAlchemy model
            reaction_model = ReactionModel(
                reaction_id=reaction.reaction_id,
                user_id=reaction.user_id,
                emoji=reaction.emoji,
                comment_id=comment_id
            )

            session.add(reaction_model)
            session.commit()

            # Get the auto-generated ID

            return
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_reaction(self, reaction_id):

        session = self.Session()
        try:
            reaction_model = session.query(ReactionModel).filter_by(reaction_id=reaction_id).first()

            if not reaction_model:
                raise ValueError(f"No reaction found with ID {reaction_id}")

            session.delete(reaction_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    

    def delete_reactions_by_comment_id(self, comment_id):
        """
        Deletes all reactions associated with a specific comment ID.

        Args:
            comment_id (int): ID of the comment whose reactions should be deleted.
        """
        session = self.Session()
        try:
            # Query and delete all reactions for the given comment ID
            reactions = session.query(ReactionModel).filter_by(comment_id=comment_id).all()
            for reaction in reactions:
                session.delete(reaction)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error deleting reactions: {str(e)}")
        finally:
            session.close()


    def delete_reactions_by_comment_ids(self, comment_ids):
        """
        Deletes all reactions associated with a list of comment IDs.

        Args:
            comment_ids (List[int]): List of comment IDs whose reactions should be deleted.
        """
        session = self.Session()
        try:
            # Query and delete all reactions for each comment ID in the list
            for comment_id in comment_ids:
                reactions = session.query(ReactionModel).filter_by(comment_id=comment_id).all()
                for reaction in reactions:
                    session.delete(reaction)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error deleting reactions: {str(e)}")
        finally:
            session.close()
