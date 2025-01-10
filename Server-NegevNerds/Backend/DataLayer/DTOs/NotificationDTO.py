
class NotificationDTO:

    def __init__(self, receiver_user_id, sender_user_id, message, timestamp, need_approval, notification_id):
        """
        Data Transfer Object for the Notification class.
        """
        self.receiver_user_id = receiver_user_id
        self.sender_user_id = sender_user_id
        self.message = message
        self.timestamp = timestamp
        self.need_approval = need_approval
        self.notification_id = notification_id


    def to_dict(self):
        """
        Converts the NotificationDTO instance to a dictionary.
        """
        return {
            "receiver_user_id": self.receiver_user_id,
            "sender_user_id": self.sender_user_id,
            "message": self.message,
            "timestamp": self.timestamp,
            "need_approval": self.need_approval,
            "notification_id": self.notification_id
        }
