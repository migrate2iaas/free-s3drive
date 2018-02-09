import traceback

def show_exception(message, exception):
    try:
        details = traceback.format_exc()
        import gui
        gui.show_error(message , "Details:\n"+details)
    except:
        pass
        
    
