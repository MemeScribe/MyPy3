# !/usr/bin/python3
from tkinter import * #Importing Tkinter
from tkinter import font
from PIL import Image, ImageTk #Importing Image handling libraries
import sqlite3
from sqlite3 import Error
from MyPy3Functions import Play
import MyPy3Functions as func
import os, pygame #Importing os pathfinding, Pygame mixer tools and external functions

path = os.path.expanduser('~/Music/')

# Initialising application window size, background, favicon ect.
root = Tk()
root.title('MyPy3')
root.geometry('1900x1000')
root.configure(background = '#302f29')
imgicon = PhotoImage(file=os.path.join('~/MyPy3/ico/logo_ico/','ms-icon-310x310.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)

# Initialising Pygame mixer
pygame.init()
pygame.mixer.init()
obj = Play() #Class object used for music menu functions
song_ended = pygame.USEREVENT + 1

# Initialising database songs list
db = r"songs.db"
sql_create_songs_table = """ CREATE TABLE IF NOT EXISTS songs (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    length text NOT NULL,
                                    filetype text NOT NULL
                                ); """
conn = func.create_connection(db)
if conn is not None:
    func.create_table(conn, sql_create_songs_table)
else:
    print("Error: Database could not be created.")

names = []
for x in func.select_songname(conn, "*"):
    names.append(x[0])
for files in sorted(os.listdir(path)):
    if files[:-4] not in names:
        pygame.mixer.music.load(path+files)
        length = func.length(files)
        song = (files[:-4],length,files[-3:])
        with conn:
            func.insert_song(conn,song)
try:
    length = length
except NameError:
    for i in range(int(func.select_songname(conn, "*")[-1][-1])):
        func.update_id(conn, (i, func.select_songname(conn, "__ALPHA__")[i][0]))

# placing Album image above songs list
load = Image.open("Album.jpg")
load = load.resize((250,250))
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.grid(row = 0, column = 0)


# Creating song list using a for loop to generate buttons based on the number of songs in 'song_list' dict
btn_dic = {}

canvas = Canvas(root, borderwidth = 0,background="#302f29", width=270, height=750)

frame = LabelFrame(canvas, bg = '#302f29')
frame.grid(row=7,column=0)

scroll = Scrollbar(root, orient="vertical",command=canvas.yview)
scroll.grid(row=7,column=1,sticky="ns")

canvas.configure(yscrollcommand = scroll.set)
canvas.grid(row=7,column=0)
canvas.create_window((0,0), window=frame, anchor="nw")
scroll.config(command=canvas.yview)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

row=7
for x in func.select_songname(conn, "__ALPHA__"):
    action = lambda x = x: obj.StartSong(x[0]+"."+x[1],x[3])
    btn_dic[x[0]] = Button(frame, text = x[0], width="30", anchor="w",
     cursor="hand2", command = action)
    btn_dic[x[0]].grid(row=row, pady=1)
    row += 1
#creating Play/Pause, next and prev buttons
curr_length = obj.length

play_pause = Button(root, text = "Play/Pause", command = obj.toggle)
play_pause.place(x=900, y=900)

action = lambda : obj.prev()
prev = Button(root, text = "Prev", command = action)
prev.place(x=825, y=900)

action = lambda : obj.next()
skip = Button(root, text = "Next", command = action)
skip.place(x=1020, y=900)

# creating volume slider
var = DoubleVar()
action = lambda x=var: obj.volume_slider(x)
volume = Scale(root, variable=var, orient=HORIZONTAL, length=200, command = action)
volume.place(x=1100, y=900)
volume.set(50)

var2 = DoubleVar()
action = lambda x=var2: obj.music_slider(x)
pos = Scale(root, variable=var2, orient=HORIZONTAL, length=1200, showvalue=0, command = action)
pos.place(x=400, y=850)

length_full = Message(root, textvariable=obj.length, width=30)
length_full.place(x=1610,y=860)
curr = "0:00"
length_current = Message(root, textvariable=curr, width=30)
length_current.place(x=390, y=860)

while True:
    var2.set((pygame.mixer.music.get_pos() / 1000) / func.min_to_sec(func.select_songid(conn, obj.counter)[0][2]) * 100)
    curr = func.sec_to_min((pygame.mixer.music.get_pos() / 1000) / func.min_to_sec(func.select_songid(conn, obj.counter)[0][2]) * 100)
    for event in pygame.event.get():
        if event.type == song_ended:
            obj.next()
    root.update()
# root.mainloop()
