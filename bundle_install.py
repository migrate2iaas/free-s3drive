#TODO: run msi exec
#TODO: install to folder
#TODO: install to start menu
#TODO: install to desktop

import os
import sys


def _install_msi(msifile , log_dir = os.getcwd()):
    #win-only
    import subprocess
    DETACHED_PROCESS = 0x00000008 # hides console window
    proc = subprocess.Popen(["msiexec" , "/quiet" , "/l*v" ,
                             log_dir+"\\msi_install_{0}.log".format(os.path.basename(msifile))
                             , "/i" ,  os.path.abspath(msifile) ] , creationflags = DETACHED_PROCESS)
    output = str(proc.communicate()[0])
    if proc.returncode:
        raise subprocess.CalledProcessError(p.returncode , args, output)       

# see http://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create-shortcuts/
def _install_shortcuts(location):
    import os, winshell
    from win32com.client import Dispatch
 
    desktop = winshell.desktop()
    path = os.path.join(desktop, "S3Drive.lnk")
    target = location
    wDir = os.path.dirname(location)
    icon = location
 
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()    

def get_location():
    location = os.getenv("ProgramFiles" , "C:")
    location += "\\S3Drive"
    if os.path.exists(location) == False:
        os.mkdir(location)
    location += "\\S3Drive.exe"
    #location = os.path.dirname(sys.executable) + "\\S3Drive.exe"
    return location

def install(msi_deps = True, shortcuts = True):
    """installs the software and deps"""
    import shutil
    #TODO: handle errors
    location = get_location();
    
    if msi_deps:
        msi_folder = "./msi"
        if getattr( sys, 'frozen', False ):
            msi_folder = sys._MEIPASS+'/msi'
        for f in os.listdir(msi_folder):
            path = os.path.join(msi_folder, f)
            if os.path.isfile(path):
                _install_msi(path , os.path.dirname(location))

    shutil.copy(sys.executable , location)
    if shortcuts:
        _install_shortcuts(location)
    

def check_installed():
    """checks if the software and deps already installed"""
    return os.path.exists(get_location())
    

if __name__ == '__main__':
    install()
