""""

"""
played_songs =[] # total song in music directory
total_song = 0
played_total_song = 0
repeat = False
import os,subprocess

BASE_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/'))
print(BASE_DIR)
music_dir=os.path.join(BASE_DIR,'media/music/')


path, dirs, files = next(os.walk(music_dir))
total_song = len(files)

print(path)

import random


# Printing original list
print("The original list is : " + str(files))

# to shuffle a list
def SuffleList(list):
    for i in range(len(list) - 1, 0, -1):
        # Pick a random index from 0 to i
        j = random.randint(0, i + 1)

        # Swap arr[i] with the element at random index
        list[i], list[j] = list[j], list[i]

    # Printing shuffled list
    print("The shuffled list is : " + str(list))
    return list


files = SuffleList(files)

while True:
    i = random.randint(0, total_song-1)
    file_name = files[i]


    if file_name not in played_songs: #
        played_songs.append(i)
    else:
        files = SuffleList(files)
        pass

    music_file  = os.path.join(music_dir,file_name)

    subprocess.call(["ffplay", "-nodisp", "-autoexit", music_file])
    played_total_song+=1

    if played_total_song == total_song:
        played_songs = []




