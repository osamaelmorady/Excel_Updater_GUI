# task_scheduler/ui/task_list_panel.py
import tkinter as tk
import customtkinter as ctk


def build_task_list_panel(app: "TaskSchedulerApp"):
    """
    Build the right panel with:
    - Title "Scheduled Tasks"
    - Listbox with vertical + horizontal scrollbars
    - Buttons: Delete, Save, Reload

    Listbox is attached as `app.listbox`.
    """
    frame = ctk.CTkFrame(app, corner_radius=10)
    frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    title_label = ctk.CTkLabel(frame, text="Scheduled Tasks", font=ctk.CTkFont(size=18, weight="bold"))
    title_label.grid(row=0, column=0, pady=(10, 5))

    # Container for listbox + scrollbars
    list_container = ctk.CTkFrame(frame, corner_radius=0, fg_color="transparent")
    list_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    list_container.grid_rowconfigure(0, weight=1)
    list_container.grid_columnconfigure(0, weight=1)

    # Listbox
    app.listbox = tk.Listbox(
        list_container,
        height=15,
        xscrollcommand=None,
        yscrollcommand=None,
    )
    app.listbox.grid(row=0, column=0, sticky="nsew")

    # Scrollbars
    y_scroll = tk.Scrollbar(list_container, orient="vertical", command=app.listbox.yview)
    y_scroll.grid(row=0, column=1, sticky="ns")

    x_scroll = tk.Scrollbar(list_container, orient="horizontal", command=app.listbox.xview)
    x_scroll.grid(row=1, column=0, sticky="ew")

    # Connect listbox to scrollbars
    app.listbox.config(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    # Bind selection event
    app.listbox.bind("<<ListboxSelect>>", app.on_task_selected)

    # Bottom button row
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.grid(row=2, column=0, pady=10)

    app.btn_delete = ctk.CTkButton(btn_frame, text="Delete Task", command=app.delete_task)
    app.btn_delete.grid(row=0, column=0, padx=5)

    app.btn_save = ctk.CTkButton(btn_frame, text="Save Tasks", command=app._save_tasks_to_disk)
    app.btn_save.grid(row=0, column=1, padx=5)

    app.btn_reload = ctk.CTkButton(btn_frame, text="Reload from File", command=app._reload_tasks_from_disk)
    app.btn_reload.grid(row=0, column=2, padx=5)

    return frame
