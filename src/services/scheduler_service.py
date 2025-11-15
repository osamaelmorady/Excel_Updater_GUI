# task_scheduler/services/scheduler_service.py
from datetime import datetime, timedelta
from typing import List

from models import Task, DATETIME_FMT
from .notification_service import NotificationPort


class SchedulerService:
    """
    Core scheduling logic:
    - decides when tasks are due
    - marks them done or moves them forward if repeating
    - delegates notification to a NotificationPort implementation
    """

    def __init__(self, tasks: List[Task], notifier: NotificationPort):
        self.tasks = tasks
        self.notifier = notifier

    def check_due_tasks(self, now: datetime | None = None) -> None:
        """Check for tasks due at `now` (default = datetime.now())."""
        if now is None:
            now = datetime.now()

        for task in self.tasks:
            if task.done:
                continue

            task_dt = task.as_datetime()
            # 60s window to trigger
            if now >= task_dt and (now - task_dt).total_seconds() < 60:
                self.notifier.notify_task_due(task)
                self._handle_repeating_task(task, now)

    def _handle_repeating_task(self, task: Task, now: datetime) -> None:
        repeat = task.repeat
        task_dt = task.as_datetime()

        if repeat == "None":
            task.done = True
            return

        if repeat == "Daily":
            while task_dt <= now:
                task_dt += timedelta(days=1)
        elif repeat == "Weekly":
            while task_dt <= now:
                task_dt += timedelta(weeks=1)

        task.datetime_str = task_dt.strftime(DATETIME_FMT)
        task.done = False
