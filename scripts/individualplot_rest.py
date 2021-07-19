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
import matplotlib.gridspec as gridspec
from regions import read_ds9
import sys

##################################################
# directories and files

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'regions/'
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

#############################
# import data

# Draw image for individual clusters
clusters = ['3','4','8','9','10','11','12','13']
clusters_resolved = ['3','4','9'] 
clusters_unresolved = [x for x in clusters if x not in clusters_resolved]
datatypes = ['_GMC', '_SC_p5']
# datatypes = ['_SC_p5']

## information for band 6 and band 7 contours
band6_types = ['_GMC']
band6_rms = 5.3e-5 
band7_types = ['_SC_p5']
band7_rms = 4.1e-5
contour_types = band6_types + band7_types

colheaders = ['GMC resolution', 'YMC resolution (0.11")', 'YMC resolution (0.09")']
# colheaders = ['robust 0.5, 0.11 arcsec']

##############
# import the zoomin apertures for GMC images
sys.path.append('configs')
from zoomin_fits_cluster import apers 

##############
# import apertures to measure the flux

##  import apertures for GMC measurements
regionfile = regionDir + 'source_band3_imfit.reg'
regions_sky = read_ds9(regionfile)
indices_resolved = [2,3,8]
regionsGMC_sky = [regions_sky[i] for i in indices_resolved]
regionsGMC_sky = {v: [k] for v, k in enumerate(regionsGMC_sky)}

indices_rest = [7,9,10,11,12]
regionsGMC2_sky= [regions_sky[i] for i in indices_rest]
regionsGMC2_sky = {v: [k] for v, k in enumerate(regionsGMC2_sky)}

## import apertures for robust 0.5 image
regionfile = regionDir + 'source_band3_2016_p5_imfit_v2.reg'
regionsp5_sky = read_ds9(regionfile)
indices = [3,4,7]
regionsp5_sky = [regionsp5_sky[i] for i in indices]
regionsp5_sky = {v: [k] for v, k in enumerate(regionsp5_sky)}
#############################
# draw figures

fig = plt.figure(figsize=(12, 7.5), constrained_layout=False)
gc = gridspec.GridSpec(ncols=1, nrows=2, figure=fig, height_ratios=[5,2.5],hspace=0.15)

# sub gridspec
gc1 = gridspec.GridSpecFromSubplotSpec(ncols=2, nrows=2, subplot_spec=gc[0],
                                       hspace=0.1, wspace=0.1) 
# gc1.update(hspace=0.1, wspace=0.1)

# import the image
for i, cluster in enumerate(clusters_resolved):
    gc1_sub = gridspec.GridSpecFromSubplotSpec(ncols=2, nrows=1, subplot_spec=gc1[i], 
                                               wspace=0)
    axes = {}

    ##### plot the GMC resolution data #####
    filename = imageDir+cluster+'_band3'+'_GMC'+'.fits'
    wcs, band3_data = fits_import(filename)
    axes[0] = fig.add_subplot(gc1_sub[0,0], projection=wcs)
    axes[0].imshow(band3_data, origin='lower', vmin=2.8e-5, vmax=1.4e-4)

    # overlay contours
    filename = imageDir+cluster+'_band6'+'_GMC'+'.fits'
    levels = band6_rms * np.array([3, 5, 10, 15])
    wcs_contour, contour = fits_import(filename)
    contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs,
                                 shape_out=np.shape(band3_data.data))
    axes[0].contour(contour_proj.data, colors = 'orange', levels=levels, linewidths=1)

    # overlay GMC apertures
    region_pix = regionsGMC_sky[i][0].to_pixel(wcs)
    region_pix.plot(color='magenta', linewidth=1.5)
    # overlay YMC apertures
    region_pix = regionsp5_sky[i][0].to_pixel(wcs)
    region_pix.plot(color='red', linewidth=1.5)

    # set the xlabel and ylabel 
    lon = axes[0].coords[0]
    lat = axes[0].coords[1]
    axes[0].tick_params(labelsize=3, direction='in')
    lon.set_axislabel('J2000 R.A.', fontsize=10)
    lat.set_axislabel('J2000 Dec.', fontsize=10)

    # annotate the source ID of each cluster
    anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
             va='center', ha='center', color='white', fontsize=20) 
    axes[0].annotate(cluster, **anno_opts)


    ##### plot the star cluster resolution data #####
    filename = imageDir+cluster+'_band3'+'_SC_p5'+'.fits'
    wcs, band3_data = fits_import(filename)
    axes[1] = fig.add_subplot(gc1_sub[0,1], projection=wcs)
    axes[1].imshow(band3_data, origin='lower', vmin=2.8e-5, vmax=1.4e-4)

    # overlay contours
    filename = imageDir+cluster+'_band7'+'_SC_p5'+'.fits'
    levels = band7_rms * np.array([3, 5, 10, 15])
    wcs_contour, contour = fits_import(filename)
    contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs,
                                 shape_out=np.shape(band3_data.data))
    axes[1].contour(contour_proj.data, colors = 'orange', levels=levels, linewidths=1)

    lon = axes[1].coords[0]
    lat = axes[1].coords[1]
    axes[1].tick_params(labelsize=3, direction='in')
    lon.set_axislabel('J2000 R.A.')
    lat.set_axislabel(' ', fontsize=10)

    if i == 0:
        axes[0].coords[0].set_axislabel(' ')
        axes[1].coords[0].set_axislabel(' ')
        # set title
        axes[0].set_title('GMC resolution', fontsize=12)
        axes[1].set_title('YMC resolution (0.11")', fontsize=12)
    if i == 1:
        axes[0].coords[1].set_axislabel(' ')
        axes[0].set_title('GMC resolution', fontsize=12)
        axes[1].set_title('YMC resolution (0.11")', fontsize=12)

    # overlay YMC apertures
    region_pix = regionsp5_sky[i][0].to_pixel(wcs)
    region_pix.plot(color='red', linewidth=1.5)
    
    # annotate each cluster name
    anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
             va='center', ha='center', color='white', fontsize=20)
    axes[1].annotate(cluster, **anno_opts)

gc2 = gridspec.GridSpecFromSubplotSpec(ncols=5, nrows=1, subplot_spec=gc[1],
                                       hspace=0.1, wspace=0.18)
for i, cluster in enumerate(clusters_unresolved):
    filename = imageDir+cluster+'_band3'+'_GMC'+'.fits'
    wcs, band3_data = fits_import(filename)
    ax = fig.add_subplot(gc2[i], projection=wcs)
    ax.imshow(band3_data, origin='lower', vmin=2.8e-5, vmax=1.4e-4)

    # overlay contours
    filename = imageDir+cluster+'_band6'+'_GMC'+'.fits'
    levels = band6_rms * np.array([3, 5, 10, 15])
    wcs_contour, contour = fits_import(filename)
    contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs,
                                 shape_out=np.shape(band3_data.data))
    ax.contour(contour_proj.data, colors = 'orange', levels=levels, linewidths=1)

    # overlay GMC apertures
    region_pix = regionsGMC2_sky[i][0].to_pixel(wcs)
    region_pix.plot(color='magenta', linewidth=1.5)

    # set the xlabel and ylabel 
    lon = ax.coords[0]
    lat = ax.coords[1]
    ax.tick_params(labelsize=3, direction='in')
    lon.set_axislabel('J2000 R.A.', fontsize=10)
    if i == 0:
        lat.set_axislabel('J2000 Dec.', fontsize=10)
    else:
        lat.set_axislabel(' ')

    # annotate the source ID of each cluster
    anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
             va='center', ha='center', color='white', fontsize=20)
    ax.annotate(cluster, **anno_opts)
# plt.show()
# fig.tight_layout()
plt.savefig(picDir+'cluster_summary_rest.pdf', bbox_inches='tight', pad_inches=0.4)


