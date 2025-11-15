# task_scheduler/ui/menu_bar.py
import tkinter as tk


def build_menu_bar(app: "CsvViewerApp"):
    """
    Create the top menu bar: File, Appearance, Help.
    `app` is the root CTk window (CsvViewerApp).
    """
    menubar = tk.Menu(app)

    # ---------- File menu ----------
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New Project", command=app.new_project)
    file_menu.add_command(label="Open Project...", command=app.open_project)
    file_menu.add_command(label="Save Project...", command=app.save_project)
    file_menu.add_separator()
    file_menu.add_command(label="Export to Excel...", command=app.export_to_excel)
    file_menu.add_command(label="Import from Excel...", command=app.import_from_excel)
    file_menu.add_separator()
    file_menu.add_command(label="Open CSV...", command=app.open_csv)
    file_menu.add_command(label="Reload CSV", command=app.reload_csv)
    file_menu.add_command(label="Save CSV", command=app.save_csv,accelerator="Ctrl+S",)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit, accelerator="Esc")
    menubar.add_cascade(label="File", menu=file_menu)

    # # ---------- Edit menu ----------
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Clear Table", command=app.csv_panel.clear_table)
    menubar.add_cascade(label="Edit", menu=edit_menu)


    # ---------- Appearance menu ----------
    appearance_menu = tk.Menu(menubar, tearoff=0)
    appearance_menu.add_radiobutton(
        label="System",
        command=lambda: app._set_appearance_mode("System")
    )
    appearance_menu.add_radiobutton(
        label="Light",
        command=lambda: app._set_appearance_mode("Light")
    )
    appearance_menu.add_radiobutton(
        label="Dark",
        command=lambda: app._set_appearance_mode("Dark")
    )
    menubar.add_cascade(label="Appearance", menu=appearance_menu)

    # ---------- Help menu ----------
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=app._show_about_dialog)
    menubar.add_cascade(label="Help", accelerator="F1", menu=help_menu)

    # Attach to window
    app.config(menu=menubar)

    return menubar
