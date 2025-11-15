# task_scheduler/services/notification_service.py
from tkinter import messagebox
from models import Task


class NotificationPort:
    """
    Simple interface / base class for notification backends.
    You can subclass this for different implementations (sound, logging, email, etc.).
    """

    def notify_task_due(self, task: Task) -> None:
        raise NotImplementedError


class TkNotificationService(NotificationPort):
    """Default notification implementation using Tk message boxes."""

    def notify_task_due(self, task: Task) -> None:
        message = f"{task.name}\n\n{task.description}"
        messagebox.showinfo("Task Reminder", message)
