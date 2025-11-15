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


