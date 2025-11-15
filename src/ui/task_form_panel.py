# task_scheduler/ui/task_form_panel.py
import customtkinter as ctk


def build_task_form_panel(app: "TaskSchedulerApp"):
    """
    Build the left panel with task inputs:
    - Task name, Date, Time, Repeat, Description
    - Add/Update, Clear buttons

    Widgets are attached to `app` as attributes:
    app.entry_name, app.entry_date, app.entry_time,
    app.option_repeat, app.text_desc, etc.
    """
    frame = ctk.CTkFrame(app, corner_radius=10)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)

    title_label = ctk.CTkLabel(frame, text="New Task", font=ctk.CTkFont(size=18, weight="bold"))
    title_label.grid(row=0, column=0, pady=(10, 15))

    # Task name
    ctk.CTkLabel(frame, text="Task name:").grid(row=1, column=0, sticky="w", padx=10)
    app.entry_name = ctk.CTkEntry(frame, placeholder_text="e.g. Pay bills")
    app.entry_name.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    # Date
    ctk.CTkLabel(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10)
    app.entry_date = ctk.CTkEntry(frame, placeholder_text="2025-11-15")
    app.entry_date.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

    # Time
    ctk.CTkLabel(frame, text="Time (HH:MM):").grid(row=5, column=0, sticky="w", padx=10)
    app.entry_time = ctk.CTkEntry(frame, placeholder_text="14:30")
    app.entry_time.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

    # Repeat
    ctk.CTkLabel(frame, text="Repeat:").grid(row=7, column=0, sticky="w", padx=10)
    app.option_repeat = ctk.CTkOptionMenu(
        frame,
        values=["None", "Daily", "Weekly"],
    )
    app.option_repeat.set("None")
    app.option_repeat.grid(row=8, column=0, sticky="ew", padx=10, pady=(0, 10))

    # Description
    ctk.CTkLabel(frame, text="Description (optional):").grid(row=9, column=0, sticky="w", padx=10)
    app.text_desc = ctk.CTkTextbox(frame, height=80)
    app.text_desc.grid(row=10, column=0, sticky="nsew", padx=10, pady=(0, 10))
    frame.grid_rowconfigure(10, weight=1)

    # Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.grid(row=11, column=0, pady=10)

    app.btn_add = ctk.CTkButton(btn_frame, text="Add / Update Task", command=app.add_or_update_task)
    app.btn_add.grid(row=0, column=0, padx=5)

    app.btn_clear = ctk.CTkButton(btn_frame, text="Clear Form", command=app.clear_form)
    app.btn_clear.grid(row=0, column=1, padx=5)

    return frame
