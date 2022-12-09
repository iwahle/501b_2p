import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from tqdm import tqdm

def main(recording_fp, roi_fp, output_fp, func_channel=0):

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
        roi_activity[roi] = np.mean(rec[:, func_channel, rois==roi], axis=1)
        f0 = roi_activity[roi][0]
        roi_activity[roi] = roi_activity[roi] - f0
        roi_activity[roi] = roi_activity[roi] / f0

    # save
    np.save(output_fp, roi_activity)

    # plot
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(roi_activity.T + np.arange(n_rois), alpha=0.4);ax.set_xlabel('time');ax.set_ylabel('roi')
    # ax[1].imshow(roi_activity);ax[1].set_xlabel('time');ax[1].set_ylabel('roi')
    plt.savefig(output_fp.replace('.npy', '.png'))

if __name__=='__main__':
    # recording_fp = sys.argv[1]
    # roi_fp = sys.argv[2]
    # output_fp = sys.argv[3]
    recording_fp = '/usr/people/iwahle/501b_2p/data/raw/f5_f/natural_250_00001_00001.tif'
    roi_fp = '/usr/people/iwahle/501b_2p/data/processed/f5_f/natural_250_00001_00001_ROIs.tiff'
    output_fp = '/usr/people/iwahle/501b_2p/data/processed/f5_f/natural_250_00001_00001_roi_activity.npy'
    plt.imshow(imread(roi_fp))
    plt.savefig('tmp.png')

    main(recording_fp, roi_fp, output_fp)