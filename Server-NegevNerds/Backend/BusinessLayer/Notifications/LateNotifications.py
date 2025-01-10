import uuid
from datetime import datetime

from Backend.BusinessLayer.Notifications.Notification import Notification
from Backend.DataLayer.Noitifications.NotificationRepository import NotificationRepository


class LateNotifications:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        """
        Initialize a LateNotifications instance.
        The notifications attribute is a dictionary where the key is the user ID
        and the value is a list of notifications for that user.
        """
        #self.notifications = {}

    def add_notification(self, sender_id, message, receiver_id,need_approval=False):
        notification_id = self.generateNotificationId()
        #if receiver_id not in self.notifications:
        #    self.notifications[receiver_id] = []
        #self.notifications[receiver_id].append(
        Notification.create(sender_user_id=sender_id,notification_id=notification_id, receiver_user_id=receiver_id, message=message, timestamp=datetime.now(),  need_approval=need_approval)

    def generateNotificationId(self):
        return "notification-" + str(uuid.uuid4())



    def get_notification(self, user_id, notification_id):
        """
        Retrieve all notifications for a specific user.

        :param user_id: The ID of the user whose notifications are to be retrieved.
        :return: A list of notifications for the specified user, or an empty list if none exist.
        """
        #if user_id in self.notifications:
        #    if notification_id in self.notifications[user_id]:
        #        return self.notifications[user_id][notification_id]

        notifications_repo = NotificationRepository()
        notification = notifications_repo.get_notifications_by_user_id(user_id=user_id)
        return notification


    def get_user_notifications(self, user_id):
        """
        Retrieve all notifications for a specific user.

        :param user_id: The ID of the user whose notifications are to be retrieved.
        :return: A list of notifications for the specified user, or an empty list if none exist.
        """
        dtos = []
        notifications_repo = NotificationRepository()
        notifications = notifications_repo.get_notifications_by_user_id(user_id=user_id)
        for notification in notifications:
            dtos.append(notification.to_dto())
        #sorted_notifications = sorted(notifications, key=lambda n: n.timestamp, reverse=True)
        return dtos


    def get_last_user_notifications(self, user_id, number_of_notifications):
        """
        Retrieve all notifications for a specific user.

        :param user_id: The ID of the user whose notifications are to be retrieved.
        :return: A list of notifications for the specified user, or an empty list if none exist.
        """
        dtos = []
        notifications_repo = NotificationRepository()
        notifications = notifications_repo.get_last_notifications_by_user_id(user_id=user_id, number_of_notifications=number_of_notifications)
        for notification in notifications:
            dtos.append(notification.to_dto())
        #sorted_notifications = sorted(notifications, key=lambda n: n.timestamp, reverse=True)
        return dtos

    def remove_user_notifications(self, user_id):
        """
        Remove all notifications for a specific user.

        :param user_id: The ID of the user whose notifications are to be removed.
        """
        #if user_id in self.notifications:
        #    del self.notifications[user_id]

        notifications_repo = NotificationRepository()
        notifications_repo.delete_notifications_by_user(user_id=user_id)

    def remove_notification(self, user_id, notification_id):
        """
        Remove all notifications for a specific user.

        :param user_id: The ID of the user whose notifications are to be removed.
        """
        #if user_id in self.notifications:
        #    del self.notifications[user_id]

        notifications_repo = NotificationRepository()
        notifications_repo.delete_notification(notification_id=notification_id)


