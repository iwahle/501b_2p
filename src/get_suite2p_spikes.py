''' 
This code has been modified from suite2p_hybrid_1212.ipynb written by Dexter Tsin
'''

# 1. Import packages
import numpy as np
from skimage.io import imread
import os 

from suite2p import default_ops
from suite2p.gui.drawroi import masks_and_traces
from suite2p.io.binary import BinaryFile as BF
from suite2p.io.binary import BinaryRWFile as RW
from suite2p.detection import detection_wrapper
from suite2p.extraction import extraction_wrapper, oasis, preprocess



def main(roi_fp, reg_file_fp, save_path):

    # load roi mask
    rois = imread(roi_fp)
    uniq_val = np.unique(rois.flatten())

    # construct stats dict in format compatible with suite2p
    # stat should be a list containing all the x/y pixels locations and the 
    # lambda values (1 in this case),
    # median is just the center of the ROI
    stats_0 = []
    for idx, val in enumerate(uniq_val[1:]):
        coordinates = np.where(rois == val)
        stats_0.append({
            'xpix' : coordinates[0].flatten(),
            'ypix' : coordinates[1].flatten(),
            'lam' : np.ones(coordinates[0].shape),
            'med' : [np.mean(coordinates[0].flatten()), np.mean(coordinates[1].flatten())]
            }
        )
        
    # overwrite default ops to match our experimental setup
    ops = default_ops()
    ops["fs"] = 30
    ops['tau'] = 1.5
    ops['reg_file'] = reg_file_fp
    ops['Lx'] = 512
    ops['Ly'] = 512

    # get spikes
    stat_orig = {}
    F, Fneu, F_chan2, Fneu_chan2, spks, ops, manual_roi_stats = masks_and_traces(
        ops, stats_0, stat_orig)

    # save F and spikes
    np.save(os.path.join(save_path, 'suite2p_F.npy'), F)
    np.save(os.path.join(save_path, 'suite2p_spikes.npy'), spks)

if __name__=='__main__':
    fly_dirs = ['f2_f', 'f4_f', 'f5_f_depth34', 'f5_f_depth54']
    data_path = '/usr/people/iwahle/501b_2p/data/raw'
    for fly_dir in fly_dirs:
        print('Current fly: ', fly_dir)
        roi_fp = os.path.join(data_path, fly_dir, 'y.ome.tiff')
        reg_file_fp =  os.path.join(data_path, fly_dir, 'data.bin')
        save_path = os.path.join(data_path.replace('raw', 'processed'), fly_dir)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        main(roi_fp, reg_file_fp, save_path)