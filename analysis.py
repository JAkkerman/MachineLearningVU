# import pandas as pd
import sys
import hdf5_getters as get
import h5py
import os
import numpy as np

'''
This loop creates a dictionary with the directory paths as keys and the
filenames as values
'''
paths = {}
for dirpath, dirnames, filenames in os.walk('MillionSongSubset/data/A'):
    if len(filenames) > 0 and len(dirnames) == 0:
        paths[dirpath] = filenames

mbtags = []
for key, folder in paths.items():
    for file in folder:
        h5 = get.open_h5_file_read(key + '/' + file)
        tags = get.get_artist_mbtags(h5)
        mbtags += [tags]

genres = []
for tag in mbtags:
    for genre in tag:
        if genre not in genres:
            genres.append(genre)

print(len(genres))
