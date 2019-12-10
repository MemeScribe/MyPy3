# !/usr/bin/python3
import os, pygame
import sqlite3
import wave
from tkinter import StringVar
from sqlite3 import Error
from mutagen.mp3 import MP3

path = os.path.expanduser('~/Music/')
db = r"songs.db"
song_ended = pygame.USEREVENT + 1
#Class for handling Play menu functions
class Play(object):
    def __init__(self):
        self.paused = False
        self.counter = 0
        self.volume = 0.5
        self.length = StringVar()
        self.length.set("0:00")

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def prev(self):
        conn = create_connection(db)
        self.counter -= 1
        try:
            prev,ftype = select_songid(conn, self.counter)[0][:2]
        except IndexError:
            prev,ftype = select_songname(conn, "*")[-1][:2]
            self.counter = int(select_songname(conn, "*")[-1][3])
        print(prev, length(prev+"."+ftype) ,self.counter)
        pygame.mixer.music.load(path+prev+"."+ftype)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.paused = False
        self.printlen()
        pygame.mixer.music.set_endevent(song_ended)

    def next(self):
        conn = create_connection(db)
        self.counter += 1
        try:
            skip,ftype = select_songid(conn, self.counter)[0][:2]
        except IndexError:
            skip,ftype = select_songid(conn, 0)[0][:2]
            self.counter = 0
        print(skip, length(skip+"."+ftype) ,self.counter)
        pygame.mixer.music.load(path+skip+"."+ftype)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.paused = False
        self.printlen()
        pygame.mixer.music.set_endevent(song_ended)

    def StartSong(self, song, songid):
        self.counter = int(songid)
        print(song, length(song), self.counter)
        pygame.mixer.music.load(path+song)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(song_ended)
        self.paused = False
        self.printlen()

    def printlen(self):
        conn = create_connection(db)
        curr_len = select_songid(conn, self.counter)[0][2]
        self.length.set(curr_len)

    def volume_slider(self, n):
        self.volume = int(n) / 100
        pygame.mixer.music.set_volume(self.volume)

    def music_slider(self, n):
        conn = create_connection(db)
        file = select_songid(conn, self.counter)[0]
        try:
            length = min_to_sec(file[2])
            n = (int(n) / 100) * length
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(n))
        except pygame.error:
            # if file[1] == "wav":
            #     with wave.open(file[0]+".wav") as file:
            #         rate = file.getframerate()
            #         length = file.getnframes()
            # else:
            print("Mypy3 doesn't support filetype:", ftype)


# Functions for handling SQLite3 with songs

def create_connection(db_file):
# create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    # create a table from the create_table_sql statement
    # :param conn: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    # :return:
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_song(conn, song):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    try:
        sql = ''' INSERT INTO songs(name,length,filetype)
                  VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, song)
        return cur.lastrowid
    except Error:
        pass

def update_id(conn, song):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE songs
              SET id = ?
              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, song)
    conn.commit()

def select_songname(conn, song):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    if song == "*":
        cur.execute("SELECT name, filetype, length, id FROM songs ORDER BY id")
    elif song == "__ALPHA__":
        cur.execute("SELECT name, filetype, length, id FROM songs ORDER BY name")
    else:
        cur.execute("SELECT name, filetype, length, id FROM songs WHERE name=?", (song,))
 
    return cur.fetchall()

def select_songid(conn, sid):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT name, filetype, length, id FROM songs WHERE id=?", (sid,))
 
    return cur.fetchall()

# BEGINNING OF NON-SQL FUNCTIONS
# ================================================================================================================================================================================

def length(song):
    pygame.mixer.music.load(path+song)
    if song[-3:] == "mp3":
        song = MP3(path+song)
        sec = int(song.info.length)
        time = str(sec // 60)+":"+str(sec % 60)
    else:
        sec = int(pygame.mixer.Sound(path+song).get_length())
        time = str(sec // 60)+":"+str(sec % 60)
    if len(time) < 4:
        time = time[:2] +"0"+ time[-1]
    return time

def min_to_sec(time):
    return int(time[0]) * 60 + int(time[-2])

def sec_to_min(time):
    return str(time // 60) + ":" + str(time % 60)