from astropy import units as u
import time
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
from regions import read_ds9
from photutils import SkyEllipticalAperture
from photutils import EllipticalAperture
from photutils import SkyRectangularAperture
import matplotlib.colors as colors
from photutils import SkyCircularAperture
from matplotlib import rcParams
rcParams['mathtext.default']='regular'
from reproject import reproject_interp
import matplotlib.image as mpimg
import pandas as pd


##################################################
# directories and files

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'region/'
logDir = Dir+'logs/'

##################################################
# basic settings

regions = ['a', 'b', 'c']
resolutions = ['SC', 'GMC']
rms = {}
rms['SC'] = 4.1e-5
rms['GMC'] = 5.3e-5

vmin = {}
vmin['SC'] = 2.8e-5
vmin['GMC'] = 2.4e-5

vmax = {}
vmax['SC'] = 1.4e-4
vmax['GMC'] = 1.2e-4
 
##################################################
# functions

def fits_import(fitsimage, item=0):
    hdr = fits.open(fitsimage)[item].header
    wcs = WCS(hdr).celestial
    data=fits.open(fitsimage)[item].data
    data=np.squeeze(data)
    data_masked=np.ma.masked_invalid(data)

    return wcs, data_masked

def cut_2d(data,position,size,wcs):
    cut=Cutout2D(data=data,position=position,size=size,wcs=wcs)
    data_cut=cut.data
    wcs_cut=cut.wcs

    return wcs_cut, data_cut

##################################################
# main program

for region in regions:
    for resolution in resolutions:
        filename = imageDir+region+'_band3_'+resolution+'_zoom.fits'
        wcs, band3_data = fits_import(filename)

       # plot the image
        fig = plt.figure()
        ax = plt.subplot(111, projection=wcs)
        ax.imshow(band3_data, origin='lower', vmin = vmin[resolution], vmax=vmax[resolution])
        levels = rms[resolution]*np.array([7.5, 10, 12.5, 15])

        if resolution == 'SC':
            filename = imageDir+region+'_band7_'+resolution+'_zoom.fits'
        if resolution == 'GMC':
            filename = imageDir+region+'_band6_'+resolution+'_zoom.fits'
        
#        if (resolution == 'SC') and (region == 'b'):
#            plt.savefig(picDir+region+'_band3_contour_'+resolution+'.png')
#            continue
        wcs_contour, contour = fits_import(filename)
        contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs, 
                                         shape_out=np.shape(band3_data.data)) 
 
        ax.contour(contour_proj.data, colors = 'red', levels=levels, linewidths=0.6)
        plt.savefig(picDir+region+'_band3_contour_'+resolution+'.png')
