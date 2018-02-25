'''
#SEE THIS LINK
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-applicationrint("hi")
'''
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import encrypt as enc

global appP

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class appPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        playFile = ""
        def upload():
            playFile = filedialog.askopenfilename()
            print(playFile)

        uploadButton = tk.Button(self, text = "Upload", command = upload)
        uploadButton.pack(side="top")

        def play():
            print("Gotta Play")

        uploadButton = tk.Button(self, text = "Play", command = play)
        uploadButton.pack(side="top")

        def edit():
            print("Gotta Edit")

        uploadButton = tk.Button(self, text = "Edit Squad", command = edit)
        uploadButton.pack(side="top")



class loginPage(Page):
    def __init__(self, *args, **kwargs):
      Page.__init__(self, *args, **kwargs)
      username = StringVar(root)
      password = StringVar(root)

      userLabel = tk.Label(self, text="Username:")
      userLabel.pack(side="top")
      userEntry = tk.Entry(self, text='', textvariable=username, width=16)
      userEntry.pack(side="top")

      passLabel = tk.Label(self, text="Password:")
      passLabel.pack(side="top")
      passEntry = tk.Entry(self, text='', textvariable=password, show="*", width=16)
      passEntry.pack(side="top")

      def login():
        usern = userEntry.get()
        passw = passEntry.get()

        entered = enc.get_user_hash(usern, passw)
        if(entered == enc.get_user_hash("sah", "dude")):
            viewHandler.showApp()

      loginButton = tk.Button(self, text = "Login", command = login)
      loginButton.pack(side="top")

class viewHandler(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        global appP
        logP = loginPage(self)
        appP = appPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        logP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        appP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        logP.show()

    def showApp():
      global appP
      appP.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = viewHandler(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("SafeSound")
    root.wm_geometry("400x400")
    root.mainloop()
