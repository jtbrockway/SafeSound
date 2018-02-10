import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont

root = Tk()
usern = ""
passw = ""

class SafeSound(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Comic Sans', size=20, weight="bold")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}
        for F in (LoginPage, AppPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.swapFrame("LoginPage")

    def swapFrame(self, page_name):
        frame=self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    #Set up framework
    mainframe = ttk.Frame(root, padding="30 30 80 80")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    
    username = StringVar(root)
    password = StringVar(root)

    ttk.Label(mainframe, text="Username:").grid(column = 2, row = 3, sticky = W)
    ttk.Entry(mainframe, text='', textvariable=username, width = 16).grid(column=2, row=4)

    ttk.Label(mainframe, text="Password:").grid(column = 2, row = 5, sticky = W)
    ttk.Entry(mainframe, text='', textvariable=password, width = 16, show='*').grid(column=2, row=6)

    def login():
        global usern
        global passw 
        usern = username.get()
        passw = password.get()
        print(usern)
        print(passw)

    ttk.Button(mainframe, text = "Login", command = login).grid(column=2, row=7)

class AppPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    print("hi")



if __name__ == "__main__":
    app = SafeSound()
    app.mainloop()
