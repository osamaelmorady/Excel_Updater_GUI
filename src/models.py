# task_scheduler/models.py
from dataclasses import dataclass
from datetime import datetime

DATETIME_FMT = "%Y-%m-%d %H:%M"


@dataclass
class Task:
    name: str
    datetime_str: str                  # e.g. "2025-11-15 14:30"
    repeat: str = "None"               # "None", "Daily", "Weekly"
    description: str = ""
    done: bool = False

    # future-ready fields (you can start using them later)
    priority: str = "Normal"           # "Low", "Normal", "High"
    category: str = "General"          # "Work", "Personal", ...

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            name=data.get("name", ""),
            datetime_str=data.get("datetime", ""),
            repeat=data.get("repeat", "None"),
            description=data.get("description", ""),
            done=data.get("done", False),
            priority=data.get("priority", "Normal"),
            category=data.get("category", "General"),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "datetime": self.datetime_str,
            "repeat": self.repeat,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "category": self.category,
        }

    def as_datetime(self) -> datetime:
        return datetime.strptime(self.datetime_str, DATETIME_FMT)

    @classmethod
    def build(
        cls,
        name: str,
        date_str: str,
        time_str: str,
        repeat: str,
        description: str,
        priority: str = "Normal",
        category: str = "General",
    ) -> "Task":
        dt = datetime.strptime(f"{date_str} {time_str}", DATETIME_FMT)
        return cls(
            name=name,
            datetime_str=dt.strftime(DATETIME_FMT),
            repeat=repeat,
            description=description,
            priority=priority,
            category=category,
            done=False,
        )
