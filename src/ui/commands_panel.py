# task_scheduler/ui/excel_panel.py
import customtkinter as ctk


def build_commands_panel(app: "ExcelViewerApp"):
    """
    Left side panel with CSV commands.
    """
    frame = ctk.CTkFrame(app, corner_radius=10)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # fill left column

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(5, weight=1)  # spacer row

    title = ctk.CTkLabel(frame, text="CSV Commands", font=ctk.CTkFont(size=16, weight="bold"))
    title.grid(row=0, column=0, pady=(10, 15), padx=10, sticky="w")

    btn_add_row = ctk.CTkButton(frame, text="Add Row", command=app.dummy)
    btn_add_row.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    btn_add_column = ctk.CTkButton(frame, text="Add Column", command=app.dummy)
    btn_add_column.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    btn_delete_row = ctk.CTkButton(frame, text="Delete Row", command=app.dummy)
    btn_delete_row.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    btn_delete_column = ctk.CTkButton(frame, text="Delete Column", command=app.dummy)
    btn_delete_column.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    return frame
