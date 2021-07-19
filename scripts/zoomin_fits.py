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
from regions import read_ds9
import copy
import sys
from matplotlib.colors import LogNorm

##########################################################
# folders

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'regions/'
logDir = Dir+'logs/'

GMC_dir = Dir+'2018/'
SC_dir = Dir + '2016/'

cont_Band3_GMC = Dir + '2018/cont_100GHz/image/'\
                       'ngc4038_band3_cont_12m_7m.fits'
cont_Band3_SC = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_2_smooth.fits'
cont_Band3_SC_p5 = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_p5_smooth_pbcor.fits'
cont_Band3_SC_p5_009 = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_p5_smooth_090_pbcor.fits'
cont_Band6_GMC = Dir + '2018/cont_200GHz/image/'\
                       'ngc4038_band6_cont_12m_7m.fits'
cont_Band7_SC = Dir + '2016/Band7/ngc40389overlap_band7_range_robust_2_smooth.fits'
cont_Band7_SC_p5 = Dir + '2016/Band3/ngc40389overlap_band7_range_robust_p5_smooth_pbcor.fits'

###########################################################
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

def import_coords(regionfile, ra_add = 0*u.arcsec, dec_add = 0*u.arcsec):
    regions = read_ds9(regionfile)
    coords = []
    for region in regions:
        coord = region.center
        coord = SkyCoord(ra=coord.ra+ra_add, dec=coord.dec+dec_add, frame='icrs')
        coords.append(coord)

    return coords

###########################################################
# basic settings

# data types for different images
datatypes = ['band3_GMC', 'band3_SC','band3_SC_p5',  'band6_GMC', 'band7_SC']
parameters = ['imagename']
continuum = dict.fromkeys(datatypes)
for key in continuum.keys():
    continuum[key] = {}


# band 3 GMC images
continuum['band3_GMC']['imagename'] = cont_Band3_GMC

# band 3 SC images
continuum['band3_SC']['imagename'] = cont_Band3_SC

# band 6 GMC images
continuum['band6_GMC']['imagename'] = cont_Band6_GMC

# band 7 SC images
continuum['band7_SC']['imagename'] = cont_Band7_SC

# band 3 SC p5
# # continuum image for Band 3 SC data with robust of 0.5 (0.11 arcsec)
continuum['band3_SC_p5'] = copy.deepcopy(continuum['band3_SC'])
continuum['band3_SC_p5']['imagename'] = cont_Band3_SC_p5

# # continuum image for Band 3 SC data, robust 0.5, beam 0.09 arcsec
continuum['band3_SC_p5_009'] = copy.deepcopy(continuum['band3_SC'])
continuum['band3_SC_p5_009']['imagename'] = cont_Band3_SC_p5_009

# band 7 SC p5
continuum['band7_SC_p5'] = copy.deepcopy(continuum['band7_SC'])
continuum['band7_SC_p5']['imagename'] = cont_Band7_SC_p5

# band 3 SC p5 009

# import individual clusters to zoom in 
sys.path.append('configs')
from zoomin_fits_cluster import apers
clusters = copy.deepcopy(apers)

# import individual GMCs to zoom in 
region_labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
features = ['position', 'size', 'aperture']
GMCs = dict.fromkeys(region_labels)
for key in GMCs.keys():
    GMCs[key] = dict.fromkeys(features)

positions = import_coords(regionDir+'source_band3_imfit.reg')
for i, position in enumerate(positions):
    GMCs[region_labels[i]]['position'] = position
    GMCs[region_labels[i]]['size'] = u.Quantity(((0.06, 0.06)), u.arcmin)    

###########################################################
# main program

# # export fitsfile for each cluster
# datatypes = ['band3_SC', 'band3_SC_p5', 'band3_SC_p5_009','band7_SC', 'band7_SC_p5']
# for data in datatypes:
#     fitsimage = continuum[data]['imagename']
#     wcs, cont_image = fits_import(fitsimage)
#     # cut the image out
#     for key in clusters.keys():
#         region_wcs, region_data = cut_2d(cont_image.data, clusters[key]['position'], 
#                                          clusters[key]['size'], wcs)
#         outputfits = imageDir + key + '_' + data + '.fits'
#         header = region_wcs.to_header()
#         hdu = fits.PrimaryHDU(region_data.data, header)   
#         hdu.writeto(outputfits, overwrite=True)

# export fitsfile for GMC data
datatypes = ['band3_GMC', 'band6_GMC']
for data in datatypes:
    fitsimage = continuum[data]['imagename']
    wcs, cont_image = fits_import(fitsimage)
    # cut the image out
    for key in GMCs.keys():
        region_wcs, region_data = cut_2d(cont_image.data, GMCs[key]['position'],
                                         GMCs[key]['size'], wcs)
        outputfits = imageDir + key + '_' + data + '.fits'
        header = region_wcs.to_header()
        hdu = fits.PrimaryHDU(region_data.data, header)
        hdu.writeto(outputfits, overwrite=True)  

 
