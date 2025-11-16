# task_scheduler/ui/csv_api.py
import csv
import os
from tkinter import messagebox, filedialog
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


class csv_mgr:
    """
    Mixin providing CSV-related APIs:

    - create_new_csv
    - open_csv
    - reload_csv
    - save_csv
    - _load_csv_file
    - CSV edit commands: add_row, add_column, delete_row, delete_column

    Expects on self:
    - self.Excel_path
    - self.csv_panel (with .load_data() and .get_data())
    - self._update_title_with_path()
    """
    # def __init__(self, master: "CsvViewerApp", **kwargs):
    #     super().__init__(master, corner_radius=10, **kwargs)

    #     # Row 0 = title, row 1 = sheet (expands)
    #     self.grid_rowconfigure(0, weight=0)
    #     self.grid_rowconfigure(1, weight=1)
    #     self.grid_columnconfigure(0, weight=1)

    #     title = ctk.CTkLabel(self, text="CSV Viewer", font=ctk.CTkFont(size=18, weight="bold"))
    #     title.grid(row=0, column=0, pady=(10, 5))

    #     # Container for the Sheet widget
    #     container = ctk.CTkFrame(self, fg_color="transparent")
    #     container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    #     container.grid_rowconfigure(0, weight=1)
    #     container.grid_columnconfigure(0, weight=1)

    #     # --- tksheet Sheet widget ---
    #     self.sheet = Sheet(
    #         container,
    #         show_x_scrollbar=True,
    #         show_y_scrollbar=True,
    #         show_top_left=False,   # no extra top-left box
    #     )
    #     self.sheet.grid(row=0, column=0, sticky="nsew")
        
    #     # Enable useful bindings (edit, copy/paste, resize, etc.)
    #     # Enable useful bindings (edit, copy/paste, resize, etc.)
    #     self.sheet.enable_bindings(
    #         "single_select",
    #         "row_select",
    #         "column_select",
    #         "arrowkeys",
    #         "row_height_resize",
    #         "column_width_resize",
    #         "drag_select",
    #         "edit_cell",
    #         "copy",
    #         "cut",
    #         "paste",
    #         "delete",
    #         "undo",
    #         "redo",
    #     )

        
        # Initial empty data
        # self.clear_table()
        
    # ----------------- CSV core operations -----------------

    def create_new_csv(self):
        """
        Create a brand new (empty) CSV file and open it in the viewer.
        If a CSV is already open, it is simply replaced in the UI.
        """
        initialfile = "new.csv"
        initialdir = os.path.dirname(self.Excel_path) if self.Excel_path else ""

        path = filedialog.asksaveasfilename(
            title="Create New CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=initialfile,
            initialdir=initialdir or None,
        )

        if not path:
            return

        try:
            # Create a CSV with one empty cell so the sheet shows 1x1 grid
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([""])

            self.Excel_path = path

            # Load a single empty cell into the sheet
            self.load_data([[""]])

            # self._update_title_with_path()
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

        self.Excel_path = path
        self.load_data(rows)
        # self._update_title_with_path()

    def reload_csv(self):
        if not self.Excel_path:
            messagebox.showinfo("Reload CSV", "No CSV file is currently open.")
            return

        try:
            rows = self._load_csv_file(self.Excel_path)
        except Exception as e:
            messagebox.showerror("Reload CSV", f"Failed to reload CSV:\n{e}")
            return

        self.load_data(rows)
        # self._update_title_with_path()

    def save_csv(self):
        """
        Save the current sheet data to a CSV file.
        """
        rows = self.get_data()
        if not rows:
            messagebox.showinfo("Save CSV", "There is no data to save.")
            return

        initialfile = os.path.basename(self.Excel_path) if self.Excel_path else "data.csv"
        initialdir = os.path.dirname(self.Excel_path) if self.Excel_path else ""

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

            self.Excel_path = path
            # self._update_title_with_path()
            messagebox.showinfo("Save CSV", f"CSV saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save CSV", f"Failed to save CSV:\n{e}")

    def _load_csv_file(self, path: str):
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows


    # def clear_table(self):
    #     """Clear all data from the sheet."""
    #     # set_sheet_data([]) leaves headers but no rows
    #     self.sheet.set_sheet_data([[]])
    #     self.sheet.headers([])          # no column labels
    #     self.sheet.row_index([])        # no row labels
    #     self.sheet.refresh()


    # def load_data(self, rows):
    #     """
    #     rows: list[list[str]] – entire CSV content (including any header row),
    #     displayed as a spreadsheet with:
    #       - column headers: A, B, C, ...
    #       - row headers: 1, 2, 3, ...
    #     """
    #     if not rows:
    #         self.clear_table()
    #         return

    #     # Ensure all rows have same length
    #     num_cols = max(len(r) for r in rows)
    #     normalized_rows = [
    #         list(r) + [""] * (num_cols - len(r))
    #         for r in rows
    #     ]

    #     # Set data
    #     self.sheet.set_sheet_data(normalized_rows)

    #     # Column headers A, B, C, ...
    #     col_headers = [index_to_col_name(i) for i in range(num_cols)]
    #     self.sheet.headers(col_headers)

    #     # Row headers 1, 2, 3, ...
    #     row_headers = [str(i + 1) for i in range(len(normalized_rows))]
    #     self.sheet.row_index(row_headers)

    #     # If your version supports themes, you *could* do:
    #     #   self.sheet.theme("light blue")
    #     # but since it raised AttributeError, we skip it.

    #     self.sheet.refresh()

    # ----------------- CSV edit commands (stubs) -----------------




    def add_row(self):
        messagebox.showinfo(
            "Add Row",
            "Add Row is not implemented yet.\n(You can implement it later.)",
        )

    def add_column(self):
        messagebox.showinfo(
            "Add Column",
            "Add Column is not implemented yet.\n(You can implement it later.)",
        )

    def delete_row(self):
        messagebox.showinfo(
            "Delete Row",
            "Delete Row is not implemented yet.\n(You can implement it later.)",
        )

    def delete_column(self):
        messagebox.showinfo(
            "Delete Column",
            "Delete Column is not implemented yet.\n(You can implement it later.)",
        )
