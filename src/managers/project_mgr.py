# task_scheduler/ui/project_api.py

import traceback
from tkinter import messagebox, filedialog
from pathlib import Path
from managers.settings_mgr import Settings
from services.excel_service import save_excel_workbook, load_excel_workbook

class project_mgr:
    """
    Standalone version — no dependency on Settings or excel_mgr.

    Provides:
    - new_project
    - open_project
    - save_project
    - _open_project_by_path
    - _load_project_yaml
    - _save_project_yaml

    Expects the following attributes ON SELF:
    - self.project_path
    - self.data_path
    - self.csv_panel (optional)
    - self._update_title_with_path()  (optional)
    """

    # ---------------------------------------------------------
    # New Project
    # ---------------------------------------------------------
    def new_project(self):
        """Clear current workbook/data & project info."""
        if getattr(self, "data_path", None):
            if not messagebox.askyesno(
                "New Project",
                "Clear current data file and start a new project?"
            ):
                return

        self.data_path = None
        self.project_path = None

        # Clear UI if available
        # if hasattr(self, "csv_panel") and hasattr(self.csv_panel, "clear_table"):
        #     self.csv_panel.clear_table()

        # if hasattr(self, "_update_title_with_path"):
        #     self._update_title_with_path()

    # ---------------------------------------------------------
    # Open Project (YAML)
    # ---------------------------------------------------------
    def open_project(self):
        path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Project YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        self._open_project_by_path(path, show_errors=True)

    # ---------------------------------------------------------
    # Save Project
    # ---------------------------------------------------------
    def save_project(self):
        if not self.data_path:
            if not messagebox.askyesno(
                "Save Project",
                "Project has no Excel file. Save anyway?"
            ):
                return
    
        path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".yaml",
            filetypes=[("Project YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return
    
        project_data = {"data_path": self.data_path or ""}
    
        try:
            self._save_project_yaml(path, project_data)
            self.project_path = path
    
            # update settings
            self.settings.add_recent_project(path)
            if self.data_path:
                self.settings.add_recent_data(self.data_path)
    
            messagebox.showinfo("Save Project", f"Project saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
    


    # ---------------------------------------------------------
    # INTERNAL: Open existing project
    # ---------------------------------------------------------
    def _open_project_by_path(self, path: str, show_errors: bool = True):
        """
        Load project YAML and restore associated Excel file path.
        """
    
        # ---------- FIX: ensure settings exists ----------
        if not hasattr(self, "settings"):
            class DummySettings:
                def add_recent_project(self, *a): pass
                def add_recent_data(self, *a): pass
            self.settings = DummySettings()
        # -------------------------------------------------
    
        # Load YAML
        try:
            project = self._load_project_yaml(path)
        except Exception as e:
            if show_errors:
                messagebox.showerror("Open Project", f"Failed to load project file:\n{e}")
            return
    
        self.project_path = path
        self.data_path = project.get("data_path") or None
    
        # Update recent project
        self.settings.add_recent_project(path)
    
        # ------------------------------------------
        # Load Excel file if path exists
        # ------------------------------------------
        if self.data_path:
            excel_path = Path(self.data_path)
            if excel_path.exists():
                try:
                    workbook = load_excel_workbook(excel_path)
                    self.current_excel_workbook = workbook
    
                    # Update settings → recent Excel list
                    self.settings.add_recent_data(self.data_path)
    
                    # Notify GUI if supported
                    # if hasattr(self, "_on_excel_loaded"):
                    #     self._on_excel_loaded(workbook)
    
                except Exception as exc:
                    if show_errors:
                        messagebox.showerror(
                            "Error",
                            f"Project opened but Excel failed to load:\n{exc}"
                        )
            else:
                if show_errors:
                    messagebox.showwarning(
                        "Missing File",
                        f"The Excel file does not exist:\n{self.data_path}"
                    )
                if hasattr(self, "csv_panel"):
                    self.csv_panel.clear_table()
    
        else:
            # No excel path in YAML
            if hasattr(self, "csv_panel"):
                self.csv_panel.clear_table()
    
        if hasattr(self, "_update_title_with_path"):
            self._update_title_with_path()
    

    # ---------------------------------------------------------
    # INTERNAL: Load YAML
    # ---------------------------------------------------------
    def _load_project_yaml(self, path: str) -> dict:
        """Minimal YAML reader for simple key: value pairs."""
        project = {}
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

    # ---------------------------------------------------------
    # INTERNAL: Save YAML
    # ---------------------------------------------------------
    def _save_project_yaml(self, path: str, data: dict) -> None:
        lines = []
        for key, value in data.items():
            if value is None:
                value = ""
            lines.append(f'{key}: "{value}"')
        text = "\n".join(lines) + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
