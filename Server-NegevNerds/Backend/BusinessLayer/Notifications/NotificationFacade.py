from Backend.BusinessLayer.Notifications.LateNotifications import LateNotifications


class NotificationFacade:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
          self.late_notifications = LateNotifications()


    def delete_user_notifications(self , user_id):
        self.late_notifications.remove_user_notifications(user_id)

    def get_user_notifications(self , user_id):
        return self.late_notifications.get_user_notifications(user_id)

    def get_user_last_notifications(self , user_id, number_of_notifications):
        return self.late_notifications.get_last_user_notifications(user_id, number_of_notifications)


    def send_notification(self, sender_id, receiver_id, message , need_approval):
        self.late_notifications.add_notification(receiver_id=receiver_id, sender_id=sender_id, message=message,need_approval=need_approval)

