import os

from Tkinter import *
try:
    import tkinter.ttk as ttk
    import tkinter.font as tkFont
    from tkinter import messagebox
except ImportError: # Python 2
    import ttk
    import tkFont
    import tkMessageBox as messagebox

import s3func
import mount
import time

# CONSTANTS
AWS_KEY_LEN = 20
AWS_SECRET_LEN = 40

# MAIN......
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

buckets_loaded = False
mounted = False
mount_obj = None

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
        root.config(cursor="wait")
        root.update()
        update_choice_list(['Connecting to AWS...'] , buckets , bucket_var)
        try:
            buckets = s3func.get_bucket_list(key_var.get() , secret_var.get())
            update_choice_list(bucket_options , buckets , bucket_var)
            buckets_loaded = True
        except Exception as e:
            messagebox.showerror("Failed to connect to AWS" , "Error connecting to AWS with supplied keys.\nError details:\n" + repr(e.__dict__))
            update_choice_list(['Error: ' + str(e)] , buckets , bucket_var)
            buckets_loaded = False
        root.config(cursor="")

def mount_command():
    if buckets_loaded == False:
        messagebox.showinfo("AWS Keys needed" , "Please enter your AWS keys and select bucket to mount to proceed!")
        return
    global mounted
    global mount_obj
    if mounted == False:
        #TODO: check errors and exception
        root.config(cursor="wait")
        root.update()
        mount_obj = mount.mount(key_var.get() , secret_var.get() , bucket_var.get() , drive_var.get())
        time.sleep(3)
        root.config(cursor="")
        if mount_alive():
            mount_button.text = "Unmount"
            mounted = True
        else:
            #TODO: more descriptive errors
            messagebox.showwarning("Failed to mount!" , "Please check fs.log for more info")
    else:
        root.config(cursor="wait")
        root.update()
        mount.unmount(mount_obj)
        time.sleep(3)
        root.config(cursor="")
        if mount_alive():
            mount_button.text = "Mount"
            mounted = False
        else:
            #TODO: more descriptive errors
            messagebox.showwarning("Failed to unmount!" , "Please check fs.log for more info")
    
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
choices = { 'Enter AWS Keys above to load bucket list...'}
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

#TODO: start yas3fs
#TODO: set icon

# last row
row = row + 1
mount_button = Button(root, text = '   Mount   ', command=mount_command, **default_style_kwarg)
mount_button.grid(row = row , column = 1 , columnspan = 2, **default_grid_kwarg)
root.mainloop()
