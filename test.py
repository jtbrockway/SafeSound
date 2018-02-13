'''
This file is for GUI testing only and should be removed once the GUI is complete
'''

import tkinter as tk
from tkinter import *

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class loginPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       
       username = StringVar(root)
       password = StringVar(root)

       userLabel = tk.Label(self, text="Username:").grid(column=2, row=3)
       userEntry = tk.Entry(self, text='', textvariable=username, width=16).grid(column=2, row=4)

       passLabel = tk.Label(self, text="Password:").grid(column=2, row=5)
       passEntry = tk.Entry(self, text='', textvariable=password, width=16).grid(column=2, row=6)

class appPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class viewHandler(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        logP = loginPage(self)
        appP = appPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        logP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        appP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        logP.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = viewHandler(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()