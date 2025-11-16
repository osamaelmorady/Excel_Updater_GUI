# excel_mgr.py (clean independent Excel-only manager)

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
