# standard python packages
import os, warnings
import glob
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import ruamel.yaml as yaml
import sys

# cascade2p packages, imported from the downloaded Github repository
sys.path.append('/usr/people/iwahle/Cascade')
from cascade2p import checks
checks.check_packages()
from cascade2p import cascade # local folder
from cascade2p.utils import plot_dFF_traces, plot_noise_level_distribution, plot_noise_matched_ground_truth


def main(dff_fp, output_dir, model_name='Global_EXC_30Hz_smoothing25ms', 
    model_folder='/usr/people/iwahle/Cascade/Pretrained_models'):

    # load df/f traces
    traces = np.load('/usr/people/iwahle/501b_2p/data/processed/f4_f/data_roi_activity.npy')

    # download model
    model_name = 'Global_EXC_30Hz_smoothing25ms'
    cascade.download_model(model_name, verbose=1, model_folder=model_folder)

    # predict
    spike_prob = cascade.predict( model_name, traces, verbosity=1, model_folder=model_folder)
    np.save(os.path.join(output_dir, 'spike_prob.npy'), spike_prob)

    # plot examples
    nb_neurons = 16
    neuron_indices = np.random.randint(traces.shape[0], size=nb_neurons)
    time_axis = plot_dFF_traces(traces,neuron_indices,30,spike_prob,y_range=(-1.5, 3))
    plt.savefig(os.path.join(output_dir, 'spike_prob_examples.png'))

    # plot all spike probs
    n_rois = traces.shape[0]
    assert traces.shape[0]==spike_prob.shape[0]
    fig,ax = plt.subplots(figsize=(20,8))
    ax.plot(spike_prob.T + np.arange(n_rois), alpha=0.4);ax.set_xlabel('time');ax.set_ylabel('roi')
    plt.savefig(os.path.join(output_dir, 'spike_prob_all.png'))

if __name__=='__main__':
    # dff_fp = sys.argv[1]
    # output_dir = sys.argv[2]
    dff_fp = '/usr/people/iwahle/501b_2p/data/processed/f4_f/data_roi_activity.npy'
    output_dir = '/usr/people/iwahle/501b_2p/data/processed/f4_f'
    main(dff_fp, output_dir)