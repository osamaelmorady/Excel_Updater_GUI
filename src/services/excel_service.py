# task_scheduler/services/excel_service.py
from typing import List

from models import Task

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # we’ll check this at runtime


_COLUMNS = ["name", "datetime", "repeat", "description", "done", "priority", "category"]


class ExcelDependencyError(RuntimeError):
    """Raised when pandas/openpyxl are not available."""
    pass


def _ensure_pandas():
    if pd is None:
        raise ExcelDependencyError(
            "Excel features require 'pandas' and 'openpyxl'.\n"
            "Install them with:\n\npip install pandas openpyxl"
        )


def export_tasks_to_excel(tasks: List[Task], path: str) -> None:
    _ensure_pandas()
    data = [t.to_dict() for t in tasks]
    df = pd.DataFrame(data, columns=_COLUMNS)
    df.to_excel(path, index=False)


def import_tasks_from_excel(path: str) -> List[Task]:
    _ensure_pandas()
    df = pd.read_excel(path)
    tasks: List[Task] = []

    for _, row in df.iterrows():
        d = {
            "name": row.get("name", ""),
            "datetime": str(row.get("datetime", "")),
            "repeat": row.get("repeat", "None"),
            "description": row.get("description", "") or "",
            "done": bool(row.get("done", False)),
            "priority": row.get("priority", "Normal"),
            "category": row.get("category", "General"),
        }
        tasks.append(Task.from_dict(d))
    return tasks
