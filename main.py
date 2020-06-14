import zipfile
import os
import atexit
import shutil
import playsound
import keyboard
import pyautogui
import colorama
from threading import Thread
from time import sleep
from sys import stdout
from mutagen.mp3 import MP3
from datetime import timedelta

def exit_handler():
    try:
        shutil.rmtree('temp')
    except FileNotFoundError:
        pass

def color_print(color, text):
    colorama.init(autoreset = True)
    colors = {'red': colorama.Fore.RED,
              'green': colorama.Fore.GREEN,
              'yellow': colorama.Fore.YELLOW,
              'blue': colorama.Fore.BLUE,
              'magenta': colorama.Fore.MAGENTA,
              'cyan': colorama.Fore.CYAN,
              'white': colorama.Fore.WHITE}
    print(colorama.Style.BRIGHT + colors.get(color) + text)
    colorama.deinit()

exit_handler()
atexit.register(exit_handler)

def counter_updater(length):
    for second in range(length):
        stdout.write("\r" + str(timedelta(seconds = second)) + " / " + str(timedelta(seconds = length)))
        sleep(1)

color_print('magenta', "    ____             _ __   ____  __")
color_print('magenta', "   / __ )__  _______(_) /__/ __ \/ /___ ___  _____  _____")
color_print('magenta', "  / __  / / / / ___/ / //_/ /_/ / / __ `/ / / / _ \/ ___/")
color_print('magenta', " / /_/ / /_/ / /__/ / ,< / ____/ / /_/ / /_/ /  __/ /    ")
color_print('magenta', "/_____/\__,_/\___/_/_/|_/_/   /_/\__,_/\__, /\___/_/")
color_print('magenta', "                                      /____/             ")
song_indexes = []
songs = []
for index, file in enumerate(os.listdir('songs')):
    color_print('yellow', "[" + str(index) + "] " + os.path.splitext(file)[0])
    song_indexes.append(index)
    songs.append(os.path.splitext(file)[0])

while True:
    try:
        song_number = int(input("Wybierz utwór: "))
        break
    except ValueError:
        color_print('red', "Numer musi być liczbą.")

print("\nWybrany utwór: " + songs[song_number])
with zipfile.ZipFile('songs/' + songs[song_number] + '.zip', 'r') as zip_ref:
    zip_ref.extractall('temp')
with open('temp/lyrics.txt') as lyrics_file:
    lyrics = lyrics_file.readlines()

line_index = 0
song_length = int(MP3("temp/song.mp3").info.length)
Thread(target = playsound.playsound, args = ('temp/song.mp3',)).start()
Thread(target = counter_updater, args = (song_length,)).start()
while True:
    try:
        keyboard.wait('F3')
        pyautogui.typewrite(lyrics[line_index].rstrip())
        pyautogui.press('enter')
        line_index += 1
    except IndexError:
        raise SystemExit