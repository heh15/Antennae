import numpy as np
import os,glob
import scipy.ndimage as sni
import sys
import re
import itertools
from shutil import copytree
from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import make_lupton_rgb
# import aplpy
from astropy.nddata import Cutout2D
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.visualization.wcsaxes import SphericalCircle
from matplotlib.patches import Arrow
from photutils import SkyCircularAnnulus
from photutils import SkyCircularAperture
from photutils import CircularAperture
from photutils import CircularAnnulus
from photutils import SkyEllipticalAperture
from photutils import SkyEllipticalAnnulus
from photutils import EllipticalAperture
from photutils import EllipticalAnnulus
from photutils import aperture_photometry
import numpy.ma as ma
import math
import shutil
import pandas as pd
from reproject import reproject_interp

###########################################################
# directories and files

Dir = '/home/heh15/research/Antennae/' 
imageDir = Dir + '2016/Band3/'
scriptDir = Dir + 'scripts/'

mapDir = Dir + 'images/'

############################################################
# basic settings

highfreq = 345
lowfreq = 100 

###########################################################
# function 

def fits_import(fitsimage, item=0):
    hdr = fits.open(fitsimage)[item].header
    wcs = WCS(hdr).celestial
    data=fits.open(fitsimage)[item].data
    data=np.squeeze(data)
    data_masked=np.ma.masked_invalid(data)

    return wcs, data_masked

def reproj_binning2(data, wcs_in, bin_num, centerCoord = '', shape_out=''):
    '''
    centerCoord is the array of central coordinates in degree. 
    '''
    map_in_shape=np.shape(data)
    nx_in, ny_in=map_in_shape
    nx_out = math.trunc(nx_in/bin_num); ny_out=math.trunc(ny_in/bin_num)
    if shape_out == '':
        shape_out = (nx_out, ny_out)
    if centerCoord == '':
        centerCoord = wcs_in.wcs.crval
    wcs_out = WCS(naxis = 2)
    wcs_out.wcs.crval = centerCoord
    wcs_out.wcs.crpix =[math.trunc(shape_out[1]/2), math.trunc(shape_out[0]/2)]
    wcs_out.wcs.cdelt=wcs_in.wcs.cdelt*bin_num
    wcs_out.wcs.ctype = ['RA---SIN', 'DEC--SIN']
    data_binned, footprint = reproject_interp((data, wcs_in), wcs_out, shape_out=shape_out)


    return wcs_out, data_binned


###########################################################
# main program

# import the image for band 3
fitsimage = imageDir + 'ngc40389overlap_band3_uvrange_robust_2_smooth_pbcor.fits' 
wcs_band3, data_band3 = fits_import(fitsimage)

# import the image for band 7
fitsimage = imageDir + 'ngc40389overlap_band7_range_robust_2_smooth_pbcor.fits'
wcs_band7, data_band7 = fits_import(fitsimage)

# reproject the  band 3 image to band 7 image. 
data_band3_rproj = reproject_interp((data_band3, wcs_band3), 
                wcs_band7, shape_out = np.shape(data_band7.data))[0]

# split the out the dust emission in band 7
data_band7_ff = data_band3_rproj * (highfreq/lowfreq)**(-0.1)
data_band7_dust = data_band7 - data_band7_ff

# export the dust emission data in 

outputfits = mapDir + 'ngc40389_band7_dust.fits'
header = wcs_band7.to_header()
hdu = fits.PrimaryHDU(data_band7_dust.data, header)
hdu.writeto(outputfits, overwrite=True)


# fig = plt.figure()
# plt.imshow(data_band7_dust, origin='lower')
# plt.show()
