# task_scheduler/ui/project_api.py
import os
import traceback
from tkinter import messagebox, filedialog

from settings_mgr import add_recent_project


class ProjectApiMixin:
    """
    Mixin providing project-level APIs:
    - new_project
    - open_project
    - save_project
    - _open_project_by_path
    - _load_project_yaml
    - _save_project_yaml

    Expects the following attributes on self:
    - self.csv_path
    - self.project_path
    - self.csv_panel (with .clear_table() and .load_data())
    - self.settings
    - self._update_title_with_path()
    - self._load_csv_file(path: str)
    """

    def new_project(self):
        """
        Clear current CSV and project info.
        """
        if getattr(self, "csv_path", None):
            if not messagebox.askyesno(
                "New Project", "Clear current CSV view and start a new project?"
            ):
                return

        self.csv_path = None
        self.project_path = None

        # Clear the table UI
        # if getattr(self, "csv_panel", None) is not None:
        #     self.csv_panel.clear_table()

        # self._update_title_with_path()

    def open_project(self):
        path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Project YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        self._open_project_by_path(path, show_errors=True)

    def save_project(self):
        if not getattr(self, "csv_path", None):
            if not messagebox.askyesno(
                "Save Project",
                "No CSV is open. Save project anyway (without CSV path)?",
            ):
                return

        path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".yaml",
            filetypes=[("Project YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        project_data = {
            "csv_path": self.csv_path or "",
        }

        try:
            self._save_project_yaml(path, project_data)
            self.project_path = path

            # Update recent projects & settings
            self.settings = add_recent_project(path)

            messagebox.showinfo("Save Project", f"Project saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Project", f"Failed to save project:\n{e}")

    # ----------------- internal helpers -----------------

    def _open_project_by_path(self, path: str, show_errors: bool = True):
        """
        Core logic to open a project from a given path.
        Used by both 'Open Project...' and startup auto-load.
        """
        try:
            project = self._load_project_yaml(path)
        except Exception as e:
            if show_errors:
                messagebox.showerror("Open Project", f"Failed to open project:\n{e}")
            else:
                print("Failed to open project on startup:")
                traceback.print_exc()
            return

        self.project_path = path
        self.csv_path = project.get("csv_path") or None

        # Update recent_projects in settings
        self.settings = add_recent_project(path)

        # if self.csv_path:
        #     try:
        #         rows = self._load_csv_file(self.csv_path)
        #         self.csv_panel.load_data(rows)
        #     except Exception as e:
        #         if show_errors:
        #             messagebox.showerror(
        #                 "Open Project", f"Project loaded, but CSV failed:\n{e}"
        #             )
        # else:
        #     # no CSV path stored in project -> clear the view
        #     self.csv_panel.clear_table()

        # self._update_title_with_path()

    def _load_project_yaml(self, path: str) -> dict:
        """
        VERY simple YAML reader for key: value pairs.
        Enough for now and still valid YAML for the future.
        """
        project: dict[str, str] = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                project[key] = value
        return project

    def _save_project_yaml(self, path: str, data: dict) -> None:
        lines = []
        for key, value in data.items():
            if value is None:
                value = ""
            lines.append(f'{key}: "{value}"')
        text = "\n".join(lines) + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
