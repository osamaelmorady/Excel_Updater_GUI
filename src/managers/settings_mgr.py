import json
from pathlib import Path
from typing import Optional, List
import os

# Adjust this if your settings.json is somewhere else
# Project root = parent directory of the folder containing THIS file
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))          # folder of settings_mgr.py
PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, os.pardir, os.pardir))  # parent of _THIS_DIR
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
SETTINGS_FILE_LOC = os.path.join(CONFIG_DIR, "settings.json")
MAX_RECENT = 10


SETTINGS_FILE = Path(SETTINGS_FILE_LOC)


class Settings:
    """
    Robust settings manager with:
    - Automatic file validation
    - Safe loads/saves
    - Backwards compatibility
    - Recent Excel/CSV/project files
    """
    def __init__(self, *args, **kwargs):
        # important: call super() for other base classes
        super().__init__(*args, **kwargs)
        self.recent_projects: List[str] = []
        self.recent_data_files: List[str] = []
        self.last_opened_project: str | None = None
        self.last_opened_data: str | None = None

    # ------------------------------------------------------------------
    # Load settings.json
    # ------------------------------------------------------------------
    @classmethod
    def load(cls) -> "Settings":
        s = cls()
        if not SETTINGS_FILE.exists():
            print("⚠ settings.json not found → Using defaults.")
            return s

        try:       
            raw = SETTINGS_FILE.read_text(encoding="utf-8").lstrip("\ufeff")
            data = json.loads(raw)
        except Exception as e:
            print("❌ Invalid settings.json:", e)
            return s

        # Backwards compatibility support
        s.recent_projects = data.get("recent_projects", []) or []
        s.recent_data_files = data.get("recent_data_files", []) or []

        s.last_opened_project = data.get("last_opened_project")
        s.last_opened_data = data.get("last_opened_data")

        # Legacy keys support (upgrade old projects)
        legacy_excel = data.get("Excel_path")
        if legacy_excel and legacy_excel not in s.recent_data_files:
            s.recent_data_files.insert(0, legacy_excel)
            s.last_opened_data = legacy_excel

        return s

    # ------------------------------------------------------------------
    # Save settings safely
    # ------------------------------------------------------------------
    def save(self):
        data = {
            "recent_projects": self.recent_projects,
            "recent_data_files": self.recent_data_files,
            "last_opened_project": self.last_opened_project,
            "last_opened_data": self.last_opened_data,
        }

        try:
            SETTINGS_FILE.write_text(
                json.dumps(data, indent=4),
                encoding="utf-8"
            )
        except Exception as e:
            print("❌ Failed to save settings:", e)

    # ------------------------------------------------------------------
    # Helpers to update recent lists
    # ------------------------------------------------------------------
    def add_recent_project(self, path: str):
        p = str(Path(path))
        if p in self.recent_projects:
            self.recent_projects.remove(p)
        self.recent_projects.insert(0, p)
        self.last_opened_project = p
        self.save()

    def add_recent_data(self, path: str):
        p = str(Path(path))
        if p in self.recent_data_files:
            self.recent_data_files.remove(p)
        self.recent_data_files.insert(0, p)
        self.last_opened_data = p
        self.save()




import os
from typing import Optional

import yaml  # pip install pyyaml


def get_data_path_from_yaml(yaml_file):
    """
    Read a YAML file and return the value of 'data_path' if present and non-empty.
    
    Returns:
        - str: the data_path value, e.g. "E:/Git/Excel_Updater_GUI/data/123213.xlsx"
        - None: if file doesn't exist, is empty, invalid, or data_path is missing/empty
    """
    # 1) File does not exist
    if not os.path.exists(yaml_file):
        return None

    try:
        # 2) Read content and handle empty file
        with open(yaml_file, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:  # empty or only whitespace
            return None

        # 3) Parse YAML
        data = yaml.safe_load(content)

    except (OSError, yaml.YAMLError):
        # IO error or YAML parsing error
        return None

    # 4) Ensure we got a mapping
    if not isinstance(data, dict):
        return None

    # 5) Extract data_path
    value = data.get("data_path")

    # Handle cases like:
    # data_path:
    # data_path: ""
    if isinstance(value, str) and value.strip():
        return value.strip()

    return None
