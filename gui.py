from tkinter import *
from tkinter import ttk

root = Tk()
root.title("SafeSound")

#Set up framework
mainframe = ttk.Frame(root, padding="30 30 80 80")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text = "Hello World").grid(row=2, column = 1, sticky = W)

ttk.Separator(mainframe, orient=VERTICAL).grid(rowspan=3, column = 2, sticky = E)

root.mainloop()
