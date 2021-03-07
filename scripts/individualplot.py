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

# # zoom in subregions of the Antennae galaxy
# for region in regions:
#     for resolution in resolutions:
#         filename = imageDir+region+'_band3_'+resolution+'_zoom.fits'
#         wcs, band3_data = fits_import(filename)
# 
#        # plot the image
#         fig = plt.figure()
#         ax = plt.subplot(111, projection=wcs)
#         ax.imshow(band3_data, origin='lower', vmin = vmin[resolution], vmax=vmax[resolution])
#         levels = rms[resolution]*np.array([7.5, 10, 12.5, 15])
# 
#         if resolution == 'SC':
#             filename = imageDir+region+'_band7_'+resolution+'_zoom.fits'
#         if resolution == 'GMC':
#             filename = imageDir+region+'_band6_'+resolution+'_zoom.fits'
#         
# #        if (resolution == 'SC') and (region == 'b'):
# #            plt.savefig(picDir+region+'_band3_contour_'+resolution+'.png')
# #            continue
#         wcs_contour, contour = fits_import(filename)
#         contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs, 
#                                          shape_out=np.shape(band3_data.data)) 
#  
#         ax.contour(contour_proj.data, colors = 'red', levels=levels, linewidths=0.6)
#         plt.savefig(picDir+region+'_band3_contour_'+resolution+'.png')


# Draw image for individual clusters
clusters = ['1a', '1b', '2', '5', '6', '7', '9']
datatypes = ['_SC', '_SC_p5', '_SC_p5_009']
band7_types = ['_SC', '_SC_p5']
rms_band7 = 4.1e-5
pbcor = [0.65, 0.65, 0.8, 0.9, 0.95,  0.85, 0.4]
colheaders = ['robust 2.0, 0.13 arcsec', 'robust 0.5, 0.11 arcsec', 'robust 0.5, 0.09 arcsec']

# import apertures
regionfile = regionDir + 'source_band3_2016_imfit.reg'
regions_sky = read_ds9(regionfile)
regions_sky.pop(3); regions_sky.pop(3)
# import source 6
regionfile = regionDir + 'source_band7_2016_imfit.reg'
region6_sky = read_ds9(regionfile)[0]
regions_sky.insert(4, region6_sky) 

# import apertures for robust 0.5 image
regionfile = regionDir + 'source_band3_2016_p5_imfit_v2.reg'
regionsp5_sky = read_ds9(regionfile)
regionsp5_sky.pop(3); regionsp5_sky.pop(3)
# import source 6
regionfile = regionDir + 'source_band7_2016_imfit_p5.reg'
regionp5_6_sky = read_ds9(regionfile)[0]
regionsp5_sky.insert(4, regionp5_6_sky)

# import apertures for subregions 
regionfile = regionDir + 'source_band3_multiple_imfit.reg'
regionsSub_temp = read_ds9(regionfile)
regionsSub_temp.pop(3); regionsSub_temp.pop(3)
regionsSub_sky = {}
regionsSub_sky[1] = regionsSub_temp[0:2]
regionsSub_sky[2] = regionsSub_temp[2:3]
regionsSub_sky[3] = regionsSub_temp[3:4]
regionsSub_sky[6] = regionsSub_temp[4:]

# remove the cluster 9 since the S/N is low
clusters.pop(-1) 

fig = plt.figure(figsize=(9, 12), constrained_layout=False)
gc = gridspec.GridSpec(ncols=2, nrows=1, figure=fig, width_ratios=[6,3])

# sub gridspec
gc1 = gridspec.GridSpecFromSubplotSpec(ncols=3, nrows=6, subplot_spec=gc[0],
                                       hspace=0.05, wspace=0.05) 
# gc1.update(hspace=0.1, wspace=0.1)

axes = {}
for n, data in enumerate(datatypes):
    axes[n] = {}
    for m, cluster in enumerate(clusters):
        filename = imageDir+cluster+'_band3'+data+'.fits'
        wcs, band3_data = fits_import(filename)
        
       # plot the image
        axes[n][m] = fig.add_subplot(gc1[m, n], 
                                     projection=wcs)
        lon = axes[n][m].coords[0]
        lat = axes[n][m].coords[1]
        axes[n][m].tick_params(labelsize=3, direction='in')
        lon.set_axislabel('J2000 R.A.', fontsize=5)
        lat.set_axislabel('J2000 Dec.', fontsize=5)
        if m != 5:
            lon.set_axislabel(' ')
        if n in [1, 2]:
            lat.set_ticks_visible(False)
            lat.set_ticklabel_visible(False)
        axes[n][m].imshow(band3_data, origin='lower', vmin = 2.8e-5, vmax=1.4e-4)
        axes[n][m].set_aspect('equal')
        
        # overlay contours
        levels = rms_band7 / pbcor[m] * np.array([3, 5, 10, 15])
        if data in band7_types:
            filename = imageDir+cluster+'_band7'+data+'.fits'
            wcs_contour, contour = fits_import(filename)
            contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs,
                                         shape_out=np.shape(band3_data.data))
            axes[n][m].contour(contour_proj.data, colors = 'orange', levels=levels, linewidths=1)

        # overlay apertures
        if n ==0:
            region_pix = regions_sky[m].to_pixel(wcs)
            region_pix.plot(color='magenta', linewidth=1.5)
        if n ==1:
            region_pix = regionsp5_sky[m].to_pixel(wcs)
            region_pix.plot(color='magenta', linewidth=1.5)
        if n == 2:
            if m in regionsSub_sky.keys():
                for region_sky in regionsSub_sky[m]:
                    region_pix = region_sky.to_pixel(wcs)
                    region_pix.plot(color='magenta', linewidth=1.5)
        
        # annotate name of each cluster
        anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
                 va='center', ha='center', color='white', fontsize=10) 
        axes[n][m].annotate(clusters[m], **anno_opts)
        # annotate sub apertures in the third column
        
   # add the title for each column
    axes_lists = list(dict.values(axes[n]))
    axes_lists[0].set_title(colheaders[n], fontsize=8)

# plot the spectrums for clusters. 
axes[3] = {}
gc2 = gridspec.GridSpecFromSubplotSpec(ncols=1, nrows=6, subplot_spec=gc[1], 
                                       hspace=0.15)
for m, cluster in enumerate(clusters):
    spectrum = pd.read_csv(logDir+'cluster'+cluster+'_fit.csv', header=None)
    axes[3][m] = fig.add_subplot(gc2[m, 0])
    axes[3][m].plot(spectrum[0], spectrum[1], color='blue')
    axes[3][m].plot(spectrum[0], spectrum[2], color='orange')
    axes[3][m].tick_params(labelsize=7, direction='in')
    axes[3][m].set_ylabel('Intensity (Jy/beam)', fontsize=8)

    # annotate name of each cluster
    anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
             va='center', ha='center', color='white', fontsize=10)
    axes[3][m].annotate(clusters[m], **anno_opts)
 
# set the xlabel for the spectrums 
axes[3][m].set_xlabel('Velocity (km/s)', fontsize=8)
# set the title
axes[3][0].set_title('CO spectrum', fontsize=8)

fig.tight_layout()
plt.savefig(picDir+'cluster_summary.png')
plt.savefig(picDir+'cluster_summary.pdf', bbox_inches='tight', pad_inches=1.2)
