import os
import time
import sys
import subprocess

import s3func
import mount
import error

from Tkinter import *
try:
    import tkinter.ttk as ttk
    import tkinter.font as tkFont
    from tkinter import messagebox
except ImportError: # Python 2
    import ttk
    import tkFont
    import tkMessageBox as messagebox

if getattr( sys, 'frozen', False ):
    resources_dir = sys._MEIPASS+'/res'
else:
    resources_dir = os.getcwd()+'/res' # save the resources dir as subsequent chdir is possible 
    
buckets_loaded = False
mounted = False
mount_obj = None
root = None

def show_message(caption , text):
    if not root:
        Tk().withdraw()
    messagebox.showinfo(caption, text)

def show_error(caption , text):
    if not root:
        Tk().withdraw()
    messagebox.showerror(caption, text)

def show_prompt(caption , text):
    if not root:
        Tk().withdraw()
    return messagebox.askokcancel(caption, text)

def splash(imagename):
    """
       use with `with` statement
       do not use after start_gui() called
    """
    import splash as spl
    temp_root = root
    if not temp_root:
        temp_root = Tk()
    temp_root.deiconify()
    return spl.SplashScreen( temp_root, resources_dir + '\\{0}.gif'.format(imagename), 2.0 )

def start_gui():
    # CONSTANTS
    AWS_KEY_LEN = 20
    AWS_SECRET_LEN = 40

    global root
    root = Tk()
    

    #set the default style for every gui element
    font = tkFont.Font(family='Arial', size=11)
    #root.iconbitmap(os.path.dirname(os.path.realpath(__file__))+'/s3drive.ico')
    default_style_kwarg = {'font': font}
    label_style_kwarg = default_style_kwarg.copy()
    label_style_kwarg.update({'anchor': W})
    padx = 5
    pady = 8
    default_grid_kwarg = {'padx' : padx , 'pady': pady , 'sticky' : "ew"}

    root.title("S3 Drive")

    def update_choice_list(menu, newvalues, var):
        o = menu
        m = o.children['menu']
        m.delete(0,END)
        for val in newvalues:
            m.add_command(label=val,command=lambda v=var,l=val:v.set(l))
        var.set(newvalues[0])

    def key_input_callback(sv):
        global buckets_loaded
        if len(key_var.get()) == AWS_KEY_LEN and len(secret_var.get()) == AWS_SECRET_LEN:
            update_choice_list(bucket_options, ['Connecting to AWS...'] , bucket_var)
            root.config(cursor="wait")
            root.update()
            try:
                buckets = s3func.get_bucket_list(key_var.get() , secret_var.get())
                update_choice_list(bucket_options , buckets , bucket_var)
                buckets_loaded = True
            except Exception as e:
                messagebox.showerror("Failed to connect to AWS" , "Error connecting to AWS with supplied keys.\nError details:\n" + repr(e.__dict__))
                update_choice_list(bucket_options , ['Error: ' + str(e)] , bucket_var)
                buckets_loaded = False
            root.config(cursor="")

    def _delete_window():
        if mounted:
            if not messagebox.askokcancel("Quit", "Closing this window will result in S3Drive to unmount.\nAre you sure you want to exit?"):
                return
            else:
                mount_command()
        try:
            if mountobj:
                mount.unmount(mount_obj)
        except Exception as e:
            pass
        root.destroy()
        sys.exit(0)

    def mount_command():
        global mounted 
        global mount_obj 
        if buckets_loaded == False:
            messagebox.showinfo("AWS Keys needed" , "Please enter your AWS keys and select bucket to mount to proceed!")
            return
        if mounted == False:
            mount_button_text.set("Mounting...Wait up to 1 min.")
            root.config(cursor="wait")
            root.update()
            try:
                mount_obj = mount.mount(key_var.get() , secret_var.get() , bucket_var.get() , drive_var.get())
                check_interval = 3
                max_time_wait = 30
                time_waited = 0
                while 1:
                    if mount.mount_alive(mount_obj):
                        #TODO: disable all inputs
                        mount_button_text.set("Unmount")
                        mounted = True
                        show_message("Mount Success" , "Bucket {0} mounted to drive {1}".format(bucket_var.get() , drive_var.get()));
                        break
                    else:
                        time.sleep(check_interval)
                        time_waited += check_interval
                    if time_waited > max_time_wait:
                        messagebox.showwarning("Failed to mount!" , "Failed to mount!\nPlease check {0}\\fs.log for more info".format(os.getcwd()))
                        break
            except Exception as e:
                error.show_exception("Failed to mount!" , e)
            if not mounted:    
                mount_button_text.set("Mount")
            else:
                #TODO: windows-only
                subprocess.Popen(r'explorer /select,"'+drive_var.get()+'"')
            root.config(cursor="")
            root.update()
        else:
            root.config(cursor="wait")
            root.update()
            mount.unmount(mount_obj)
            time.sleep(8)
            if not mount.mount_alive(mount_obj):
                #TODO: enable all inputs
                mount_button_text.set("Mount")
                mounted = False
            else:
                #TODO: more descriptive errors
                messagebox.showwarning("Failed to unmount!" , "Please check fs.log for more info")
            root.config(cursor="")
            root.update()
        
    #TODO: make it configurable so to support more param entries
    row = 0
    # row 1
    row = row + 1
    key_label = Label(root,text="AWS Key:" , **label_style_kwarg)
    key_label.grid(row = row, column = 1, **default_grid_kwarg)
    key_var = StringVar(root)
    key_var.trace("w", lambda name, index, mode, sv=key_var: key_input_callback(sv))
    key_entry = Entry(root, width=AWS_SECRET_LEN, textvariable=key_var, **default_style_kwarg)
    key_entry.grid(row = row, column = 2, **default_grid_kwarg)
    # row 2
    row = row + 1
    secret_label = Label(root,text="AWS Secret:" , **label_style_kwarg)
    secret_label.grid(row = row , column = 1, **default_grid_kwarg)
    secret_var = StringVar(root)
    secret_var.trace("w", lambda name, index, mode, sv=secret_var: key_input_callback(sv))
    secret_entry = Entry(root, width=AWS_SECRET_LEN, textvariable=secret_var, **default_style_kwarg)
    secret_entry.grid(row = row , column = 2, **default_grid_kwarg)
    # row 3 
    row = row + 1
    bucket_label = Label(root,text="Bucket:" , **label_style_kwarg)
    bucket_label.grid(row = row , column = 1, **default_grid_kwarg)
    bucket_var = StringVar(root)
    choices = { 'Enter AWS Keys above to load the bucket list...'}
    bucket_var.set(list(choices)[0])
    #bucket_var.trace("w", lambda name, index, mode, sv=bucket_var: input_callback(sv))
    bucket_options = OptionMenu(root, bucket_var, *choices)
    bucket_options.grid(row = row , column = 2, **default_grid_kwarg)
    # row 4 
    row = row + 1
    drive_label = Label(root,text="Mount to:" , **label_style_kwarg)
    drive_label.grid(row = row , column = 1, **default_grid_kwarg)
    drive_var = StringVar(root)
    choices = mount.get_free_drives()
    drive_var.set(list(choices)[-1])
    #bucket_var.trace("w", lambda name, index, mode, sv=bucket_var: input_callback(sv))
    drive_options = OptionMenu(root, drive_var, *choices)
    drive_options.grid(row = row , column = 2, **default_grid_kwarg)

    # last row
    row = row + 1
    mount_button_text = StringVar()
    mount_button = Button(root, textvariable = mount_button_text, command=mount_command, **default_style_kwarg)
    mount_button_text.set("Mount")
    mount_button.grid(row = row , column = 1 , columnspan = 2, **default_grid_kwarg)

    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.deiconify()
    root.mainloop()

if __name__ == '__main__':
    start_gui()
