# !/usr/bin/python3
import os, pygame
#plays mp3 file
class Play(object):
    def __init__(self):
        self.paused = False
        self.counter = 0
        self.volume = 0.5

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def prev(self, dic):
        if self.counter == 0:
            self.counter = len(dic) - 1
        else:
            self.counter -= 1
        prev = list(dic.keys())[self.counter]
        print(prev, self.counter)
        pygame.mixer.music.load("songs/"+prev)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.paused = False

    def next(self, dic):
        if self.counter == len(dic) - 1:
            self.counter = 0
        else:
            self.counter += 1
        prev = list(dic.keys())[self.counter]
        print(prev, self.counter)
        pygame.mixer.music.load("songs/"+prev)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.paused = False

    def StartSong(self, song, dic):
        pygame.mixer.music.load("songs/"+song)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.counter = dic[song]
        self.paused = False

    def volume_slider(self, n):
        self.volume = int(n) / 100
        pygame.mixer.music.set_volume(self.volume)


def add_new(): #scans songs.csv and checks if any songs not already in playlist
    l=set()
    for file in os.listdir("songs"):
        with open("songs.csv", "r+") as f:
            if file+'\n' not in f.readlines():
                l.add(file)
    with open("songs.csv", "a") as f:
        l = sorted(list(l))
        for file in l:
            f.write(file+"\n")

def FullList(): #Opens songs.csv and returns them as a numbered dictionary
    i = 0
    d = {}
    with open("songs.csv","r") as s:
        for f in s.readlines():
            f = f.strip()
            d[f] = i
            i += 1
    return d