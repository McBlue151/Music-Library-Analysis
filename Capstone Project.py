# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:57:49 2022

@author: Ben
"""

import os
from tinytag import TinyTag
import pandas as pd
import time

def main():
    print("Welcome")
    decision = input("Do you want to create a new music data set(y/n)? ").lower()
    if decision == "y":
        folder = input("Please input your music folder location: ")
    
        ALL_FILES = find_all_files(folder)
        CLEANED_LIST = find_music_files(ALL_FILES)
        musicMeta = metadata_lists(CLEANED_LIST)
        pandas_at_work(musicMeta)
    
    if decision =="n":
        try: 
            inputFileName = input("Please input file name: ")
            musicMeta = pd.read_csv(inputFileName)
            pandas_at_work(musicMeta)
        except:
            exit("That file couldn't be opened.")

#find and store all files in folder and subfolders=============================
def find_all_files(folder):    
    ALL_FILES = []
    
    for path, currentDirectory, files in os.walk(folder):
        for file in files:
            all_files = os.path.join(path, file)
            ALL_FILES.append(all_files)
    return ALL_FILES
    
#filter all but mp3 formated files=============================================    
def find_music_files(ALL_FILES):
    CLEANED_LIST = [item for item in ALL_FILES if ".mp3" or ".m4a" in item]
    return CLEANED_LIST

#extra metadata of files into lists============================================
def metadata_lists(CLEANED_LIST):
    TITLE = []
    ARTIST = []
    ALBUM = []
    TRACK = []
    YEAR = []
    GENRE = [] 
    LENGTH = []
    
    for f in CLEANED_LIST:
        audio = TinyTag.get(f)
        if audio.title == "":
            TITLE.append("")
        else:
            TITLE.append(audio.title)
            
        if audio.artist == "":
            ARTIST.append("")
        else:
            ARTIST.append(audio.artist)
            
        if audio.album == "":
            ALBUM.append("")
        else:
            ALBUM.append(audio.album)
        
        if audio.track == "":
            TRACK.append("")
        else:
            TRACK.append(audio.track)
            
        if audio.year == "":
            YEAR.append("")
        else:
            YEAR.append(audio.year)
            
        if audio.genre == "":
            GENRE.append("")
        else:
            GENRE.append(audio.genre)
            
        if audio.duration == "":
            LENGTH.append("")
        else: #convert to hh:mm:ss
            LENGTH.append(time.strftime("%H:%M:%S", time.gmtime(audio.duration)))
            
    data = {"Title": TITLE, "Artist": ARTIST, "Album": ALBUM, "Track": TRACK,
            "Year": YEAR, "Genre": GENRE, "Length": LENGTH}

    musicMeta = pd.DataFrame.from_dict(data)
    musicMeta.to_csv("music metadata.csv")
    return musicMeta

#time for pandas to do its job=================================================
def pandas_at_work(musicMeta):
    print("Here are some metrics about your music library:")
    musicMeta = pd.read_csv("music metadata.csv", engine="python")

    #show which category has missing items
    print("=====================================================================")
    missingMusic = musicMeta.shape[0] - musicMeta.count()
    print("The following number of files are missing details for each category:")
    print(missingMusic)

    #show top 10 artists by song count  
    print("=====================================================================")
    artistCount = musicMeta["Artist"].value_counts()
    print("The top 10 artists with the most songs are:\n",
          artistCount.head(10))

    #show top 10 years by song count
    print("=====================================================================")
    yearCount = musicMeta["Year"].value_counts()
    print("The top 10 years with the most songs are:\n",
          yearCount.head(10))

    #show genre distribution
    print("=====================================================================")
    genreCount = musicMeta["Genre"].value_counts()
    print("The top 10 genres with the most songs are:\n",
          genreCount.head(10))

    #show 10 longest songs
    print("=====================================================================")
    top10len = musicMeta.sort_values("Length", ascending=False)\
             .dropna(subset=["Title", "Artist", "Year", "Genre"]).iloc[0:10,1:]
    print("The 10 longest songs are:\n", 
         top10len)
    print("Thank you and I hope you learned more about your music!")
    
main()