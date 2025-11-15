# task_scheduler/ui/main_window.py
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk

from models import Task
from storage import (
    load_tasks,
    save_tasks,
    load_tasks_from,
    save_tasks_to,
    TASKS_FILE,
)
from services.scheduler_service import SchedulerService
from services.notification_service import TkNotificationService
from services.excel_service import (
    export_tasks_to_excel,
    import_tasks_from_excel,
    ExcelDependencyError,
)

# NEW: import UI builders
from ui.menu_bar import build_menu_bar
from ui.task_form_panel import build_task_form_panel
from ui.task_list_panel import build_task_list_panel


class TaskSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # current project path
        self.project_path: str = TASKS_FILE

        # --- Window setup ---
        self.title("Task Scheduler")
        self.geometry("1024x800")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Internal storage: list[Task]
        self.tasks: list[Task] = load_tasks()

        # Scheduler + notifier services
        self.notifier = TkNotificationService()
        self.scheduler = SchedulerService(self.tasks, self.notifier)

        # Build menu bar (in separate module)
        build_menu_bar(self)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Build panels (in separate modules)
        build_task_form_panel(self)
        build_task_list_panel(self)

        self.refresh_listbox()
        self.check_tasks_loop()
        self._update_window_title()

    # ------------------------------------------------------------------
    # Window / appearance helpers
    # ------------------------------------------------------------------
    def _update_window_title(self):
        import os
        name = os.path.basename(self.project_path) if self.project_path else "Untitled"
        self.title(f"Task Scheduler - {name}")

    def _set_appearance_mode(self, mode: str):
        ctk.set_appearance_mode(mode)

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Task Scheduler\n\nBuilt with customtkinter.\n© Osama ElMorady's toolbox 😉"
        )

    # ------------------------------------------------------------------
    # Task operations
    # ------------------------------------------------------------------
    def add_or_update_task(self):
        name = self.entry_name.get().strip()
        date_str = self.entry_date.get().strip()
        time_str = self.entry_time.get().strip()
        repeat = self.option_repeat.get()
        desc = self.text_desc.get("1.0", "end").strip()

        if not name or not date_str or not time_str:
            messagebox.showerror("Error", "Please fill in task name, date, and time.")
            return

        try:
            task = Task.build(
                name=name,
                date_str=date_str,
                time_str=time_str,
                repeat=repeat,
                description=desc,
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index] = task
        else:
            self.tasks.append(task)

        self.refresh_listbox()
        self.clear_form(auto_keep_selection=False)

    def delete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a task to delete.")
            return

        index = selection[0]
        del self.tasks[index]
        self.refresh_listbox()

    def on_task_selected(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        task = self.tasks[index]

        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, task.name)

        dt = task.as_datetime()
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, dt.strftime("%Y-%m-%d"))

        self.entry_time.delete(0, "end")
        self.entry_time.insert(0, dt.strftime("%H:%M"))

        self.option_repeat.set(task.repeat)

        self.text_desc.delete("1.0", "end")
        self.text_desc.insert("1.0", task.description)

    def clear_form(self, auto_keep_selection=True):
        self.entry_name.delete(0, "end")
        self.entry_date.delete(0, "end")
        self.entry_time.delete(0, "end")
        self.option_repeat.set("None")
        self.text_desc.delete("1.0", "end")
        if not auto_keep_selection:
            self.listbox.selection_clear(0, "end")

    def refresh_listbox(self):
        self.listbox.delete(0, "end")
        for task in self.tasks:
            done_flag = "✔" if task.done else " "
            display = f"[{done_flag}] {task.datetime_str} | {task.name} ({task.repeat})"
            self.listbox.insert("end", display)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _save_tasks_to_disk(self):
        try:
            save_tasks_to(self.tasks, self.project_path)
            messagebox.showinfo("Saved", "Tasks saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save tasks:\n{e}")

    def _reload_tasks_from_disk(self):
        try:
            self.tasks = load_tasks_from(self.project_path)
            self.scheduler.tasks = self.tasks
            self.refresh_listbox()
            messagebox.showinfo("Reloaded", "Tasks reloaded from disk.")
        except Exception as e:
            messagebox.showerror("Reload Error", f"Failed to reload tasks:\n{e}")

    # ------------------------------------------------------------------
    # Scheduler integration
    # ------------------------------------------------------------------
    def check_tasks_loop(self):
        self.scheduler.check_due_tasks()
        self.refresh_listbox()
        self.after(30000, self.check_tasks_loop)

    # ------------------------------------------------------------------
    # File menu actions
    # ------------------------------------------------------------------
    def new_project(self):
        if self.tasks:
            if not messagebox.askyesno("New Project", "Clear current tasks and start a new project?"):
                return

        self.tasks.clear()
        self.project_path = TASKS_FILE
        self.refresh_listbox()
        self._update_window_title()

    def open_project(self):
        path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Task YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        self.project_path = path
        self.tasks = load_tasks_from(path)
        self.scheduler.tasks = self.tasks
        self.refresh_listbox()
        self._update_window_title()

    def save_project(self):
        path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".yaml",
            filetypes=[("Task YAML files", "*.yaml"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            save_tasks_to(self.tasks, path)
            self.project_path = path
            self.scheduler.tasks = self.tasks
            self._update_window_title()
            messagebox.showinfo("Save Project", f"Project saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Project", f"Failed to save project:\n{e}")

    def export_to_excel(self):
        if not self.tasks:
            messagebox.showinfo("Export to Excel", "There are no tasks to export.")
            return

        path = filedialog.asksaveasfilename(
            title="Export to Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
        )
        if not path:
            return

        try:
            export_tasks_to_excel(self.tasks, path)
            messagebox.showinfo("Export to Excel", f"Tasks exported to:\n{path}")
        except ExcelDependencyError as e:
            messagebox.showerror("Excel Export", str(e))
        except Exception as e:
            messagebox.showerror("Excel Export", f"Failed to export tasks:\n{e}")

    def import_from_excel(self):
        path = filedialog.askopenfilename(
            title="Import from Excel",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            imported = import_tasks_from_excel(path)
        except ExcelDependencyError as e:
            messagebox.showerror("Excel Import", str(e))
            return
        except Exception as e:
            messagebox.showerror("Excel Import", f"Failed to import tasks:\n{e}")
            return

        if not imported:
            messagebox.showinfo("Excel Import", "No tasks found in the selected file.")
            return

        self.tasks.extend(imported)
        self.scheduler.tasks = self.tasks
        self.refresh_listbox()
        messagebox.showinfo("Excel Import", f"Imported {len(imported)} tasks.")


def run_app():
    app = TaskSchedulerApp()
    app.mainloop()
