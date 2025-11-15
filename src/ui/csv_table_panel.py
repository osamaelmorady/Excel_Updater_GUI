# task_scheduler/ui/csv_table_panel.py
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class CsvTablePanel(ctk.CTkFrame):
    """
    Right panel that shows CSV content in a table (Treeview)
    with horizontal & vertical scrollbars.
    """

    def __init__(self, master: "CsvViewerApp", **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)

        # Row 0 = title (fixed), row 1 = table (expands)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="CSV Viewer", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Container for tree + scrollbars
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Treeview (table)
        self.tree = ttk.Treeview(container, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.v_scroll = tk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        self.h_scroll = tk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

    # ---------------------------
    # Public API
    # ---------------------------
    def clear_table(self):
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        self.tree["columns"] = ()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_data(self, headers, rows):
        self.clear_table()

        self.tree["columns"] = headers
        for col in headers:
            self.tree.heading(col, text=col)
            # 👇 prevent columns from auto-stretching to the widget width
            self.tree.column(col, width=120, anchor="w", stretch=False)

        for row in rows:
            values = list(row) + [""] * (len(headers) - len(row))
            self.tree.insert("", "end", values=values)

