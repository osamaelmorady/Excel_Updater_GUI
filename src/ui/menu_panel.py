# task_scheduler/ui/menu_panel.py
import tkinter as tk

# from managers.project_mgr import *
# from managers.excel_mgr import *
# from managers.csv_mgr import *


def build_menu_bar(app: "ExcelViewerApp"):
    """
    Create the top menu bar: File, Appearance, Help.
    `app` is the root CTk window (ExcelViewerApp).
    """
    menubar = tk.Menu(app)

    # ---------- File menu ----------
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New Project...", command=app.new_project, accelerator="Ctrl+N")
    file_menu.add_command(label="Open Project...", command=app.open_project, accelerator="Ctrl+O")
    file_menu.add_command(label="Save Project As...", command=app.save_project, accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit, accelerator="Esc")
    menubar.add_cascade(label="File", menu=file_menu)

    # # ---------- Edit menu ----------
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Undo", command=app.dummy)
    edit_menu.add_command(label="Redo", command=app.dummy)
    edit_menu.add_separator()
    edit_menu.add_command(label="Refresh", command=app.dummy)
    edit_menu.add_command(label="Clear", command=app.dummy)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    
    # # ---------- Excel menu ----------
    excel_menu = tk.Menu(menubar, tearoff=0)
    excel_menu.add_command(label="Export to Excel...", command=app.export_to_excel)
    excel_menu.add_command(label="Import from Excel...", command=app.import_from_excel)
    excel_menu.add_separator()
    excel_menu.add_command(label="Add New Sheet...", command=app.dummy)
    excel_menu.add_command(label="Delete Current Sheet...", command=app.dummy)
    excel_menu.add_command(label="Reload Current Sheet...", command=app.dummy) 
    excel_menu.add_command(label="Clear Current Sheet...", command=app.dummy) 
    excel_menu.add_command(label="Save Current Sheet...", command=app.dummy)  
    menubar.add_cascade(label="Excel", menu=excel_menu)

    # # ---------- CSV menu ----------
    CSV_menu = tk.Menu(menubar, tearoff=0)
    CSV_menu.add_command(label="New..", command=app.create_new_csv)
    CSV_menu.add_command(label="Open..", command=app.open_csv)
    CSV_menu.add_command(label="Reload..", command=app.reload_csv)
    CSV_menu.add_command(label="Save As", command=app.save_csv)
    menubar.add_cascade(label="CSV", menu=CSV_menu)


    # # ---------- View menu ----------
    view_menu = tk.Menu(menubar, tearoff=0)
    
    window_menu = tk.Menu(view_menu, tearoff=0)
    window_menu.add_command(label="Full Screen", accelerator="F11", command=app.dummy)
    window_menu.add_command(label="Window", accelerator="F12", command=app.dummy)
    view_menu.add_cascade(label="Window", menu=window_menu) 

    
    appearance_menu = tk.Menu(view_menu, tearoff=0)
    appearance_menu.add_radiobutton(label="System",command=lambda: app._set_appearance_mode("System") )
    appearance_menu.add_radiobutton( label="Light", command=lambda: app._set_appearance_mode("Light") )
    appearance_menu.add_radiobutton( label="Dark", command=lambda: app._set_appearance_mode("Dark")  )
    view_menu.add_cascade(label="Appearance", menu=appearance_menu)
    menubar.add_cascade(label="View", menu=view_menu)
    
    # ---------- Help menu ----------
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About",  accelerator="F1", command=app._show_about_dialog)
    menubar.add_cascade(label="Help", menu=help_menu)

    # Attach to window
    app.config(menu=menubar)

    return menubar



