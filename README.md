# 501b_2p

## use this repo
- would recommend using this on the server
- `git clone https://github.com/iwahle/501b_2p.git`


## use DeepCell Label to segment images
1. compute the mean of a recording over time:
    ```
    from skimage.io import imread
    from tiffile import imwrite
    data = imread('path/to/movie.tif') # should be np array of size (time x channels x 512 x 512)
    avg = np.mean(data[:,0,:,:],axis=0) # you can change channel if you want
    imwrite('path/to/save.tif', avg)
2. annotate image 
  - go here: https://deepcell.org/
  - go to predict
  - upload the averaged tif file with settings: Segmentation, 40x, XY
  - click view results
  - pull the max color ranges down to see the image better it will have generated some ROIs but they will probably not fit well, delete if you want under the cell tab
  - use the GUI to annotate as you'd like: hit 'b' to enter brush mode, then 
    hit 'n' every time you start drawing out a new cell
  - click download
  - unzip the downloaded file. inside there should be a file called y.ome.tiff that includes the labeled ROIs
3. generate df/f traces
  - call `python src/get_roi_activity path/to/original/recording path/to/y.ome.tiff path/to/save.npy`
  - if things have not exploded by this point, this will save an .npy file where you tell it to with a n_rois x n_timeframes matrix of df/f traces

    











## old instructions on suite2p stuff

### how to install `suite2p`
Follow steps 1-7 here: https://suite2p.readthedocs.io/en/latest/installation.html.
If you are doing processing on the server and using the GUI to visualize results
locally, you need to do this on both machines.

After you enter your suite2p conda environment, you will also need to install
this specific version of cellpose manually: `pip install cellpose==0.6.5`.

### run suite2p processing from command line (I would do this on the server)
- download `.tif` files into a subdirectory of `data/raw` (this can be done with
  `gdown`. First `pip install gdown`, then 
  `gdown https://drive.google.com/uc?id=<file_id>` for a file or 
  `gdown --folder https://drive.google.com/drive/folders/<file_id>` for a whole directory.)
- `src/suite2p_pipeline.py` will set up the processing parameters, load in any
  `.tif` files in the specified directory, and run the suite2p processing pipeline.
  Settings and directory path can be modified in the script.
- to run the script: `python src/suite2p_pipeline.py`
- if files were in directory `data/raw/example`, this script will save processing
  results to `data/processed/example`
  
### visualize suite2p processing results in GUI
- if you were running suite2p on the server, copy the results onto your local machine, e.g.:
  `scp -r iwahle@scotty.pni.princeton.edu:/usr/people/iwahle/501b_2p/data/processed/example /Users/imanwahle/Downloads`
- start up the suite2p GUI by running in a local terminal: `conda activate suite2p` and then `suite2p`
- In the GUI, navigate to `File > Load processed data` and then select the `stat.npy`
  file in the directory you just copied over from the server, i.e. 
  `/Users/imanwahle/Downloads/example/plane0/stat.npy`
