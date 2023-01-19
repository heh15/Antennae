'''
This is to measure the velocity dispersion for different clusters using
data from 12CO 2-1 cubes. I am going to fit Gaussian to the spectrum of
each cluster in a certain velocity ranges. The aperture used to extract
the spectrum is imfit result for image with beam of 0.9 arcsec 
'''

import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

# extract the spectrum for each cluster. 

# for aperture from imfit to the image of 0.11 arcsec beam size
clustername = ['1a', '1b', '2', '5', '6', '7']
chans = [[33, 48], [36, 48], [29, 39], [14, 30], [9, 24], [40, 46]]
vel_disp = []
vel_disp_err = []

# for aperture from imfit to the image 0.134 arcsec beam size
chans = [[33, 48], [37, 48], [28, 40], [14, 33], [9, 25], [40, 48]]

# for sources that broken apart into multiple sources.
clustername_add = ['1bI', '1bII', '2a', '5a'] 
chans_add = [[37, 48], [37, 48], [30, 39], [18, 31]]

clustername = clustername + clustername_add
chans = chans + chans_add

# Display the spectrum for cluster 1.

for i in range(len(clustername)):
    if clustername[i] in clustername_add:
        filename = 'tables/cluster'+clustername[i]+'.tsv'
    else: 
#        filename = 'tables/cluster'+clustername[i]+'_robust2.tsv'
        filename = 'tables/cluster'+clustername[i]+'_p5.tsv'
    spectrum = pd.read_csv(filename, skiprows=7, sep='\t', header=None)
    
    # fit the spectrum at given range
    # cluster 1, 33 ~ 47
    x = spectrum[0][chans[i][0]:chans[i][1]]
    y = spectrum[1][chans[i][0]:chans[i][1]]
    
    
    n = len(x)                          #the number of data
    mean = sum(x*y)/sum(y)                   #note this correction
    sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))        #note this correction
    maximum = np.max(y)
    
    popt, pcov = curve_fit(gaus, x, y, p0=[maximum, mean, sigma])
    vel_disp.append(np.abs(popt[2]))
    perr = np.sqrt(np.diag(pcov))
    vel_disp_err.append(perr[2])
    
    fig = plt.figure()
    plt.title('cluster '+ clustername[i], fontsize=20)
    plt.plot(spectrum[0], spectrum[1])
    plt.plot(spectrum[0], gaus(spectrum[0], *popt))
    plt.savefig('pictures/spectrum_'+clustername[i]+'_p5.png')
    
    # output the fitted velocity
    spectrum[2] = gaus(spectrum[0], *popt)
    filename = 'tables/cluster'+clustername[i]+'_p5_fit.csv'
    spectrum.to_csv(filename, index = False, header=False)
    
    