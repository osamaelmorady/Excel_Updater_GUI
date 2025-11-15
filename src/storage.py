# task_scheduler/storage.py
import json
import os
from typing import List

from models import Task

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")  # default project


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_tasks() -> List[Task]:
    """Load from default project file."""
    return load_tasks_from(TASKS_FILE)


def save_tasks(tasks: List[Task]) -> None:
    """Save to default project file."""
    save_tasks_to(tasks, TASKS_FILE)


def load_tasks_from(path: str) -> List[Task]:
    """Load tasks from a specific JSON file path."""
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_list = json.load(f)
        return [Task.from_dict(d) for d in raw_list]
    except Exception:
        return []


def save_tasks_to(tasks: List[Task], path: str) -> None:
    """Save tasks to a specific JSON file path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)
