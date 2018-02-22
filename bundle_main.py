"""this main is called when we exec from bundle"""

import mount
import gui
import error

import os
import sys

def main():
    if "YAFS" in sys.argv:
        sys.argv.remove("YAFS")
        try:
            import yas3fs
            return yas3fs.main()
        except Exception as e:
            error.show_exception("S3 Filesystem failure!" , e)
            return

    try:
        import bundle_install
        install_location = os.path.dirname(bundle_install.get_location())
        if install_location != os.getcwd():
            if not bundle_install.check_installed():
                with gui.splash("install"):
                    bundle_install.install()
                gui.show_message("S3 Drive", "Installation complete to {0} folder. S3Drive link is available on your desktop.".format(install_location));
            else:
                if gui.show_prompt("S3 Drive" , "Existing installation is found. Do you want to update it?"):
                    with gui.splash("install"):
                        bundle_install.install()
                    gui.show_message("S3 Drive", "Update complete in {0} folder. S3Drive link is available on your desktop.".format(install_location));
            sys.exit(0)
    except Exception as e:
        error.show_exception("Failed to install!" , e)
        return
    
    os.chdir(install_location) 
    gui.start_gui()
        
    
    
    
if __name__ == '__main__':
    main()
