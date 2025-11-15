# task_scheduler/ui/main_window.py
import os
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from managers.settings_mgr import load_settings
from managers.hotkeys_mgr import register_hotkeys
from managers.project_mgr import ProjectApiMixin
from managers.excel_mgr import ExcelApiMixin
from managers.csv_mgr import CsvApiMixin


from ui.excel_panel import CsvTablePanel
from ui.menu_panel import build_menu_bar
from ui.commands_panel import build_excel_panel


class CsvViewerApp(ProjectApiMixin, ExcelApiMixin, CsvApiMixin, ctk.CTk):
    def __init__(self):
        super().__init__(self)

        # --- Window setup ---
        self.title("CSV Viewer")
        self.geometry("1024x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # state
        self.csv_path: str | None = None      # currently opened CSV
        self.project_path: str | None = None  # currently opened/saved project (YAML)

        # Layout: col 0 = sidebar, col 1 = main area
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=260)  # sidebar width
        self.grid_columnconfigure(1, weight=1)               # main viewer

        # LEFT: commands panel
        self.commands_panel = build_excel_panel(self)

        # RIGHT: CSV table panel
        self.csv_panel = CsvTablePanel(self)
        self.csv_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Menu bar
        build_menu_bar(self)

        # Hotkeys
        register_hotkeys(self)

        # Load settings & auto-open last project if available
        self.settings = load_settings()
        recent = self.settings.get("recent_projects", [])
        if recent:
            last_project = recent[0]
            # don't spam error popups on startup; fail silently
            self._open_project_by_path(last_project, show_errors=False)

        # self._update_title_with_path()

    # ------------------------------------------------------------------
    # Appearance / Help
    # ------------------------------------------------------------------
    def _set_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "CSV Viewer / Project Manager\n\nBuilt with customtkinter.\n© Osama ElMorady 😉",
        )

    # ------------------------------------------------------------------
    # Window title helper
    # ------------------------------------------------------------------
    # def _update_title_with_path(self):
    #     if not self.csv_path:
    #         self.title("CSV Viewer")
    #     else:
    #         name = os.path.basename(self.csv_path)
    #         self.title(f"CSV Viewer - {name}")


def run_app():
    app = CsvViewerApp()
    app.mainloop()
