import Tkinter as tk
from Tkinter import * #are these two lines not equivalent?? choose one? :)  -S
import tkFileDialog as filedialog
import encrypt as enc
import mongodrive2 as dab
import smove2 as updown
import pymongo
import vlc
import time
import thread
import threading

global appP
global editP
global viewhandler
global username
global password
global encKey
global songList
global songBox
global logged
global logP
global logBackButton
global newButton
global idolP
global idolBox
global pausePressed
global player
global song
global songLock

username = ''
password = ''
encKey = ''
songList = ''
logged = 0
pausePressed = True

songLock = threading.Lock()

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
        global username

        def back():
            viewHandler.showApp(viewhandler)

        backButton = tk.Button(self, text="Back", command = back)
        backButton.pack(side="top", fill = "x", anchor = "w")

        squadLabel = tk.Label(self, text="Squad Member: (Enter just first name)")
        squadLabel.pack()
        squadEntry = tk.Entry(self, text='', width=16)
        squadEntry.pack()

        def addSquad():
            fan = str(squadEntry.get())
            dab.new_squad_mem(username, fan)

        def removeSquad():
            fan = str(squadEntry.get())
            dab.rmv_squad_mem(username, fan)

        addButton = tk.Button(self, text="Add member", command = addSquad)
        addButton.pack(side="top", fill = "x", anchor = "w")

        removeButton = tk.Button(self, text="Remove Member", command = removeSquad)
        removeButton.pack(side="top", fill = "x", anchor = "w")

class idolPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global viewhandler
        global idolBox

        def back():
            viewHandler.showApp(viewhandler)

        backButton = tk.Button(self, text="Back", command = back)
        backButton.pack(side="top", fill = "x", anchor = "w")

        idolLabel = tk.Label(self, text="Idols:")
        idolLabel.pack()
        
        scrollbar = tk.Scrollbar(self, orient="vertical")
        idolBox = tk.Listbox(self, yscrollcommand = scrollbar.set)

        scrollbar.config(command=idolBox.yview)
        scrollbar.pack(side="right", fill="y")
        #scrollbar.grid(row=0,column=2, rowspan = 3)
        idolBox.pack(side="top", fill="both", expand=True)

class appPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global viewhandler
        global username
        global password
        global songList
        global songBox
        global idolBox

        songLabel = tk.Label(self, text='Enter name of song to be uploaded')
        songLabel.pack(side='top')
        songEntry = tk.Entry(self, width=25)
        songEntry.pack(side='top')

        def upload():
            global encKey
            global username
            global songBox

            playFile = filedialog.askopenfilename()
            encryptFile = enc.encrypt_song(playFile, encKey)
            songName = songEntry.get()
            path = 'ulmusic/' + songName
            with open(path, 'wb') as encFile:
                encFile.write(encryptFile)
            if(len(songName) > 0):
                dab.new_song(username, songName)
                updown.upload(songName, path)
                songBox.insert(END, songName)

        uploadButton = tk.Button(self, text = "Upload", command = upload)
        uploadButton.pack(side="top", fill = "x", anchor = "w")
        #uploadButton.grid(row=4, column=2, sticky = N+S+E+W)

        def edit():
            global logBackButton
            global newButton

            logBackButton.config(state=NORMAL)
            newButton.config(state=DISABLED)
            viewHandler.showLogin(viewhandler)

        editButton = tk.Button(self, text = "Edit Squad", command = edit)
        editButton.pack(side="top", fill = "x", anchor = "e")
        #editButton.grid(row=5,column=2, sticky = N+S+E+W)

        def idols():
            global idolBox
            global viewhandler
            global username

            idolList = dab.get_idols(username)
            for item in idolList:
                idolBox.insert(END, item)
            viewHandler.showIdol(viewhandler)

        idolButton = tk.Button(self, text="Idols", command = idols)
        idolButton.pack(side="top", fill = "x", anchor = "e")

        songNameLabel = tk.Label(self, text = "No Song Playing")

        playFile = ""
        def load():
            global username
            global pausePressed
            global player
            global song

            songSel = songBox.curselection()
            song = songBox.get(songSel[0])
            updown.download(song, "/dlmusic/")
            path = 'dlmusic/' + 'dlc' + song + '.mp3'

            decKey = dab.get_key(username, song)
            decryptFile = enc.decrypt_song(path, decKey)

            decSong = 'dlmusic/dec' + song + '.mp3'
            with open(decSong, 'w') as unenc:
                unenc.write(decryptFile)
            print("Done Decrypt")

            #Play the music
            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(decSong)
            media.get_mrl()
            player.set_media(media)
            songNameLabel["text"] = song + " ready to play"

        def playSong():
            global player
            global song
            global pausePressed
            global songLock
            
            playing = set([1,2,3,4])
            player.play()
            time.sleep(3)
            duration = player.get_length() / 1000
            mm, ss = divmod(duration, 60)
            while True:
                state = player.get_state()
                if state not in playing:
                    break 
                elif not pausePressed:
                    currentTime = player.get_time() / 1000
                    cmm, css = divmod(currentTime, 60)
                    songLock.acquire()
                    songNameLabel["text"] = "Playing " + song + ". Time: " + "%02d:%02d/%02d:%02d" % (cmm,css,mm,ss)
                    songLock.release()
                continue

        def play():
            global pausePressed
            global player
            global song

            pausePressed = not pausePressed
            if playButton["text"] == "Play":
                playButton["text"] = "Pause"
                thread.start_new_thread(playSong, ())
            elif playButton["text"] == "Pause":
                player.pause()
                playButton["text"] = "Resume"
            else:
                player.play()
                playButton["text"] = "Pause"

            if pausePressed:
                songLock.acquire()
                songNameLabel["text"] = "Paused " + song + "."
                songLock.release()
            

        playButton = tk.Button(self, text = "Play", command = play)
        playButton.pack(side = "bottom")

        songNameLabel.pack(side="bottom")

        loadButton = tk.Button(self, text = "Load", command = load)
        loadButton.pack(side="bottom")
        #playButton.grid(row=4, column=0, rowspan = 2, columnspan = 2, sticky = N+S+E+W)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        songBox = tk.Listbox(self, yscrollcommand = scrollbar.set)

        scrollbar.config(command=songBox.yview)
        scrollbar.pack(side="right", fill="y")
        #scrollbar.grid(row=0,column=2, rowspan = 3)
        songBox.pack(side="bottom", fill="both", expand=True)
        #songBox.grid(row=0, column=0, rowspan = 3, columnspan = 2)
        
class loginPage(Page):
    def __init__(self, *args, **kwargs):
      Page.__init__(self, *args, **kwargs)

      global viewhandler
      global encKey
      global logged
      global logBackButton
      global failLabel
      global newButton

      userLabel = tk.Label(self, text="Username:")
      userLabel.pack(side="top")
      userEntry = tk.Entry(self, text='', width=16)
      userEntry.pack(side="top")

      passLabel = tk.Label(self, text="Password:")
      passLabel.pack(side="top")
      passEntry = tk.Entry(self, text='', show="*", width=16)
      passEntry.pack(side="top")

      def back():
        viewHandler.showApp(viewhandler)

      logBackButton = tk.Button(self, text="Back", command = back)
      logBackButton.pack(side="bottom", fill = "x", anchor = "w")
      logBackButton.config(state=DISABLED)

      def login():
        global songList
        global username
        global password
        global songBox
        global encKey
        global logged

        if(logged == 0):
            username = userEntry.get()
            password = passEntry.get()
            encKey = enc.get_user_hash(username, password)
            if(dab.valid_login(username, password)):
                songList = dab.get_songs(username, password)
                for item in songList:
                    songBox.insert(END, item)
                dab.store_key(encKey, username, password)
                
                logged = 1
                passEntry.delete(0, 'end')

                viewHandler.showApp(viewhandler)
        else:
            if((userEntry.get() == username) and (passEntry.get() == password)):
                viewHandler.showEdit(viewhandler)

      loginButton = tk.Button(self, text = "Login", command = login)
      loginButton.pack(side="top")

      def newUser():
		global username
		global password
		global encKey
		global logged

		username = userEntry.get()
		password = passEntry.get()
		encKey = enc.get_user_hash(username, password)
		if(dab.new_user(username, password)):
			dab.store_key(encKey, username, password)
			logged = 1
			passEntry.delete(0, 'end')
			viewHandler.showApp(viewhandler)
		  
      newButton = tk.Button(self, text = "New User", command = newUser)
      newButton.pack(side="top")

class viewHandler(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        global viewhandler
        global appP
        global editP
        global logP
        global idolP

        viewhandler = self

        logP = loginPage(self)
        appP = appPage(self)
        editP = editPage(self)
        idolP = idolPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        logP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        appP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        editP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        idolP.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        logP.show()

    def showLogin(self):
        global logP
        logP.show()

    def showApp(self):
        global appP
        appP.show()

    def showEdit(self):
        global editP
        editP.show()

    def showIdol(self):
        global idolP
        idolP.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = viewHandler(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("SafeSound")
    root.wm_geometry("400x400")
    root.mainloop()
