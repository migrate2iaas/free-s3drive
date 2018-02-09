#TODO: run msi exec
#TODO: install to folder
#TODO: install to start menu
#TODO: install to desktop

import os
import sys


def _install_msi(msifile):
    #win-only
    import subprocess
    DETACHED_PROCESS = 0x00000008 # hides console window
    proc = subprocess.Popen(["msiexec" , "/quiet" , "/l*v" , os.getcwd()+"\\msi_install.log" , "/i" , os.path.abspath(msifile) ] ,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  creationflags = DETACHED_PROCESS)
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
    if msi_deps:
        for f in os.listdir(sys._MEIPASS+'/msi'):
            if os.path.isfile(f):
                _install_msi(f)

    location = get_location();
    shutil.copy(sys.executable , location)
    if shortcuts:
        _install_shortcuts(location)
    

def check_installed():
    """checks if the software and deps already installed"""
    return os.path.exists(get_location())
    

if __name__ == '__main__':
    install()
