import datetime

from sqlalchemy import Column, Integer, String, Boolean, PickleType, ForeignKey, DateTime
from ..Base import Base


class NotificationModel(Base):

    __tablename__ = 'notifications'

    # Primary key
    sender_user_id = Column(String,ForeignKey('users.user_id'), nullable=False)
    receiver_user_id = Column(String,ForeignKey('users.user_id'), nullable=False)
    massage = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now(),  nullable=False)
    notification_id = Column(String, nullable=False, primary_key=True)
    need_approval = Column(Boolean, nullable=False)



    def to_business_model(self):
        from Backend.BusinessLayer.Notifications.Notification import Notification
        if isinstance(self.timestamp, str):
            # If it's already a string, just use it
            timestamp_str = self.timestamp
        elif self.timestamp is None:
            timestamp_str = None
        else:
            # Try to convert to string format
            try:
                timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                # Fallback to string conversion if all else fails
                timestamp_str = str(self.timestamp) if self.timestamp else None

        notification = Notification(
            sender_user_id=self.sender_user_id,
            receiver_user_id=self.receiver_user_id,
            message=self.massage,
            timestamp=timestamp_str,
            notification_id=self.notification_id,
            need_approval=self.need_approval
        )
        return notification

    @classmethod
    def from_business_model(cls, notification):
        return cls(
            notification_id=notification.notification_id,
            sender_user_id = notification.sender_user_id,
            receiver_user_id = notification.receiver_user_id,
            message = notification.massage,
            timestamp = notification.timestamp,
            need_approval = notification.need_approval
        )
        pass
