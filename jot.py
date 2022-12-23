#import modules:
from tkinter import *
from tkinter.ttk import *
import sv_ttk
from re import sub as replace
from time import sleep as delay
import keyboard

tk = Tk() #create Tk master
tk.attributes('-topmost', 'true') #make this window stay above all others
tk.minsize(347, 34)
tk.attributes("-alpha", 0.9)
#open window where it was last opened, or open it in the center of screen:
try:
    with open("jot_data/geometry", "r") as geometryFile:
        tk.geometry(geometryFile.read())
except:
    tk.eval('tk::PlaceWindow . center')
tk.wm_overrideredirect(True) #hide the x button
sv_ttk.use_dark_theme() #set dark theme of window
tk.resizable(width=True, height=False) #disable increasing/decreasing window height (but let resizing width remain available)

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
    keyboard.press("alt")
    #delay(0.25)
    keyboard.press_and_release("tab")
    #delay(0.25)
    keyboard.release("alt")
    delay(0.25) #wait for the window to close. you may see the screen flash, it is the window that opens when alt+tab is pressed
    keyboard.write(output)
    keyboard.press_and_release("enter")
    InputText.delete(0, "end")
def close():
    with open("jot_data/geometry" ,"w") as geometryFile:
        geometryFile.write(tk.winfo_geometry())
    exit()
def transparency_7(Event):
    global change_transparency #this is used for preventing this function from running twice
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