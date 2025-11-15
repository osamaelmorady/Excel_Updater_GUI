# task_scheduler/ui/main_window.py
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from models import Task
from storage import load_tasks, save_tasks
from services.scheduler_service import SchedulerService
from services.notification_service import TkNotificationService


class TaskSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window setup ---
        self.title("Task Scheduler")
        self.geometry("800x500")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Internal storage: list[Task]
        self.tasks: list[Task] = load_tasks()

        # Scheduler + notifier services
        self.notifier = TkNotificationService()
        self.scheduler = SchedulerService(self.tasks, self.notifier)

        self.build_menu_bar()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

        self.refresh_listbox()
        self.check_tasks_loop()
        
        
    def build_menu_bar(self):
        """Create the top menu bar: File, Edit, Appearance, Help."""
        menubar = tk.Menu(self)

        # ---------- File menu ----------
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Tasks", command=self._save_tasks_to_disk)
        file_menu.add_command(label="Reload Tasks", command=self._reload_tasks_from_disk)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # ---------- Edit menu ----------
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear Form", command=self.clear_form)
        edit_menu.add_command(label="Delete Selected Task", command=self.delete_task)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # ---------- Appearance menu ----------
        appearance_menu = tk.Menu(menubar, tearoff=0)
        appearance_menu.add_radiobutton(
            label="System",
            command=lambda: self._set_appearance_mode("System")
        )
        appearance_menu.add_radiobutton(
            label="Light",
            command=lambda: self._set_appearance_mode("Light")
        )
        appearance_menu.add_radiobutton(
            label="Dark",
            command=lambda: self._set_appearance_mode("Dark")
        )
        menubar.add_cascade(label="Appearance", menu=appearance_menu)

        # ---------- Help menu ----------
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Attach to window
        self.config(menu=menubar)

    def _set_appearance_mode(self, mode: str):
        """Change global appearance mode for customtkinter."""
        ctk.set_appearance_mode(mode)

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Task Scheduler\n\nBuilt with customtkinter.\n© Osama ElMorady's toolbox 😉"
        )


    # ------------------------------------------------------------------
    # UI building
    # ------------------------------------------------------------------
    def _build_left_panel(self):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(frame, text="New Task", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, pady=(10, 15))

        # Task name
        ctk.CTkLabel(frame, text="Task name:").grid(row=1, column=0, sticky="w", padx=10)
        self.entry_name = ctk.CTkEntry(frame, placeholder_text="e.g. Pay bills")
        self.entry_name.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Date
        ctk.CTkLabel(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10)
        self.entry_date = ctk.CTkEntry(frame, placeholder_text="2025-11-15")
        self.entry_date.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Time
        ctk.CTkLabel(frame, text="Time (HH:MM):").grid(row=5, column=0, sticky="w", padx=10)
        self.entry_time = ctk.CTkEntry(frame, placeholder_text="14:30")
        self.entry_time.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Repeat
        ctk.CTkLabel(frame, text="Repeat:").grid(row=7, column=0, sticky="w", padx=10)
        self.option_repeat = ctk.CTkOptionMenu(
            frame,
            values=["None", "Daily", "Weekly"],
        )
        self.option_repeat.set("None")
        self.option_repeat.grid(row=8, column=0, sticky="ew", padx=10, pady=(0, 10))

        # (Future) priority / category widgets can be added here easily

        # Description
        ctk.CTkLabel(frame, text="Description (optional):").grid(row=9, column=0, sticky="w", padx=10)
        self.text_desc = ctk.CTkTextbox(frame, height=80)
        self.text_desc.grid(row=10, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame.grid_rowconfigure(10, weight=1)

        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=11, column=0, pady=10)

        self.btn_add = ctk.CTkButton(btn_frame, text="Add / Update Task", command=self.add_or_update_task)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_clear = ctk.CTkButton(btn_frame, text="Clear Form", command=self.clear_form)
        self.btn_clear.grid(row=0, column=1, padx=5)

    def _build_right_panel(self):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(frame, text="Scheduled Tasks", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, pady=(10, 5))

        self.listbox = tk.Listbox(frame, height=15)
        self.listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.listbox.bind("<<ListboxSelect>>", self.on_task_selected)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=10)

        self.btn_delete = ctk.CTkButton(btn_frame, text="Delete Task", command=self.delete_task)
        self.btn_delete.grid(row=0, column=0, padx=5)

        self.btn_save = ctk.CTkButton(btn_frame, text="Save Tasks", command=self._save_tasks_to_disk)
        self.btn_save.grid(row=0, column=1, padx=5)

        self.btn_reload = ctk.CTkButton(btn_frame, text="Reload from File", command=self._reload_tasks_from_disk)
        self.btn_reload.grid(row=0, column=2, padx=5)

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
                # priority/category default for now
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
            # priority displayed later if you like: f"{task.priority}"
            display = f"[{done_flag}] {task.datetime_str} | {task.name} ({task.repeat})"
            self.listbox.insert("end", display)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _save_tasks_to_disk(self):
        save_tasks(self.tasks)
        messagebox.showinfo("Saved", "Tasks saved successfully.")

    def _reload_tasks_from_disk(self):
        self.tasks = load_tasks()
        self.scheduler.tasks = self.tasks  # keep scheduler in sync
        self.refresh_listbox()
        messagebox.showinfo("Reloaded", "Tasks reloaded from disk.")

    # ------------------------------------------------------------------
    # Scheduler integration
    # ------------------------------------------------------------------
    def check_tasks_loop(self):
        """Call scheduler service periodically."""
        self.scheduler.check_due_tasks()
        self.refresh_listbox()
        self.after(30000, self.check_tasks_loop)
        


def run_app():
    app = TaskSchedulerApp()
    app.mainloop()
