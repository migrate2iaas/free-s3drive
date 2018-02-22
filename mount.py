import string
import os
import sys
import subprocess
import psutil

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
    p = subprocess.Popen(args, startupinfo=suinfo)
    return p
#TODO: add function to get stdout\stderr from subprocess for more info in case of errors

def mount(key, secret, bucket, mountpoint):
    #setting env for new proc
    os.environ["AWS_ACCESS_KEY_ID"] = str(key)
    os.environ["AWS_SECRET_ACCESS_KEY"] = str(secret)
    bucket_url = "s3://"+bucket
    fs_parms = [bucket_url , mountpoint, '--log' , 'fs.log' , '--debug' ,
                ,'--cache-path', os.getenv('TEMP',os.getcwd())+"/yas3fs-cache"
                ,'--uid', '545'] #uid 545 means 'all users'
                               #TODO: set uid that maps to the current user sid
                               #for rules see https://github.com/billziss-gh/winfsp/blob/9bd9cf4fbd42c1c0d0c50666df403df3d3381c43/src/dll/posix.c#L120 
    if getattr( sys, 'frozen', False ) :
        # running in a bundle , we exec the same module
        p = _run_proc([sys.executable , "YAFS"] + fs_parms)
    else:
        # running live
        python_path = sys.executable
        p = _run_proc([python_path , "-m" , "yas3fs.__init__"] + fs_parms)
    return {"process" : p , "mountpoint" : mountpoint}

def mount_alive(mount_obj):
    if mount_obj["process"].poll() != None:
        return False
    if os.path.exists(mount_obj["mountpoint"]) == False:
        return False
    #TODO: On Linux also check return os.path.ismount(mount_obj["mountpoint"])
    return True

def unmount(mount_obj):
    parent = psutil.Process(mount_obj["process"].pid)
    for child in parent.children(recursive=True):  
        child.kill()
    parent.kill()
