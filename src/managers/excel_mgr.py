# excel_mgr.py (clean independent Excel-only manager)
# excel_mgr.py
import os
import pandas as pd  # requires: pip install pandas openpyxl

from tkinter import messagebox, filedialog
from pathlib import Path
from typing import Optional




from services.excel_service import (
    save_excel_workbook,
    load_excel_workbook,
    ExcelError,
    ExcelWorkbook,
)


class excel_mgr:
    """
    Independent Excel manager.
    Provides:
    - import_from_excel()
    - export_to_excel()

    Stores:
    - self.data_path                (path to currently opened Excel)
    - self.current_excel_workbook  (ExcelWorkbook object)

    This file has NO dependency on settings_mgr or project_mgr.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Must exist for project_mgr compatibility
        self.data_path: Optional[str] = None
        self.current_excel_workbook: Optional[ExcelWorkbook] = None

    # ---------------------------------------------------------
    # Import Excel file
    # ---------------------------------------------------------
    def import_from_excel(self):
        """
        Let user pick an Excel file, then Load & Store:
        - self.data_path
        - self.current_excel_workbook

        Then GUI can use these attributes to update UI.
        """
        path = filedialog.askopenfilename(
            title="Open Excel file",
            filetypes=[
                ("Excel files", "*.xlsx *.xlsm *.xls"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            workbook: ExcelWorkbook = load_excel_workbook(path)
        except ExcelError as exc:
            messagebox.showerror("Excel Import Error", str(exc))
            return

        # Save internally
        self.data_path = path
        self.current_excel_workbook = workbook

        # Extract sheet information for UI
        self.sheet_names = workbook.sheet_names()
        self.sheet_count = workbook.sheet_count()

        messagebox.showinfo(
            "Excel Loaded",
            f"Loaded Excel file:\n{path}\n\nSheets found: {self.sheet_count}",
        )

        # If the GUI has a function to populate tabs, call it:
        if hasattr(self, "_on_excel_loaded"):
            self._on_excel_loaded(workbook)

        return workbook

    # ---------------------------------------------------------
    # Export Excel file
    # ---------------------------------------------------------
    def export_to_excel(self):
        """
        Export the entire ExcelWorkbook to user-selected location.
        """
        wb = getattr(self, "current_excel_workbook", None)
        if wb is None:
            messagebox.showinfo(
                "Export to Excel",
                "No Excel workbook is loaded to export.",
            )
            return

        # Suggest original location
        initialdir = str(wb.path.parent) if wb.path else None
        initialfile = wb.path.name if wb.path else "export.xlsx"

        path = filedialog.asksaveasfilename(
            title="Export Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialdir=initialdir,
            initialfile=initialfile,
        )
        if not path:
            return

        try:
            save_excel_workbook(wb, path)
        except ExcelError as exc:
            messagebox.showerror(
                "Export to Excel",
                f"Failed to export workbook:\n{exc}",
            )
            return

        messagebox.showinfo(
            "Export Successful",
            f"Workbook exported to:\n{path}",
        )




    # ---------------------------------------------------------
    # Process Excel file
    # ---------------------------------------------------------
    # ----------------- Core Excel operations -----------------

    def open_excel(self):
        """
        Open an Excel file (.xlsx) and display the first sheet in the grid.
        """
        path = filedialog.askopenfilename(
            title="Open Excel file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            df = self._load_excel_first_sheet(path)
        except ImportError:
            messagebox.showerror(
                "Excel Import",
                "Missing dependency: pandas/openpyxl.\n\n"
                "Install with:\n  pip install pandas openpyxl",
            )
            return
        except Exception as e:
            messagebox.showerror("Open Excel", f"Failed to open Excel file:\n{e}")
            return

        self.excel_path = path
        self.current_sheet_name = df.attrs.get("sheet_name", None)
        self._df_to_sheet(df)
        self._update_title_if_available()


    def reload_excel(self):
        """
        Reload the current Excel file (same sheet).
        """
        if not getattr(self, "excel_path", None):
            messagebox.showinfo("Reload Excel", "No Excel file is currently open.")
            return

        sheet_name = getattr(self, "current_sheet_name", None)

        try:
            df = self._load_excel_sheet(self.excel_path, sheet_name)
        except Exception as e:
            messagebox.showerror("Reload Excel", f"Failed to reload Excel:\n{e}")
            return

        self._df_to_sheet(df)
        self._update_title_if_available()

    def load_excel_sheet(self, sheet_name: str):
        """
        Load a specific sheet from the currently opened Excel file.
        """
        if not getattr(self, "excel_path", None):
            messagebox.showinfo("Excel", "No Excel file is currently open.")
            return

        try:
            df = self._load_excel_sheet(self.excel_path, sheet_name)
        except Exception as e:
            messagebox.showerror("Excel", f"Failed to load sheet '{sheet_name}':\n{e}")
            return

        self.current_sheet_name = sheet_name
        self._df_to_sheet(df)
        self._update_title_if_available()


    def save_excel_as(self):
        """
        Save current grid data to a new Excel file (.xlsx).
        """
        # get data from tksheet
        try:
            data = self.sheet.get_sheet_data(return_copy=True)
        except TypeError:
            data = self.sheet.get_sheet_data()

        if not data:
            messagebox.showinfo("Save Excel", "There is no data to save.")
            return

        # choose path
        initialfile = (
            os.path.basename(getattr(self, "excel_path", "") or "data.xlsx")
        )
        initialdir = (
            os.path.dirname(getattr(self, "excel_path", "")) if getattr(self, "excel_path", None) else ""
        )

        path = filedialog.asksaveasfilename(
            title="Save as Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=initialfile,
            initialdir=initialdir or None,
        )
        if not path:
            return

        try:
            df = pd.DataFrame(data)
            df.to_excel(path, index=False)
            self.excel_path = path
            self._update_title_if_available()
            messagebox.showinfo("Save Excel", f"Excel file saved to:\n{path}")
        except ImportError:
            messagebox.showerror(
                "Excel Export",
                "Missing dependency: pandas/openpyxl.\n\n"
                "Install with:\n  pip install pandas openpyxl",
            )
        except Exception as e:
            messagebox.showerror("Save Excel", f"Failed to save Excel:\n{e}")

    # ----------------- Internal helpers -----------------

    def _load_excel_first_sheet(self, path: str) -> pd.DataFrame:
        """
        Load the first sheet of an Excel file.
        """
        xls = pd.ExcelFile(path)
        sheet_name = xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
        df.attrs["sheet_name"] = sheet_name
        return df

    def _load_excel_sheet(self, path: str, sheet_name: str | None) -> pd.DataFrame:
        """
        Load a specific sheet from an Excel file.
        If sheet_name is None, loads the first sheet.
        """
        xls = pd.ExcelFile(path)
        if sheet_name is None:
            sheet_name = xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
        df.attrs["sheet_name"] = sheet_name
        return df

    def _df_to_sheet(self, df: "pd.DataFrame"):
        """
        Push a DataFrame into the tksheet widget.
        """
        # Normalize to list of lists (rows)
        rows = df.fillna("").astype(str).values.tolist()

        # Ensure at least one cell
        if not rows:
            rows = [[""]]

        # Set data in the Sheet widget
        self.sheet.set_sheet_data(rows)

        # Optional: you can add headers from df.columns if you like
        # For now, leave A/B/C... from tksheet as-is, or:
        # self.sheet.headers(list(df.columns.astype(str)))

        # Row headers 1..N
        row_headers = [str(i + 1) for i in range(len(rows))]
        self.sheet.row_index(row_headers)

        self.sheet.refresh()

    def _update_title_if_available(self):
        """
        Call the app's _update_title_with_path() if it exists.
        """
        if hasattr(self, "_update_title_with_path"):
            self._update_title_with_path()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    