import keyboard
import time
import mouse
from threading import Thread
import win32con
import win32gui
import os, sys
import tkinter as tk
from PIL import ImageTk, Image
import winsound


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def setClickthrough(hwnd):
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)

root= tk.Tk()
# Make the root window always on top
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0)
# Turn off the window shadow
root.wm_attributes("-transparentcolor", "#000000")
title = "AutoClick"
root.title(title)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.config(bg='#000000')

ico = resource_path('ico.ico')
ico = ImageTk.PhotoImage(Image.open(ico))
root.iconphoto(False, ico)

# Hide the root window drag bar and close button
# root.overrideredirect(1)
root.wm_attributes('-fullscreen', 'True')
  
canvas1 = tk.Canvas(root, width = 160, height = 80)
canvas1.pack()
canvas1.place(relx=0.9, rely=0.05)
label1 = tk.Label(root, text=f'Looping click\nctrl+C loop click\nctrl+V break loop\nctrl+Z exit program', fg='blue', font=('helvetica', 12, 'bold'), justify=tk.LEFT)
win_id = canvas1.create_window(70, 35, window=label1)

setClickthrough(canvas1.winfo_id())
setClickthrough(label1.winfo_id())

running = False
loop = True

def breakloop():
    global loop, running
    root.wm_attributes("-alpha", 0)
    winsound.MessageBeep(winsound.MB_ICONHAND)
    loop = False
    running = False
    
def loop_click():
    global loop
    
    while loop:
        mouse.click()
        time.sleep(0.05)

def start_click():
    global loop, running
    root.wm_attributes("-alpha", 0.24)
    winsound.MessageBeep(winsound.MB_OK)
    if not running:
        loop = True
        running = True
        Thread(target = loop_click).start()

def exit_app():
    os._exit(0)

keyboard.add_hotkey('CTRL+C', start_click)
keyboard.add_hotkey('CTRL+V', breakloop)
keyboard.add_hotkey('CTRL+Z', exit_app)

# # or this
# while True:
#     # Wait for the next event.
#     event = keyboard.read_event()
#     if event.event_type == keyboard.KEY_DOWN and event.name == 'space':
#         print('space was pressed')
#     else:
#         print(event.name)

root.mainloop()