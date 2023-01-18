#import modules (the less the better):
from tkinter import Tk, PhotoImage, Menu
from tkinter.ttk import Entry, Button
import sv_ttk
from re import sub as replace
from time import sleep as delay
from keyboard import press as keyboard_press, press_and_release as keyboard_press_and_release, write as keyboard_write, release as keyboard_release
from sys import exit #for some reason pyinstaller applications don't terminate using the normal exit() or quit() functions.

tk = Tk() #create Tk master
sv_ttk.use_dark_theme() #set dark theme of window
tk.wm_overrideredirect(True) #hide the x button
tk.eval('tk::PlaceWindow . center') #open it in the (not-so-exactly) center of the screen

#SplashScreen:
splashscreen_photo = PhotoImage(file="jot_data/splashscreen.png")
splashscreen = Button(tk, image=splashscreen_photo)
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
    with open("jot_data/.geometry", "r") as geometryFile:
        tk.geometry(geometryFile.read())
except:
    pass

#window functions:
def Convert(): #convert all "ی"s (if any) and send the converted message.
    output = replace("ی", "ي", InputText.get())
    #alt+tab to focus on the application that has the textbox selected:
    keyboard_press("alt")
    #delay(0.25)
    keyboard_press_and_release("tab")
    #delay(0.25)
    keyboard_release("alt")
    delay(0.45) #wait for the window to close. you may see the screen flash, it is the window that opens when alt+tab is pressed
    keyboard_write(output)
    keyboard_press_and_release("enter") #send the typed message.
    InputText.delete(0, "end") #remove everything in the entry
def close():
    with open("jot_data/.geometry" ,"w") as geometryFile:
        geometryFile.write(tk.winfo_geometry())
    exit()
change_transparency = True #this is used for preventing the following function from running twice
def transparency_7(Event): #make window a little opaque
    global change_transparency
    if change_transparency:
        i = 1.0
        while i >= 0.7:
            tk.attributes("-alpha", i)
            i -= 0.1
            #Sleep some time to make the transition not immediate
            delay(0.05)
    change_transparency = False
def transparency10(Event): #make window plain
    global change_transparency
    change_transparency = True
    tk.attributes("-alpha", 1)
def Disable_changing_transparency(): #disable fading
    tk.bind("<Enter>", lambda a: a)
    tk.bind("<Leave>", lambda a: a)
def Enable_changing_transparency(): #enable fading
    tk.bind("<Enter>", transparency10)
    tk.bind("<Leave>", transparency_7)
def Drag(Event): #drag the window to where the mouse pointer is.
    Disable_changing_transparency() #prevent changing opacity when window is being dragged.
    tk.geometry("+{}+{}".format(Event.x_root, Event.y_root))
#entry right click menu:
#functions:
def Cut():
    tk.clipboard_clear() #clear clipboard or copied text will contain previous copied text!
    tk.clipboard_append(InputText.selection_get()) #add what is selected to clipboard
    #remove selected text:
    ##DOES NOT WORK FOR AN ENTRY!
    """
    Selection_beginning = InputText.count("1.0", "sel.first")
    Selection_end = InputText.count("1.0", "sel.last")
    oldText = InputText.get(0.0, END)
    newText = oldText[0:Selection_beginning[0]] + Selection_end[to[0]:]
    InputText.delete(0.0, END)
    InputText.insert(0.0, newText)
    """
def Copy():
    tk.clipboard_clear() #clear clipboard or copied text will contain previous copied text!
    tk.clipboard_append(InputText.selection_get())
def Paste():
    InputText.insert("end", tk.clipboard_get())
def open_right_click_menu(Event):
    window_coordinates = [int(tk.geometry().split("+")[1])+20, int(tk.geometry().split("+")[2])]
    tk.call('tk_popup', right_click_menu, window_coordinates[0]+Event.x, window_coordinates[1]+Event.y)
#making the right click menu:
right_click_menu = Menu()
for label, command in [("Cut", Cut), ("Copy", Copy), ("Paste", Paste)]:
    right_click_menu.add_command(label=label, command=command)

#create widgets:
InputText = Entry(tk, width=30, justify="right")
Send_image = PhotoImage(file="jot_data/send.png") #send icon. from icons8.com
ReplaceAndSend_btn = Button(tk, image=Send_image, command=Convert)
Close_image = PhotoImage(file="jot_data/close.png") #close icon. from icons8.com
Close_btn = Button(tk, image=Close_image, command=close)
Drag_image = PhotoImage(file="jot_data/drag.png") #drag icon. also from icons8.com
Drag_btn = Button(tk, image=Drag_image)
#place widgets on screen:
Drag_btn.pack(side="left", fill="y")
InputText.pack(side="left", fill="both", expand=True)
ReplaceAndSend_btn.pack(side="left", fill="y")
Close_btn.pack(side="left", fill="y")

InputText.bind("<Return>", lambda Event: Convert()) #lambda is used so Event won't be given as an argument to Convert function
Drag_btn.bind("<B1-Motion>", Drag)
Drag_btn.bind("<ButtonRelease>", lambda Event: Enable_changing_transparency()) #enable changing transparency after dragging the window has finished.
InputText.bind("<Button-3>", open_right_click_menu)
ReplaceAndSend_btn.bind("<Button-3>", lambda Event: InputText.delete(0, "end")) #delete written things when Send button is right-clicked
Enable_changing_transparency()
tk.mainloop()