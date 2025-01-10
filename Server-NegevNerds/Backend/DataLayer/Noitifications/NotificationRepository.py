import os

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from Backend.DataLayer.Noitifications.NotificationModel import Base
from Backend.DataLayer.Noitifications.NotificationModel import NotificationModel


class NotificationRepository:
    """Repository for handling exam database operations"""
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
    def add_Notification(self, notification):
        """
        Add a new exam to the database

        Args:
            notification (notification): Business layer exam object

        Returns:
            int: ID of the newly created exam
        """
        session = self.Session()
        try:
            # Convert business model to SQLAlchemy model
            notificationModel = NotificationModel(
                sender_user_id= notification.sender_user_id,
                receiver_user_id= notification.receiver_user_id,
                massage= notification.message,
                need_approval= notification.need_approval,
                notification_id=notification.notification_id,
                timestamp= notification.timestamp

            )

            session.add(notificationModel)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_notifications_by_user_id(self, user_id):
        """
        Retrieve a exam by their ID

        Args:
            exam_id (int): exam's unique identifier

        Returns:
            exam: Business layer exam object
        """
        session = self.Session()
        notifications= []
        try:
            notification_model = (session.query(NotificationModel).
                                  filter_by(receiver_user_id=user_id)
                                  .order_by(desc(NotificationModel.timestamp))
                                  .all())
            for notification in notification_model:
                if notification is not None:
                    notifications.append(notification.to_business_model())
            return notifications
        finally:
            session.close()

    def get_last_notifications_by_user_id(self, user_id:str, number_of_notifications:int):
        """
        Retrieve the last 5 notifications for a user by their ID, sorted by time_stamp.

        Args:
            user_id (int): User's unique identifier.

        Returns:
            list: A list of the last 5 notifications as business layer objects.
        """
        session = self.Session()
        notifications = []
        try:
            # Query the database for the last 5 notifications
            notification_model = (
                session.query(NotificationModel)
                .filter_by(receiver_user_id=user_id)
                .order_by(desc(NotificationModel.timestamp))  # Order by time_stamp descending
                .limit(number_of_notifications)
                .all()
            )

            # Convert to business model and return
            for notification in notification_model:
                if notification is not None:
                    notifications.append(notification.to_business_model())
            return notifications
        finally:
            session.close()


    def delete_notification(self,notification_id):

        session = self.Session()
        try:
            notification_model = session.query(NotificationModel).filter_by(notification_id=notification_id).first()

            if not notification_model:
                raise ValueError(f"No notification found with id {notification_id}")

            session.delete(notification_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_notifications_by_user(self, user_id):

        session = self.Session()
        try:
            notification_model = session.query(NotificationModel).filter_by(receiver_user_id=user_id).all()

            if not notification_model:
                raise ValueError(f"No notification found for  {user_id}")

            session.delete(notification_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


