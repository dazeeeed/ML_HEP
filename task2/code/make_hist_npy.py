#!/usr/bin/env python3

import numpy as np
import sys, getopt
import time
import matplotlib.pyplot as plt

from custom_fnk import label_position, load_npy

    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'sb')
    except getopt.GetoptError:
        print('Error...')
        sys.exit(2)

    if len(opts) != 2:
        print(f'I need 2 arguments in format ./[program_name] -s <signal_file.npy> -b <background_file.npy>')
        sys.exit(1)

    for opt, arg in opts:
        if opt in '-s':
            signal_file = arg
        if opt in '-b':
            background_file = arg
        
    start = time.time()

    # plik z sygnalem
    signal, signal_labels = load_npy(signal_file)

    # plik z tlem
    background, background_labels = load_npy(background_file)

    print(f'Loaded in {time.time() - start:.2f}s')

    weights = signal[:, signal_labels.index('w')] * signal[:, signal_labels.index('matchHftWeight')]

    hist_1d(signal[:, signal_labels.index('m')], background[:, background_labels.index('m')], 'm', weights=weights)
    hist_1d(signal[:, signal_labels.index('pt')], background[:, background_labels.index('pt')], 'pt', weights=weights)
    hist_1d(signal[:, signal_labels.index('dca12')], background[:, background_labels.index('dca12')], 'dca12', weights=weights)
    hist_1d(signal[:, signal_labels.index('decayLength')], background[:, background_labels.index('decayLength')], 'decayLenght', weights=weights)
    hist_1d(signal[:, signal_labels.index('dcaV0ToPv')], background[:, background_labels.index('dcaV0ToPv')], 'dcaV0ToPv', weights=weights)
    hist_1d(signal[:, signal_labels.index('ptKaon')], background[:, background_labels.index('ptKaon')], 'ptKaon', weights=weights)
    hist_1d(signal[:, signal_labels.index('dcaKaon')], background[:, background_labels.index('dcaKaon')], 'dcaKaon', weights=weights)
    hist_1d(signal[:, signal_labels.index('ptPion')], background[:, background_labels.index('ptPion')], 'ptPion', weights=weights)
    hist_1d(signal[:, signal_labels.index('dcaPion')], background[:, background_labels.index('dcaPion')], 'dcaPion', weights=weights)

    print('Done!')
    

def hist_1d(signal, background, x_label, weights=None):
    plt.clf()

    bins = 400

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # signal hist
    ax1.hist(signal, bins=bins, weights=weights, histtype='step', color='blue')
    ax1.set_xlabel(x_label)
    ax1.set_ylabel('Signal', color='blue')

    # dodaje drugą oś Y, ale ma tą samą oś X
    ax2 = ax1.twinx() 

    # background hist
    ax2.hist(background, bins=bins, histtype='step', color='red')
    ax2.set_ylabel('Backgound', color='red')

    title = f'{x_label}_signal_vs_background_12'
    plt.title(title)

    # opis histogramu
    sgn_desc = f'Entries {format(signal.shape[0], ".2e")}\
         \nMean {np.mean(signal):.4f} \nStd dev {np.std(signal):.4f}'
    bckg_desc = f'Entries {format(background.shape[0], ".2e")}\
         \nMean {np.mean(background):.4f} \nStd dev {np.std(background):.4f}'
    hist_desc = f'Signal: {sgn_desc} \n\nBackground: {bckg_desc}'

    # zeby nic nie ucieło
    plt.tight_layout()

    # save file
    img_path = f'../img/hist1d/{title}'
    plt.savefig(img_path)
    #plt.show()

    
if __name__ == '__main__':
    main(sys.argv[1:])