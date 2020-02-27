# import pandas as pd
import sys
import hdf5_getters as get
import h5py
import os
import numpy as np
import operator

"""
This loop creates a dictionary with the directory paths as keys and the
filenames as values
"""
NUMBER_GENRES = 20
GENRE_FILE = 'genres.txt'

def get_paths():
    paths = {}
    for dirpath, dirnames, filenames in os.walk('MillionSongSubset/data/A'):
        if len(filenames) > 0 and len(dirnames) == 0:
            paths[dirpath] = filenames

    return paths


def get_mbtags(paths):
    mbtags = []
    for key, folder in paths.items():
        for file in folder:
            h5 = get.open_h5_file_read(key + '/' + file)
            tags = get.get_artist_terms(h5)
            mbtags += tags.tolist()
            h5.close()

    return mbtags


def count_mbtags(mbtags, numb_genres):
    mbtags_numb = {}
    for el in mbtags:
        if el in mbtags_numb.keys():
            mbtags_numb[el] += 1
        else:
            mbtags_numb[el] = 1

    large_tags = {}
    while len(large_tags) < numb_genres:
        large = max(mbtags_numb.items(), key=operator.itemgetter(1))[0]
        large_tags[large] = mbtags_numb[large]
        del mbtags_numb[large]

    # write genres to text file
    f = open(GENRE_FILE, 'w')
    for el in large_tags:
        poep = el.decode("utf-8")
        f.write(poep + ',' + str(large_tags[el]) + '\n')
    f.close()


if __name__ == '__main__':
    paths = get_paths()
    mbtags = get_mbtags(paths)
    count_mbtags(mbtags, NUMBER_GENRES)
