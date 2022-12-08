import numpy as np
import sys
from suite2p.default_ops import default_ops
from suite2p.run_s2p import run_s2p
from glob import glob
import os

# set processing parameters
# start with defaults
ops = default_ops()

# these are the parameters we are pretty sure about so far
ops['nchannels'] = 2
ops['fs'] = 30
ops['tau'] = 1.5
ops['align_by_chan'] = 2

# change any other parameters you want here
# parameter docs here but not totally up to date :(
# https://suite2p.readthedocs.io/en/latest/settings.html


# set the data directories to process

# if you just have one directory, put it in the list below
fns = ['/usr/people/iwahle/501b_2p/data/raw/f5_f/']

# if you want to go through multiple directories, uncomment this instead of line above
# data_path = '/usr/people/iwahle/501b_2p/data/raw/'
# fns = glob(data_path + 'f*_f/')

# this will package up the data paths and generate directories for the results
db = []
for i in range(len(fns)):
    if not os.path.exists(fns[i].replace('raw','processed')):
        os.mkdir(fns[i].replace('raw','processed'))
    db.append({'data_path' : [fns[i]], 'save_folder' : fns[i].replace('raw','processed')})

# run the pipeline
for dbi in db:
    opsEnd=run_s2p(ops=ops,db=dbi)

