import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from tqdm import tqdm
from glob import glob
import os
from suite2p.io.binary import BinaryFile as BF
from dff_calc import dff_calc # from here: https://github.com/PBLab/dff-calc/blob/master/dff_calc/df_f_calculation.py

def main_tiffs(recording_dir, roi_fp, output_dir, func_channel=0, delete_rec=False):

    # pull all tifs in dir
    recording_fps = glob(recording_dir + '/*.tif')
    
    # loop through all recordings
    for recording_fp in recording_fps:
        print(recording_fp)
        
        # load recording (.tif)
        rec = imread(recording_fp)
        n_frames = rec.shape[0]
        print(rec.shape)

        # load ROIs
        rois = imread(roi_fp)
        n_rois = len(np.unique(rois))

        # for each ROI, pull out activity
        roi_activity = np.zeros((n_rois, n_frames))
        for roi in tqdm(range(n_rois)):
            # handle whether one or two channels were included
            if rec.ndim==4:
                roi_activity[roi] = np.mean(rec[:, func_channel, rois==roi], axis=1)
            elif rec.ndim==3:
                roi_activity[roi] = np.mean(rec[:, rois==roi], axis=1)
            else: 
                raise ValueError('recording has wrong number of dimensions')
            f0 = roi_activity[roi][0]
            roi_activity[roi] = roi_activity[roi] - f0
            roi_activity[roi] = roi_activity[roi] / f0

        # save
        output_fp = os.path.join(output_dir, 
            os.path.basename(recording_fp).replace('.tif', '_roi_activity.npy'))
        np.save(output_fp, roi_activity)

        # plot
        fig,ax = plt.subplots(figsize=(20,8))
        ax.plot(roi_activity.T + np.arange(n_rois), alpha=0.4);ax.set_xlabel('time');ax.set_ylabel('roi')
        plt.savefig(output_fp.replace('.npy', '.png'))

        # delete tif to make space
        if delete_rec:
            os.remove(recording_fp)

def main_bin(recording_fp, roi_fp, output_dir, func_channel=0, delete_rec=False):
    
    print(recording_fp)
    
    # load recording (.bin)
    rec = BF(512,512,recording_fp).data
    n_frames = rec.shape[0]
    print(rec.shape)

    # load ROIs
    rois = imread(roi_fp)
    n_rois = len(np.unique(rois))

    # for each ROI, pull out activity
    roi_activity = np.zeros((n_rois, n_frames))
    for roi in tqdm(range(n_rois)):
        # handle whether one or two channels were included
        if rec.ndim==4:
            roi_activity[roi] = np.mean(rec[:, func_channel, rois==roi], axis=1)
        elif rec.ndim==3:
            roi_activity[roi] = np.mean(rec[:, rois==roi], axis=1)
        else: 
            raise ValueError('recording has wrong number of dimensions')
        # f0 = roi_activity[roi][0]
        # roi_activity[roi] = roi_activity[roi] - f0
        # roi_activity[roi] = roi_activity[roi] / f0

    # compute df/f from f
    roi_activity = dff_calc(roi_activity)

    # save
    output_fp = os.path.join(output_dir, 
        os.path.basename(recording_fp).replace('.bin', '_roi_activity.npy'))
    np.save(output_fp, roi_activity)

    # plot
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(roi_activity.T + np.arange(n_rois), alpha=0.4);ax.set_xlabel('time');ax.set_ylabel('roi')
    plt.savefig(output_fp.replace('.npy', '.png'))

    # delete tif to make space
    if delete_rec:
        os.remove(recording_fp)

if __name__=='__main__':
    # recording_fp = sys.argv[1]
    # roi_fp = sys.argv[2]
    # output_fp = sys.argv[3]
    fly_dir = 'f2_f'
    data_path = '/usr/people/iwahle/501b_2p/data'
    recording_fp = os.path.join(data_path, f'raw/{fly_dir}/data.bin')
    roi_fp = os.path.join(data_path, f'raw/{fly_dir}/y.ome.tiff')
    output_dir = os.path.join(data_path, f'processed/{fly_dir}')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    plt.imshow(imread(roi_fp))
    plt.savefig('tmp.png')

    main_bin(recording_fp, roi_fp, output_dir, delete_rec=False)
    # main_tiffs(recording_dir, roi_fp, output_dir, delete_rec=False)