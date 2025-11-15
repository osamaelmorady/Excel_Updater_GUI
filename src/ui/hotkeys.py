# task_scheduler/ui/hotkeys.py

def register_hotkeys(app: "CsvViewerApp"):
    """
    Register global hotkeys for the application.
    - Ctrl+S : Save CSV
    - Esc    : Exit application
    - F1     : Help / About
    """

    # --- Handlers ---

    def _on_ctrl_s(event=None):
        # Save current CSV
        if hasattr(app, "save_csv"):
            app.save_csv()
        return "break"  # prevent default beep / focus change

    def _on_escape(event=None):
        # Exit application
        app.quit()
        return "break"

    def _on_f1(event=None):
        # Show help / about
        if hasattr(app, "_show_about_dialog"):
            app._show_about_dialog()
        return "break"

    # --- Bindings ---
    #
    # bind_all => works no matter which widget has focus
    app.bind_all("<Control-s>", _on_ctrl_s)
    app.bind_all("<Control-S>", _on_ctrl_s)  # in case Shift is pressed
    app.bind_all("<Escape>", _on_escape)
    app.bind_all("<F1>", _on_f1)
