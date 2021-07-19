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

#############################
# import data

# Draw image for individual clusters
clusters = ['1a', '1b', '2', '5', '6', '7']
datatypes = ['_GMC', '_SC_p5', '_SC_p5_009']
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
indices = [0,1,4,5,6]
regionsGMC_sky = [regions_sky[i] for i in indices]
regionsGMC_sky.insert(0, regionsGMC_sky[0])
regionsGMC_sky = {v: [k] for v, k in enumerate(regionsGMC_sky)}

## import apertures for robust 0.5 image
regionfile = regionDir + 'source_band3_2016_p5_imfit_v2.reg'
regionsp5_sky = read_ds9(regionfile)
regionsp5_sky.pop(3); regionsp5_sky.pop(3)
# import source 6
regionfile = regionDir + 'source_band7_2016_imfit_p5.reg'
regionp5_6_sky = read_ds9(regionfile)[0]
regionsp5_sky.insert(4, regionp5_6_sky)
regionsp5_sky = {v: [k] for v, k in enumerate(regionsp5_sky)}

##  import apertures for subregions 
regionfile = regionDir + 'source_band3_multiple_imfit.reg'
regionsSub_temp = read_ds9(regionfile)
regionfile = regionDir + 'source_band3_1b_doublefit.reg'
regions1b = read_ds9(regionfile) 

regionsSub_temp.pop(3); regionsSub_temp.pop(3)
regionsSub_sky = {}
regionsSub_sky[1] = regions1b
regionsSub_sky[2] = regionsSub_temp[2:3]
regionsSub_sky[3] = regionsSub_temp[3:4]
regionsSub_sky[6] = regionsSub_temp[4:]

# put all 3 region dictionaries into a list
regionsSky = [regionsGMC_sky, regionsp5_sky, regionsSub_sky]
# regionsSky = [regionsp5_sky]

#############################
# draw figures

fig = plt.figure(figsize=(2.5*len(datatypes)+3, 12), constrained_layout=False)
gc = gridspec.GridSpec(ncols=2, nrows=1, figure=fig, width_ratios=[2.5*len(datatypes),3])

# sub gridspec
gc1 = gridspec.GridSpecFromSubplotSpec(ncols=len(datatypes), nrows=6, subplot_spec=gc[0],
                                       hspace=0.05, wspace=0.01) 
# gc1.update(hspace=0.1, wspace=0.1)

axes = {}
for n, data in enumerate(datatypes):
    axes[n] = {}
    for m, cluster in enumerate(clusters):
        if (cluster in ['1a', '1b']) and (data=='_GMC'):
           cluster = '1' 
        filename = imageDir+cluster+'_band3'+data+'.fits'
        wcs, band3_data = fits_import(filename)
        
       # plot the image
        axes[n][m] = fig.add_subplot(gc1[m, n], 
                                     projection=wcs)
        lon = axes[n][m].coords[0]
        lat = axes[n][m].coords[1]
        axes[n][m].tick_params(labelsize=3, direction='in')
        lon.set_axislabel('J2000 R.A.', fontsize=10)
        lat.set_axislabel('J2000 Dec.', fontsize=10)
        if m != 5:
            lon.set_axislabel(' ')
        if n in [1, 2]:
            lat.set_axislabel(' ')
#             lat.set_ticks_visible(False)
#             lat.set_ticklabel_visible(False)
        axes[n][m].imshow(band3_data, origin='lower', vmin = 2.8e-5, vmax=1.4e-4)
        axes[n][m].set_aspect('equal')
        
        # overlay contours
        if data not in contour_types:
            pass    
        else:
            if data in band6_types:
                filename = imageDir+cluster+'_band6'+data+'.fits'
                levels = band6_rms * np.array([3, 5, 10, 15])
            elif data in band7_types:
                filename = imageDir+cluster+'_band7'+data+'.fits'
                levels = band7_rms * np.array([3, 5, 10, 15])
            wcs_contour, contour = fits_import(filename)
            contour_proj, footprint = reproject_interp((contour, wcs_contour), wcs,
                                         shape_out=np.shape(band3_data.data))
            axes[n][m].contour(contour_proj.data, colors = 'orange', levels=levels, linewidths=1)

        # overlay aperture
        if m in regionsSky[n].keys():
            if data == '_GMC':
                color = 'magenta'
            else: 
                color = 'red'
            for region_sky in regionsSky[n][m]:
                region_pix = region_sky.to_pixel(wcs)
                region_pix.plot(color=color, linewidth=1.5)

        # overlay zoomin region
        if data == '_GMC':
            # aper_pix = apers[clusters[m]]['aperture'].to_pixel(wcs)
            # aper_pix.plot(color='red', linewidth=2) 
            print(regionsp5_sky[m])
            region_pix = regionsp5_sky[m][0].to_pixel(wcs)
            region_pix.plot(color='red', linewidth=1.5)        
     
        # annotate name of each cluster
        anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
                 va='center', ha='center', color='white', fontsize=20) 
        axes[n][m].annotate(cluster, **anno_opts)
        # annotate sub apertures in the third column
        
   # add the title for each column
    axes_lists = list(dict.values(axes[n]))
    axes_lists[0].set_title(colheaders[n], fontsize=12)

# plot the spectrums for clusters. 
axes[3] = {}
gc2 = gridspec.GridSpecFromSubplotSpec(ncols=1, nrows=6, subplot_spec=gc[1], 
                                       hspace=0.15)
for m, cluster in enumerate(clusters):
    spectrum = pd.read_csv(logDir+'cluster'+cluster+'_p5_fit.csv', header=None)
    axes[3][m] = fig.add_subplot(gc2[m, 0])
    axes[3][m].plot(spectrum[0], spectrum[1], color='blue')
    axes[3][m].plot(spectrum[0], spectrum[2], color='orange')
    axes[3][m].tick_params(labelsize=7, direction='in')
    axes[3][m].set_ylabel('Intensity (Jy/beam)', fontsize=12)

    # annotate name of each cluster
    anno_opts = dict(xy=(0.1, 0.9), xycoords='axes fraction',
             va='center', ha='center', color='white', fontsize=10)
    axes[3][m].annotate(clusters[m], **anno_opts)
 
# set the xlabel for the spectrums 
axes[3][m].set_xlabel('Velocity (km/s)', fontsize=12)
# set the title
axes[3][0].set_title('CO spectrum', fontsize=12)

fig.tight_layout()
plt.savefig(picDir+'cluster_summary_v1.pdf', bbox_inches='tight', pad_inches=0.5)
