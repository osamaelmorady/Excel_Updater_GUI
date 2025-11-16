# task_scheduler/ui/hotkeys_mgr.py

def register_hotkeys(app: "CsvViewerApp"):
    """
    Register global hotkeys_mgr for the application.

    - Ctrl+N : New Project
    - Ctrl+O : Open CSV
    - Ctrl+S : Save CSV
    - Esc    : Exit application
    - F1     : Help / About
    - F5     : Refresh CSV
    """

    # --- Handlers ---
    def _on_ctrl_n(event=None):
        # add/create new  CSV
        if hasattr(app, "new_project"):
            app.new_project()
        return "break"

    def _on_ctrl_o(event=None):
        if hasattr(app, "open_project"):
            app.open_project()
        return "break"
    

    def _on_ctrl_s(event=None):
        # Save current CSV
        if hasattr(app, "save_project"):
            app.save_project()
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
    
    def _on_f5(event=None):
        # reload csv file
        if hasattr(app, "reload_csv"):
            app.reload_csv()
        return "break" 
    
    
    def _on_f11(event=None):
        # maximize window to full screen
        if hasattr(app, "_maximize_window"):
            app._maximize_window()
        return "break" 
    
    
    def _on_f12(event=None):
        # minimize window to ("1024x700")
        if hasattr(app, "_minimize_window"):
            app._minimize_window()
        return "break"         
    

    # --- Bindings ---
    #
    # --- Bindings (global) ---
    app.bind_all("<Control-n>", _on_ctrl_n)
    app.bind_all("<Control-N>", _on_ctrl_n)
    app.bind_all("<Control-o>", _on_ctrl_o)
    app.bind_all("<Control-O>", _on_ctrl_o)
    app.bind_all("<Control-s>", _on_ctrl_s)
    app.bind_all("<Control-S>", _on_ctrl_s)

    app.bind_all("<Escape>", _on_escape)
    
    app.bind_all("<F1>", _on_f1)
    app.bind_all("<F5>", _on_f5)
    app.bind_all("<F11>", _on_f11)
    app.bind_all("<F12>", _on_f12)