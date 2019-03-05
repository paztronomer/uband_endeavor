""" Simple script to assess variability of PCA solution for 
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def pc_comp1(regx):
    # Get filenames
    l1 = glob.glob(regx)
    l1 = sorted(l1)
    # Define plot
    fig, axis = plt.subplots(4, 1)
    for idx, ax in enumerate(axis):
        for fnm in l1[:2]:
            hdu = fits.open(fnm)
            x0 = np.copy(hdu[0].data)
            x1 = np.copy(hdu[1].data) 
            hdu.close()
            #
            print(x0.shape)
            row = np.arange(x0.shape[0])
            ax.plot(row, x0[:,idx], '.')
            
    plt.show()

def pc_comp2(fnm1, fnm2):
    x0 = np.copy(fits.open(fnm1)[0].data)
    y0 = np.copy(fits.open(fnm2)[0].data)

    fig, axis = plt.subplots(4, 1, figsize=(8, 4), sharex=True)
    for i, ax in enumerate(axis):
        kw = {
            'ls': '-',
            'lw': 0.3,
        }
        ax.plot(x0[:, i], color='navy', **kw)
        ax.plot(y0[:, i], color='gold', **kw)
        ax.text(0.1, 0.7, 'PC{0}'.format(i + 1), transform=ax.transAxes)
        ax.set_ylabel('PC value')
    axis[-1].set_xlabel('row')

    plt.suptitle('[u-band] Per-component comparison between healthy/bad PCA',
                 color='g')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.98, top=0.9, hspace=0.1)
   
    plt.savefig('pc_comparison.png', dpi=300, format='png')

    plt.show()
    exit()

if __name__ == '__main__':
    
    pc_comp2('pca_sel2/pca_Y2N+14_onlyStack_sel2_u_0p008_n04.fits',
             'pca_sel2/pca_Y2N+14_sel2_u_0p008_n04.fits')
    pc_comp1('pca_sel2/pca_Y2N+14_onlyStack*')
