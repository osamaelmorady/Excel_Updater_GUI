# task_scheduler/ui/excel_panel.py
import customtkinter as ctk
from tksheet import Sheet
from tkinter import messagebox

def index_to_col_name(index: int) -> str:
    """Convert 0-based index to spreadsheet-like column name (A, B, ..., Z, AA, AB, ...)."""
    name = ""
    idx = index
    while True:
        idx, rem = divmod(idx, 26)
        name = chr(ord("A") + rem) + name
        if idx == 0:
            break
        idx -= 1
    return name





class ExcelPanel(ctk.CTkFrame):
    """
    Right panel that shows CSV/Excel content in a tksheet Sheet widget:
    - full grid (like Excel / Google Sheets)
    - row numbers on the left
    - column letters A, B, C, ...
    - editable cells
    """

    def __init__(self, master: "ExcelViewerApp", **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)

        # Row 0 = title, row 1 = sheet (expands), row 2 = bottom tabs
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Workbook",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, pady=(10, 5))

        # Container for the Sheet widget
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 5))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # TODO: put your tksheet widget inside `container` later
        # self.sheet = Sheet(container, ...)
        # self.sheet.grid(row=0, column=0, sticky="nsew")

        


        # --- Bottom "tabs" (dummy for now) ---
        self.bottom_tabs = ctk.CTkSegmentedButton(self,
            values=["Summary", "Filters", "Macros"],
            command=self.on_bottom_tab_selected
        )
        
        self.bottom_tabs.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        # Select default tab
        self.bottom_tabs.set("Summary")

    def on_bottom_tab_selected(self, tab_name: str):
        """
        Dummy callback for bottom tabs.
        Replace the body of this function later with real logic.
        """
        print(f"[ExcelPanel] Bottom tab selected: {tab_name}")
        messagebox.showinfo(
            "Not implemented yet",
            f"Tab '{tab_name}' is not implemented yet.\n\n"
            f"This is just a dummy action."
        )
