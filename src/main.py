#!/usr/bin/env python

import json
import os
import datetime
import sys

from core.imglib import *
from contouring.ContouringFilter import ContouringFilter


def get_config(file_path):
    global config
    with open(file_path, 'r') as f:
        config = json.load(f)

if __name__ == '__main__':

    get_config(sys.argv[1])

    if not os.path.isdir(config['outfolder']) :
        os.makedirs(config['outfolder'])

    for item in sorted(os.listdir(config['inputfolder'])):
        itemPath = os.path.join(config['inputfolder'], item)
        if item.endswith(".png"):
            filter = ContouringFilter(itemPath, config['outfolder'])
            filter.processImage()
            #filter.writeSVG()



    print('Processing finished')
