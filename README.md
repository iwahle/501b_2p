# 501b_2p

## how to install `suite2p`
Follow steps 1-7 here: https://suite2p.readthedocs.io/en/latest/installation.html.
If you are doing processing on the server and using the GUI to visualize results
locally, you need to do this on both machines.

## run suite2p processing from command line (I would do this on the server)
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
  
## visualize suite2p processing results in GUI
- if you were running suite2p on the server, copy the results onto your local machine, e.g.:
  `scp -r iwahle@scotty.pni.princeton.edu:/usr/people/iwahle/501b_2p/data/processed/example /Users/imanwahle/Downloads`
- start up the suite2p GUI by running in a local terminal: `conda activate suite2p` and then `suite2p`
- In the GUI, navigate to `File > Load processed data` and then select the `stat.npy`
  file in the directory you just copied over from the server, i.e. 
  `/Users/imanwahle/Downloads/example/plane0/stat.npy`
