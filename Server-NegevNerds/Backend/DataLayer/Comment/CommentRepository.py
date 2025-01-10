import os

from requests import delete
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.DataLayer.Comment.CommentModel import Base, CommentModel


class CommentRepository:

    def __init__(self, db_path=None, session=None):
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
        if session is None:
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.Session = session

    def add_comment(self, comment, question_id):

        session = self.Session()
        try:
            # Convert business model to SQLAlchemy model
            comment_model = CommentModel(
                comment_id=comment.comment_id,
                writer_name=comment.writer_name,
                writer_id = comment.writer_id,
                date=comment.date,
                prev_id=comment.prev_id,
                text=comment.comment_text,
                deleted=comment.deleted,
                question_id=question_id
            )

            session.add(comment_model)
            session.commit()

            # Get the auto-generated ID

            return
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_comment_by_id(self, comment_id):

        session = self.Session()
        try:
            comment_model = session.query(CommentModel).filter_by(comment_id=comment_id).first()
            return comment_model.to_business_model() if comment_model else None
        finally:
            session.close()



    def update_deleted_comment(self, comment):

        session = self.Session()
        try:

            comment_model = session.query(CommentModel).filter_by(comment_id=comment.comment_id).first()

            if not comment_model:
                raise ValueError(f"No comment found with ID {comment.comment_id}")

            # Update field
            comment_model.deleted = 1

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_comment(self, comment_id):

        session = self.Session()
        try:
            comment_model = session.query(CommentModel).filter_by(comment_id=comment_id).first()

            if not comment_model:
                raise ValueError(f"No comment found with ID {comment_id}")

            session.delete(comment_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete_comments_by_question_id(self, question_id):
        """
        Deletes all comments associated with a specific question ID.

        Args:
            question_id (str): The ID of the question whose comments should be deleted.
        """
        session = self.Session()
        try:
            # Query to find all comments for the given question_id
            comments = session.query(CommentModel).filter_by(question_id=question_id).all()

            # Delete all retrieved comments
            for comment in comments:
                session.delete(comment)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_comment_ids_by_question_id(self, question_id):
        """
        Retrieves all comment IDs associated with a specific question ID.

        Args:
            question_id (str): The ID of the question whose comment IDs should be retrieved.

        Returns:
            List[int]: A list of comment IDs.
        """
        session = self.Session()
        try:
            # Query to find all comments for the given question_id
            comment_ids = session.query(CommentModel.comment_id).filter_by(question_id=question_id).all()

            # Extract IDs from the query result
            return [comment_id[0] for comment_id in comment_ids]
        except Exception as e:
            raise Exception(f"Error retrieving comment IDs: {str(e)}")
        finally:
            session.close()

    def get_comments_metadata_by_question_id(self, question_id):
        """
        Fetch all comment IDs and their writer IDs for a specific question ID.

        Args:
            question_id (str): The ID of the question.

        Returns:
            list[dict]: A list of dictionaries with comment ID and writer ID.
        """
        session = self.Session()
        try:
            # Query to fetch comment ID and writer ID
            comments = session.query(CommentModel.comment_id, CommentModel.writer_id).filter_by(question_id=question_id).all()
            return [{"comment_id": comment.comment_id, "writer_id": comment.writer_id} for comment in comments]
        except Exception as e:
            raise Exception(f"Error fetching comments metadata: {str(e)}")
        finally:
            session.close()
    

    def get_replies_by_comment_id(self, comment_id):
        """
        Retrieves all comments where their prev_id matches the given comment_id.

        Args:
            comment_id (int): The ID of the comment whose replies should be retrieved.

        Returns:
            list[CommentModel]: A list of comments that are replies to the given comment ID.
        """
        session = self.Session()
        try:
            # Query to find all comments with prev_id equal to the given comment_id
            replies = session.query(CommentModel).filter_by(prev_id=comment_id).all()
            return [reply.to_business_model() for reply in replies]
        except Exception as e:
            raise Exception(f"Error retrieving replies for comment ID {comment_id}: {str(e)}")
        finally:
            session.close()

    
    def get_prev_id_by_comment_id(self, comment_id):
        """
        Retrieves the prev_id for a given comment_id.

        Args:
            comment_id (int): The ID of the comment whose prev_id should be retrieved.

        Returns:
            int or None: The prev_id of the comment, or None if the comment is not found.
        """
        session = self.Session()
        try:
            # Query to find the comment with the given comment_id
            comment = session.query(CommentModel).filter_by(comment_id=comment_id).first()
            return comment.prev_id if comment else None
        except Exception as e:
            raise Exception(f"Error retrieving prev_id for comment ID {comment_id}: {str(e)}")
        finally:
            session.close()


    def update_replies_prev_id(self, replies_to_comment, comment_prev):
        """
        Updates the prev_id of all comments in replies_to_comment to comment_prev.

        Args:
            replies_to_comment (list): A list of comment models (or dictionaries) representing the replies.
            comment_prev (int): The new prev_id to set for the replies.
        """
        session = self.Session()
        try:
            # Iterate over all replies and update their prev_id
            for reply in replies_to_comment:
                comment = session.query(CommentModel).filter_by(comment_id=reply.comment_id).first()
                if comment:
                    comment.prev_id = comment_prev  # Update prev_id

            session.commit()  # Commit all changes
        except Exception as e:
            session.rollback()
            raise Exception(f"Error updating replies prev_id: {str(e)}")
        finally:
            session.close()



