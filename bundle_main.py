"""this main is called when we exec from bundle"""

import mount
import gui
import error

def main():
    if "YAFS" in sys.argv:
        sys.argv.remove("YAFS")
        import yas3fs
        return yas3fs.main()

    try:
        import bundle_install
        if not bundle_install.check_installed():
            bundle_install.install()
    except Exception as e:
        error.show_exception("Failed to install!" , e)
        return
        
    gui.start_gui()
        
    
    
    
if __name__ == '__main__':
    main()
