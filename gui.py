'''
#SEE THIS LINK
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-applicationrint("hi")
'''
import Tkinter as tk
from Tkinter import *
import tkFileDialog as filedialog
import encrypt as enc
import mongodrive2 as dab
#import smove2 as updown
import pymongo

global appP
global editP
global viewhandler
global username
global password
global key

uri = "mongodb://rondell:weasley@ds125198.mlab.com:25198/squaduga"
client = pymongo.MongoClient(uri)
db = client.get_default_database()

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class editPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global viewhandler

        def back():
            viewHandler.showApp(viewhandler)

        backButton = tk.Button(self, text="Back", command = back)
        backButton.pack(side="top", fill = "x", anchor = "w")

        squadLabel = tk.Label(self, text="Squad Member: (Enter first and last name)")
        squadLabel.pack()
        squadEntry = tk.Entry(self, text='', width=16)
        squadEntry.pack()

        def addSquad():
            name = squadEntry.get()
            print("add " + name + " to squad")

        def removeSquad():
            name = squadEntry.get()
            print("remove " + name + " from squad")

        addButton = tk.Button(self, text="Add member", command = addSquad)
        addButton.pack(side="top", fill = "x", anchor = "w")

        removeButton = tk.Button(self, text="Back", command = removeSquad)
        removeButton.pack(side="top", fill = "x", anchor = "w")

class appPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global viewhandler
        global key

        songLabel = tk.Label(self, text='Enter name of song to be uploaded')
        songLabel.pack(side='top')
        songEntry = tk.Entry(self, width=25)
        songEntry.pack(side='top')

        def upload():
            playFile = filedialog.askopenfilename()
            encryptFile = enc.encrypt_song(playFile, key)

            songName = songEntry.get()

        uploadButton = tk.Button(self, text = "Upload", command = upload)
        uploadButton.pack(side="top", fill = "x", anchor = "w")
        #uploadButton.grid(row=4, column=2, sticky = N+S+E+W)

        def edit():
            viewHandler.showEdit(viewhandler)

        editButton = tk.Button(self, text = "Edit Squad", command = edit)
        editButton.pack(side="top", fill = "x", anchor = "e")
        #editButton.grid(row=5,column=2, sticky = N+S+E+W)

        playFile = ""
        def play():
            songSel = songBox.curselection()
            song = songBox.get(songSel[0])
            print(song)


        playButton = tk.Button(self, text = "Play", command = play)
        playButton.pack(side="bottom")
        #playButton.grid(row=4, column=0, rowspan = 2, columnspan = 2, sticky = N+S+E+W)

        scrollbar = tk.Scrollbar(self, orient="vertical")

        songBox = tk.Listbox(self, yscrollcommand = scrollbar.set)
        '''songBox.insert("end", "one")
        songBox.insert("end", "two")
        songBox.insert("end", "three")'''
        for i in range(0, 30):
            songBox.insert("end", i)

        scrollbar.config(command=songBox.yview)
        scrollbar.pack(side="right", fill="y")
        #scrollbar.grid(row=0,column=2, rowspan = 3)
        songBox.pack(side="bottom", fill="both", expand=True)
        #songBox.grid(row=0, column=0, rowspan = 3, columnspan = 2)
        
class loginPage(Page):
    def __init__(self, *args, **kwargs):
      Page.__init__(self, *args, **kwargs)

      global viewhandler
      global username
      global password
      global key

      username = StringVar(root)
      password = StringVar(root)

      userLabel = tk.Label(self, text="Username:")
      userLabel.pack(side="top")
      userEntry = tk.Entry(self, text='', width=16)
      userEntry.pack(side="top")

      passLabel = tk.Label(self, text="Password:")
      passLabel.pack(side="top")
      passEntry = tk.Entry(self, text='', show="*", width=16)
      passEntry.pack(side="top")

      def login():
        usern = userEntry.get()
        passw = passEntry.get()

        key = enc.get_user_hash(usern, passw)
        if(dab.valid_login(usern, passw)):
            username = usern
            password = passw
            viewHandler.showApp(viewhandler)

      loginButton = tk.Button(self, text = "Login", command = login)
      loginButton.pack(side="top")

class viewHandler(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        global viewhandler
        global appP
        global editP

        viewhandler = self

        logP = loginPage(self)
        appP = appPage(self)
        editP = editPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        logP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        appP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        editP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        logP.show()

    def showApp(self):
        global appP
        appP.show()

    def showEdit(self):
        global editP
        editP.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = viewHandler(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("SafeSound")
    root.wm_geometry("400x400")
    root.mainloop()
