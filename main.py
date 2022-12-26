#import modules:
from tkinter import Tk, PhotoImage
from tkinter.ttk import Entry, Button
import sv_ttk
from re import sub as replace
from time import sleep as delay
from keyboard import press as keyboard_press, press_and_release as keyboard_press_and_release, write as keyboard_write, release as keyboard_release
#import sys
from sys import exit #for some reason pyinstaller applications don't terminate using the normal exit() or quit() functions.
#from os import path
#for pyinstaller "additional files":
#def resource_path(relative_path): #with help from https://stackoverflow.com/a/13790741/
#    try:
#        base_path = sys._MEIPASS
#    except Exception:
#        base_path = path.abspath(".")
#    return path.join(base_path, relative_path)

tk = Tk() #create Tk master
sv_ttk.use_dark_theme() #set dark theme of window
tk.wm_overrideredirect(True) #hide the x button
tk.eval('tk::PlaceWindow . center') #open it in the center of the screen

#SplashScreen:
splashscreen_photo = PhotoImage(file="jot_data/splashscreen.png")
splashscreen = Button(image=splashscreen_photo)
splashscreen.pack()
tk.update()
delay(3)
splashscreen.pack_forget()
del splashscreen, splashscreen_photo

tk.attributes('-topmost', 'true') #make this window stay above all others
tk.minsize(347, 34)
tk.attributes("-alpha", 0.9)
#open window where it was last opened, or let it stay where splashscreen was shown.
try:
    with open("jot_data/geometry", "r") as geometryFile:
        tk.geometry(geometryFile.read())
except:
    pass
    
def Convert():
    #InputText_str = Entry.get(1, "end")
    output = replace("ی", "ي", InputText.get())
    """
    OutputText.config(state="enabled")
    OutputText.delete(0, "end")
    OutputText.insert(0, output)
    OutputText.config(state="disabled")
    tk.clipboard_clear()
    tk.clipboard_append(output)
    """
    #delay(1)
    keyboard_press("alt")
    #delay(0.25)
    keyboard_press_and_release("tab")
    #delay(0.25)
    keyboard_release("alt")
    delay(0.25) #wait for the window to close. you may see the screen flash, it is the window that opens when alt+tab is pressed
    keyboard_write(output)
    keyboard_press_and_release("enter")
    InputText.delete(0, "end")
def close():
    with open("jot_data/geometry" ,"w") as geometryFile:
        geometryFile.write(tk.winfo_geometry())
    exit()
change_transparency = True #this is used for preventing the following function from running twice
def transparency_7(Event):
    global change_transparency
    if change_transparency:
        i = 1.0
        while i >= 0.7:
            tk.attributes("-alpha", i)
            i -= 0.1
            #Sleep some time to make the transition not immediate
            delay(0.05)
    change_transparency = False
def transparency10(Event):
    global change_transparency
    change_transparency = True
    tk.attributes("-alpha", 1)
def Disable_changing_transparency():
    tk.bind("<Enter>", lambda a: a)
    tk.bind("<Leave>", lambda a: a)
def Enable_changing_transparency():
    tk.bind("<Enter>", transparency10)
    tk.bind("<Leave>", transparency_7)
def Drag(Event):
    Disable_changing_transparency()
    tk.geometry("+{}+{}".format(Event.x_root, Event.y_root))

InputText = Entry(tk, width=30, justify="center")
Send_image = PhotoImage(file="jot_data/send.png") #send icon. from icons8.com
ReplaceAndSend_btn = Button(tk, image=Send_image, command=Convert)
Close_image = PhotoImage(file="jot_data/close.png") #close icon. from icons8.com
Close_btn = Button(tk, image=Close_image, command=close)
Drag_image = PhotoImage(file="jot_data/drag.png") #drag icon. also from icons8.com
Drag_btn = Button(tk, image=Drag_image)
#buttons = Frame(tk)
#InputText.pack(side="left", expand=True, fill="both")
#buttons.pack(side="left")
#ReplaceAndSend_btn.pack(side="left")
#Close_btn.pack(side="left")
Drag_btn.grid(row=0, column=0)
InputText.grid(row=0, column=1)
ReplaceAndSend_btn.grid(row=0, column=2)
Close_btn.grid(row=0, column=3)

InputText.bind("<Return>", lambda Event: Convert()) #lambda is used so Event won't be given as an argument to Convert function


#Close_btn.bind("<Button-3>", ShowHideButtons) #toggle visibility of - [] x buttons. used for moving/resizing window.
#Drag_btn.bind("<B1-Motion>", lambda Event: tk.geometry("+{}+{}".format(Event.x_root, Event.y_root)))
Drag_btn.bind("<B1-Motion>", Drag)
Drag_btn.bind("<ButtonRelease>", lambda Event: Enable_changing_transparency())
ReplaceAndSend_btn.bind("<Button-3>", lambda Event: InputText.delete(0, "end")) #clear Entry when "send" button is right-clicked
Enable_changing_transparency()
tk.mainloop()
