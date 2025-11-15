# settings_manager.py
import json
import os

# Adjust this if your settings.json is somewhere else

# Folder where *this* file lives (e.g. .../src)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root = parent of src (one level up)
PROJECT_ROOT = os.path.dirname(_THIS_DIR)

# Config folder under project root
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")

# settings.json inside config
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")


MAX_RECENT = 5


def _default_settings() -> dict:
    return {
        "recent_projects": []  # list of paths (strings)
    }


def load_settings() -> dict:
    """
    Load settings.json if it exists, otherwise return default settings.
    """
    if not os.path.exists(SETTINGS_FILE):
        return _default_settings()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return _default_settings()
        # Ensure key exists
        data.setdefault("recent_projects", [])
        return data
    except Exception:
        # Corrupted / unreadable file -> fall back
        return _default_settings()


def save_settings(settings: dict) -> None:
    """
    Save the settings dict to settings.json.
    """
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def add_recent_project(path: str) -> dict:
    """
    Insert a project path at the top of recent_projects (no duplicates, max 5).
    Returns the updated settings dict.
    """
    settings = load_settings()
    recent = settings.get("recent_projects", [])

    # Remove if already exists, then insert at front
    recent = [p for p in recent if p != path]
    recent.insert(0, path)
    settings["recent_projects"] = recent[:MAX_RECENT]

    save_settings(settings)
    return settings
