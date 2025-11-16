# task_scheduler/ui/main_window.py
import os
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from managers.project_mgr import project_mgr
from managers.excel_mgr import excel_mgr
from managers.csv_mgr import csv_mgr
from managers.settings_mgr import Settings
from managers.hotkeys_mgr import register_hotkeys

from ui.excel_panel import ExcelPanel
from ui.menu_panel import build_menu_bar
from ui.commands_panel import build_commands_panel


class ExcelViewerApp(ctk.CTk,Settings,project_mgr,excel_mgr,csv_mgr):
    def __init__(self):
        super().__init__()

        # ------ --- --- --- --- Previous settings setup --- --- --- --- ---
        # Load settings & auto-open last project if available
        self.settings = Settings.load()

        recent = getattr(self.settings, "recent_projects", [])
        last_project = None

        if recent:
            last_project = recent[0]
            # don't spam error popups on startup; fail silently
            self._open_project_by_path(last_project, show_errors=False)

        # state
        self.Excel_path: str | None = None      # currently opened Excel
        self.project_path: str | None = last_project  # currently opened/saved project (YAML)
        # ------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


        # ------ --- --- --- --- Window setup --- --- --- --- ---
        # --- Window setup ---
        self.title("Excel Automator")
        self.geometry("1024x700")
        # Maximize AFTER the window is created (prevents flicker)
        self.after(100, self._maximize_window)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Layout: col 0 = sidebar, col 1 = main area
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=260)  # sidebar width
        self.grid_columnconfigure(1, weight=1)               # main viewer
        # ------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


        # ------ --- --- --- --- Panels setup --- --- --- --- ---
        # LEFT: commands panel
        self.commands_panel = build_commands_panel(self)

        # RIGHT: CSV table panel
        self.excel_panel = ExcelPanel(self)
        self.excel_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # ------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        
        
        
        # ------ --- --- --- --- Menu Bars setup --- --- --- --- ---
        # Menu bar
        build_menu_bar(self)
        # ------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        
        
        
        
        # ------ --- --- --- --- Sepcial functions setup --- --- --- --- ---
        # # # Hotkeys
        register_hotkeys(self)
        # ------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


        # self._update_title_with_path()

    # ------------------------------------------------------------------
    # Appearance / Help
    # ------------------------------------------------------------------
    def _maximize_window(self):
        try:
            self.state("zoomed")   # On Windows this should maximize without hiding taskbar
        except Exception:
            # Fallback in case zoomed isn't supported
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            self.geometry(f"{w}x{h}+0+0")

    def _minimize_window(self):
        try:
            self.geometry("1024x700")
        except Exception:
            # Fallback in case zoomed isn't supported
            return
            
    def _set_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Excel Automator / Project Manager\n\nBuilt with customtkinter.\n© Osama ElMorady 😉",
        )

    def dummy(self):
        return

    # ------------------------------------------------------------------
    # Window title helper
    # ------------------------------------------------------------------
    # def _update_title_with_path(self):
    #     if not self.Excel_path:
    #         self.title("Excel Automator")
    #     else:
    #         name = os.path.basename(self.Excel_path)
    #         self.title(f"Excel Automator - {name}")


def run_app():
    app = ExcelViewerApp()
    app.mainloop()
    
