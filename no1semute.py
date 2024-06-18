#Coded and made by no1se
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from PIL import Image, ImageTk
import subprocess

default_keybind = '`'
listener_for_key = None

def mic_status():
    result = subprocess.run(["amixer", "get", "Capture"], capture_output=True, text=True)
    return "off" in result.stdout

def update_mic_status():
    if mic_status():
        status_label.config(text="Mic Off", fg="red")
    else:
        status_label.config(text="Mic On", fg="green")
    root.after(1000, update_mic_status)

def toggle_mute():
    subprocess.run(["amixer", "set", "Capture", "toggle"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    update_mic_status()

def bye_bitch():
    if messagebox.askokcancel("Quit", "Oh hell naw! Are you sure?"):
        listener.stop()
        root.destroy()

def set_keybind():
    keybind_window = tk.Toplevel(root,bg="black")
    keybind_window.title("Set Keybind")
    keybind_window.geometry("300x100")
    root.resizable(False, False)

    listen_for_key_label = tk.Label(keybind_window, text="Press the desired key", font=("Helvetica", 12))
    listen_for_key_label.pack(pady=20)

    def on_key_press(key):
        global default_keybind, listener, listener_for_key
        try:
            keybind_window.destroy()
            if hasattr(key, 'char') and key.char:
                the_key = key.char
            elif hasattr(key, 'name'):
                the_key = key.name
            else:
                the_key = str(key)
                
            default_keybind = the_key
            keybind_window.destroy()
            if listener_for_key is not None:
                listener_for_key.stop()
                listener_for_key = None
            listener.stop()
            listener = keyboard.GlobalHotKeys({default_keybind: toggle_mute})
            listener.start()
        except Exception as e:
            print("fuck")

    listener_for_key = keyboard.Listener(on_press=on_key_press)
    listener_for_key.start()

root = tk.Tk()
root.title("no1seMute")
root.geometry("300x100")
root.config(bg="black")
root.resizable(False, False)

logo_path = "logo.png"
img = Image.open(logo_path)
img= img.resize((50,50), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)

left_image_label = tk.Label(root, image=photo,bg="black")
left_image_label.image = photo 
left_image_label.pack(side="left", padx=20)

right_image_label = tk.Label(root, image=photo,bg="black")
right_image_label.image = photo  
right_image_label.pack(side="right", padx=20)


status_label = tk.Label(root,bg="black")
status_label.pack(pady=20)

set_keybind_button = tk.Button(root, text="Set Keybind", command=set_keybind,bg="white",fg="black",relief="flat")
set_keybind_button.pack(pady=10)

update_mic_status()

listener = keyboard.GlobalHotKeys({default_keybind: toggle_mute})
listener.start()

root.protocol("WM_DELETE_WINDOW", bye_bitch)

root.mainloop()

#I'm tired. Was it worth losing sleep for?