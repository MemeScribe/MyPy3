# !/usr/bin/python3
from tkinter import * #Importing Tkinter
from PIL import Image, ImageTk #Importing Image handling libraries
from MyPy3Functions import Play
import MyPy3Functions as func
import os, pygame #Importing os pathfinding, Pygame mixer tools and external functions

# Initialising application window size, background, favicon ect.
root = Tk()
root.title('MyPy3')
root.geometry('1900x1000')
root.configure(background = '#302f29')
imgicon = PhotoImage(file=os.path.join('~/MyPy3/ico/logo_ico/','ms-icon-310x310.png'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)  

# scanning for new songs
func.add_new()

# Assigning songs to a dictionary for labeling
song_list = func.FullList()

# placing Album image above songs list
load = Image.open("Album.jpg")
load = load.resize((250,250))
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.grid(row = 0, column = 0)

# Initialising Pygame mixer
pygame.init()
pygame.mixer.init()
obj = Play() #Class object used for music menu functions

# Creating song list using a for loop to generate buttons based on the number of songs in 'song_list' dict
btn_dic = {}
row = 7
for k in song_list:
    action = lambda x = k: obj.StartSong(x, song_list)
    btn_dic[k] = Button(root, text = k[:-4], width="30", anchor="w",
     command = action)
    btn_dic[k].grid(row = row, column = 0, pady = 5)
    row += 1
#creating Play/Pause, next and prev buttons

play_pause = Button(root, text = "Play/Pause", command = obj.toggle)
play_pause.place(x=900, y=900)

action = lambda x=song_list: obj.prev(x)
prev = Button(root, text = "Prev", command = action)
prev.place(x=825, y=900)

action = lambda x=song_list: obj.next(x)
skip = Button(root, text = "Next", command = action)
skip.place(x=1020, y=900)

# creating volume slider
var = DoubleVar()
action = lambda x=var: obj.volume_slider(x)
volume = Scale(root, variable=var, orient=HORIZONTAL, length=200, command = action)
volume.place(x=1100, y=900)
volume.set(50)

root.mainloop()
