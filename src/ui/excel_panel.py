# task_scheduler/ui/excel_panel.py
import customtkinter as ctk
from tksheet import Sheet


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
    Right panel that shows CSV content in a tksheet Sheet widget:
    - full grid (like Excel / Google Sheets)
    - row numbers on the left
    - column letters A, B, C, ...
    - editable cells
    """

    def __init__(self, master: "ExcelViewerApp", **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)

        # Row 0 = title, row 1 = sheet (expands)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="CSV Viewer", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, pady=(10, 5))

        # Container for the Sheet widget
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --- tksheet Sheet widget ---
        self.sheet = Sheet(
            container,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            show_top_left=False,   # no extra top-left box
        )
        self.sheet.grid(row=0, column=0, sticky="nsew")
        
        # Enable useful bindings (edit, copy/paste, resize, etc.)
        # Enable useful bindings (edit, copy/paste, resize, etc.)
        self.sheet.enable_bindings(
            "single_select",
            "row_select",
            "column_select",
            "arrowkeys",
            "row_height_resize",
            "column_width_resize",
            "drag_select",
            "edit_cell",
            "copy",
            "cut",
            "paste",
            "delete",
            "undo",
            "redo",
        )


        # Initial empty data
        self.clear_table()

    # ---------------------------
    # Public API (used by app)
    # ---------------------------
    def clear_table(self):
        """Clear all data from the sheet."""
        # set_sheet_data([]) leaves headers but no rows
        self.sheet.set_sheet_data([[]])
        self.sheet.headers([])          # no column labels
        self.sheet.row_index([])        # no row labels
        self.sheet.refresh()

    def load_data(self, rows):
        """
        rows: list[list[str]] – entire CSV content (including any header row),
        displayed as a spreadsheet with:
          - column headers: A, B, C, ...
          - row headers: 1, 2, 3, ...
        """
        if not rows:
            self.clear_table()
            return

        # Ensure all rows have same length
        num_cols = max(len(r) for r in rows)
        normalized_rows = [
            list(r) + [""] * (num_cols - len(r))
            for r in rows
        ]

        # Set data
        self.sheet.set_sheet_data(normalized_rows)

        # Column headers A, B, C, ...
        col_headers = [index_to_col_name(i) for i in range(num_cols)]
        self.sheet.headers(col_headers)

        # Row headers 1, 2, 3, ...
        row_headers = [str(i + 1) for i in range(len(normalized_rows))]
        self.sheet.row_index(row_headers)

        # If your version supports themes, you *could* do:
        #   self.sheet.theme("light blue")
        # but since it raised AttributeError, we skip it.

        self.sheet.refresh()


    # def get_data(self):
    #     """
    #     Return current sheet data as list of rows (list[list[str]]).
    #     """
    #     try:
    #         # newer tksheet versions
    #         return self.sheet.get_sheet_data(return_copy=True)
    #     except TypeError:
    #         # older versions without the argument
    #         return self.sheet.get_sheet_data()
