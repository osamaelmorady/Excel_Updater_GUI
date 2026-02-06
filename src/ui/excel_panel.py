# task_scheduler/ui/excel_panel.py
import os
import pandas as pd  # requires: pip install pandas openpyxl
import customtkinter as ctk
from tksheet import Sheet
from tkinter import messagebox


from managers.excel_mgr import excel_mgr

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



class BottomTabsPanel(ctk.CTkFrame):
    def __init__(self, master, on_tab_change=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.on_tab_change = on_tab_change

        self.tabs = ctk.CTkSegmentedButton(
            self,
            values=["input1.csv", "input2.csv", "input3.csv","input4.csv","input5.csv","input6.csv"],
            command=self._on_tab_selected,
        )
        self.tabs.pack(fill="x", padx=10, pady=(0, 10))

        # default
        self.tabs.set("Summary")

    def _on_tab_selected(self, value: str):
        if self.on_tab_change is not None:
            self.on_tab_change(value)
        else:
            # dummy behavior
            messagebox.showinfo("Not implemented", f"Tab '{value}' is not implemented yet.")


class ExcelPanel(ctk.CTkFrame,excel_mgr):
    """
    Right panel that shows CSV/Excel content in a tksheet Sheet widget:
    - full grid (like Excel / Google Sheets)
    - row numbers on the left
    - column letters A, B, C, ...
    - editable cells
    """

    def __init__(self, master: "ExcelViewerApp", **kwargs):
        ctk.CTkFrame.__init__(self, master, corner_radius=10, **kwargs)
        excel_mgr.__init__(self)  # if you later add __init__ to excel_mgr

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
        # --- tksheet Sheet widget ---
        self.sheet = Sheet( container, show_x_scrollbar=True,  show_y_scrollbar=True,  show_top_left=False)
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
        
        
        excel_all_data = self.load_excel_first_sheet()
        self.df_to_sheet(excel_all_data)
        
        rows = [[""]]
        self.sheet.set_sheet_data(rows)
        



        # Bottom tabs (in their own panel)
        self.tabs_panel = BottomTabsPanel(self, on_tab_change=self.on_bottom_tab_selected)
        self.tabs_panel.grid(row=2, column=0, sticky="ew")
        

    def on_bottom_tab_selected(self, tab_name: str):
        # Dummy for now
        print(f"[ExcelPanel] Tab selected: {tab_name}")
        # later: switch modes / show side widgets / change filters, etc.


    def df_to_sheet(self, df: "pd.DataFrame"):
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
        # if hasattr(self, "_update_title_with_path"):
        #     self._update_title_with_path()
        return
    
    
    def load_excel_first_sheet(self, path: str) -> pd.DataFrame:
        """
        Load the first sheet of an Excel file.
        """
        xls = pd.ExcelFile(path)
        sheet_name = xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
        df.attrs["sheet_name"] = sheet_name
        return df