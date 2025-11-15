# task_scheduler/storage.py
import json
import os
from typing import List

from models import Task

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            raw_list = json.load(f)
        return [Task.from_dict(d) for d in raw_list]
    except Exception:
        # corrupted file, bad JSON, etc.
        return []


def save_tasks(tasks: List[Task]) -> None:
    ensure_data_dir()
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)
