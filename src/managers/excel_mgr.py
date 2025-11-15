# task_scheduler/ui/excel_api.py
from tkinter import messagebox


class excel_mgr:
    """
    Mixin providing Excel-related APIs.

    Currently only stubs; you can later implement real Excel export/import
    (e.g. using pandas or openpyxl).
    """

    def export_to_excel(self):
        """
        Placeholder: you can later export current table to Excel.
        """
        messagebox.showinfo(
            "Export to Excel",
            "Export to Excel is not implemented yet.\n\n"
            "Later, we can export the current CSV table to .xlsx using pandas.",
        )

    def import_from_excel(self):
        """
        Placeholder: you can later import Excel and show it in the table.
        """
        messagebox.showinfo(
            "Import from Excel",
            "Import from Excel is not implemented yet.\n\n"
            "Later, we can load .xlsx and display it like a CSV.",
        )
