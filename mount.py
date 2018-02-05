import string
import os

def get_free_drives():
    #TODO: implement non-Windows version
    from ctypes import windll
    free_drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if not bitmask & 1:
            free_drives.append(letter+":")
        bitmask >>= 1
    return free_drives

def _run_proc(args):
    suinfo = subprocess.STARTUPINFO() #TODO: suinfo is windows only
    suinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
    suinfo.wShowWindow = subprocess.SW_HIDE #hides console window
    p = subprocess.Popen(args, stdout=subprocess.PIPE , stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=suinfo)
    return p
#TODO: add function to get stdout\stderr from subprocess for more info in case of errors

def mount(key, secret, bucket, mountpoint):
    #setting env for new proc
    os.environ["AWS_ACCESS_KEY_ID"] = str(key)
    os.environ["AWS_SECRET_ACCESS_KEY"] = str(secret)
    python_path = sys.executable
    #TODO: check mount OK somehow
    p = _run_proc([python_path , "-m" , "yas3fs.__init__" , bucket , mountpoint, '--log' , 'fs.log'])
    return {"process" : p , "mountpoint" : mountpoint}

def mount_alive(mount_obj):
    if mount_obj["process"].poll():
        return False
    if os.path.exists(mount_obj["mountpoint"]) == False:
        return False
    #TODO: On Linux also check return os.path.ismount(mount_obj["mountpoint"])
    return True

def unmount(mount_obj)
    mount_obj["process"].terminate()
