# task_scheduler/ui/main_window.py
import csv
import os
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk
from .hotkeys import register_hotkeys

from ui.csv_table_panel import CsvTablePanel
from settings_manager import load_settings, add_recent_project


from services.excel_service import (
    export_tasks_to_excel,
    import_tasks_from_excel,
    ExcelDependencyError,
)

from ui.menu_bar import build_menu_bar
from .csv_commands_panel import build_csv_commands_panel


class CsvViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window setup ---
        self.title("CSV Viewer")
        self.geometry("1024x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # current CSV path
        # --- state ---
        self.csv_path: str | None = None   # currently opened CSV
        self.project_path: str | None = None  # currently opened/saved project (YAML)

        # Layout: col 0 = sidebar, col 1 = main area
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=260)  # sidebar width
        self.grid_columnconfigure(1, weight=1)               # main viewer
        
        # LEFT: commands panel
        self.commands_panel = build_csv_commands_panel(self)

        # RIGHT: CSV table panel
        self.csv_panel = CsvTablePanel(self)
        self.csv_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._update_title_with_path()

        # Menu bar
        build_menu_bar(self)
        
        # 🔥 Register global hotkeys
        register_hotkeys(self)

        self._update_title_with_path()
        
        # --- NEW: load settings & auto-open last project if available ---
        self.settings = load_settings()
        recent = self.settings.get("recent_projects", [])
        if recent:
            last_project = recent[0]
            # don't spam error popups on startup; fail silently
            self._open_project_by_path(last_project, show_errors=False)

        self._update_title_with_path()

    # ------------------------------------------------------------------
    # Appearance / Help
    # ------------------------------------------------------------------
    def _update_window_title(self):
        import os
        name = os.path.basename(self.project_path) if self.project_path else "Untitled"
        self.title(f"CsvViewerApp - {name}")

    def _set_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Task Scheduler\n\nBuilt with customtkinter.\n© Osama ElMorady's toolbox 😉"
        )
    # ------------------------------------------------------------------
    # File actions
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # File menu actions
    # ------------------------------------------------------------------
    # -------- File menu: Project handling --------
    def new_project(self):
        """
        Clear current CSV and project info.
        """
        if self.csv_path:
            if not messagebox.askyesno(
                "New Project", "Clear current CSV view and start a new project?"
            ):
                return

        self.csv_path = None
        self.project_path = None
        self.csv_panel.clear_table()
        self._update_title_with_path()

    def open_project(self):
        path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Project YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        self._open_project_by_path(path, show_errors=True)


    def save_project(self):
        if not self.csv_path:
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

            # 🔥 update recent projects & settings
            self.settings = add_recent_project(path)

            messagebox.showinfo("Save Project", f"Project saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Project", f"Failed to save project:\n{e}")


    def _load_project_yaml(self, path: str) -> dict:
        """
        VERY simple YAML reader for key: value pairs.
        Enough for now and still valid YAML for the future.
        """
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

    def _save_project_yaml(self, path: str, data: dict) -> None:
        lines = []
        for key, value in data.items():
            if value is None:
                value = ""
            # basic quoting; you can improve later
            lines.append(f'{key}: "{value}"')
        text = "\n".join(lines) + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


    def _open_project_by_path(self, path: str, show_errors: bool = True):
        """
        Core logic to open a project from a given path.
        Used by both 'Open Project...' and startup auto-load.
        """
        import traceback

        try:
            project = self._load_project_yaml(path)
        except Exception as e:
            if show_errors:
                messagebox.showerror("Open Project", f"Failed to open project:\n{e}")
            else:
                # optional: print to console
                print("Failed to open project on startup:")
                traceback.print_exc()
            return

        self.project_path = path
        self.csv_path = project.get("csv_path") or None

        # Update recent_projects in settings
        self.settings = add_recent_project(path)

        if self.csv_path:
            try:
                rows = self._load_csv_file(self.csv_path)
                self.csv_panel.load_data(rows)
            except Exception as e:
                if show_errors:
                    messagebox.showerror(
                        "Open Project", f"Project loaded, but CSV failed:\n{e}"
                    )
        else:
            self.csv_panel.clear_table()

        self._update_title_with_path()







    # ------------------------------------------------------------------
    # Excel helpers
    # ------------------------------------------------------------------



    def export_to_excel(self):
        """
        Placeholder: you can later export current table to Excel.
        """
        messagebox.showinfo(
            "Export to Excel",
            "Export to Excel is not implemented yet.\n\n"
            "Later, we can export the current CSV table to .xlsx using pandas.",
        )

    def import_from_excel(self):
        """
        Placeholder: you can later import Excel and show it in the table.
        """
        messagebox.showinfo(
            "Import from Excel",
            "Import from Excel is not implemented yet.\n\n"
            "Later, we can load .xlsx and display it like a CSV.",
        )

    
    # ------------------------------------------------------------------
    # CSV helpers
    # ------------------------------------------------------------------
    def create_new_csv(self):
        """
        Create a brand new (empty) CSV file and open it in the viewer.
        If a CSV is already open, it is simply replaced in the UI.
        """
        # Ask the user where to create the new CSV
        initialfile = "new.csv"
        initialdir = os.path.dirname(self.csv_path) if self.csv_path else ""

        path = filedialog.asksaveasfilename(
            title="Create New CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=initialfile,
            initialdir=initialdir or None,
        )

        # User cancelled the dialog
        if not path:
            return

        try:
            # Physically create a new, empty CSV file with one empty cell
            # (A1) so the sheet shows 1 row, 1 column.
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([""])   # one empty cell

            # Update app state to point to this new CSV
            self.csv_path = path

            # Load a single empty cell into the sheet
            self.csv_panel.load_data([[""]])

            # Update window title
            self._update_title_with_path()

            messagebox.showinfo("Create CSV", f"New CSV created:\n{path}")
        except Exception as e:
            messagebox.showerror("Create CSV", f"Failed to create CSV:\n{e}")


    
    def open_csv(self):
        path = filedialog.askopenfilename(
            title="Open CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            rows = self._load_csv_file(path)
        except Exception as e:
            messagebox.showerror("Open CSV", f"Failed to open CSV:\n{e}")
            return

        self.csv_path = path
        self.csv_panel.load_data(rows)
        self._update_title_with_path()

    def reload_csv(self):
        if not self.csv_path:
            messagebox.showinfo("Reload CSV", "No CSV file is currently open.")
            return

        try:
            rows = self._load_csv_file(self.csv_path)
        except Exception as e:
            messagebox.showerror("Reload CSV", f"Failed to reload CSV:\n{e}")
            return

        self.csv_panel.load_data(rows)
        self._update_title_with_path()
        
    def save_csv(self):
        """
        Save the current sheet data to a CSV file.
        """
        rows = self.csv_panel.get_data()
        if not rows:
            messagebox.showinfo("Save CSV", "There is no data to save.")
            return

        # Suggest current file name if we have one
        initialfile = os.path.basename(self.csv_path) if self.csv_path else "data.csv"
        initialdir = os.path.dirname(self.csv_path) if self.csv_path else ""

        path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=initialfile,
            initialdir=initialdir or None,
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)

            self.csv_path = path
            self._update_title_with_path()
            messagebox.showinfo("Save CSV", f"CSV saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save CSV", f"Failed to save CSV:\n{e}")

    
    
    def _load_csv_file(self, path: str):
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # return all rows; viewer will handle headers visually (A, B, C, ...)
        return rows

    def _update_title_with_path(self):
        if not self.csv_path:
            self.title("CSV Viewer")
        else:
            name = os.path.basename(self.csv_path)
            self.title(f"CSV Viewer - {name}")
            
            

    # ------------------------------------------------------------------
    # CSV edit commands (stubs for now)
    # ------------------------------------------------------------------
    def add_row(self):
        messagebox.showinfo("Add Row", "Add Row is not implemented yet.\n(You can implement it later.)")

    def add_column(self):
        messagebox.showinfo("Add Column", "Add Column is not implemented yet.\n(You can implement it later.)")

    def delete_row(self):
        messagebox.showinfo("Delete Row", "Delete Row is not implemented yet.\n(You can implement it later.)")

    def delete_column(self):
        messagebox.showinfo("Delete Column", "Delete Column is not implemented yet.\n(You can implement it later.)")

            


def run_app():
    app = CsvViewerApp()
    app.mainloop()
