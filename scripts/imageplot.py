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

############################################################
# directories and files

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'regions/'
logDir = Dir+'logs/'

GMC_dir = Dir+'2018/'
SC_dir = Dir + '2016/'

cont_Band3_GMC = Dir + '2018/cont_100GHz/image/'\
                       'ngc4038_band3_cont_12m_7m_pbcor.fits'
cont_Band3_SC = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_2_smooth_pbcor.fits'

cont_Band3_SC_p5 = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_p5_smooth_pbcor.fits'

cont_Band3_SC_p5_009 = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_p5_smooth_090_pbcor.fits' 

cont_Band6_GMC = Dir + '2018/cont_200GHz/image/'\
                       'ngc4038_band6_cont_12m_7m_pbcor.fits'
cont_Band7_SC = Dir + '2016/Band3/ngc40389overlap_band7_range_robust_2_smooth_pbcor.fits'

cont_Band7_SC_p5 = Dir + '2016/Band3/ngc40389overlap_band7_range_robust_p5_smooth_pbcor.fits'

############################################################
# function 

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

############################################################
# basic settings
galaxy='antennae'
line='100 GHz'

GMC_ra = 15 * (12*u.degree + 1*u.arcmin + 53.192*u.arcsec)
GMC_dec = -(18*u.degree + 52*u.arcmin + 31.8*u.arcsec) 
SC_ra = 15*(12*u.degree + 1*u.arcmin + 54.9*u.arcsec)
SC_dec = -(18*u.degree + 52*u.arcmin + 51*u.arcsec)


datatypes = ['band3_GMC', 'band3_SC','band3_SC_p5',  'band6_GMC', 'band7_SC']
parameters = ['imagename']
continuum = dict.fromkeys(datatypes)
for key in continuum.keys():
    continuum[key] = {}    

# continuum image for Band 3 GMC data
continuum['band3_GMC']['imagename'] = cont_Band3_GMC
continuum['band3_GMC']['vmax'] = 1.18e-4
continuum['band3_GMC']['vmin'] = 2*1.2e-5
continuum['band3_GMC']['color_scheme'] = 'viridis'
continuum['band3_GMC']['txts'] = ['1','2','3','4','5','6','7','8','9','10','11','12','13']

regionfiles = regionDir + 'source_coords_band3.reg'
coords = import_coords(regionfiles, ra_add=2*u.arcsec, dec_add=-4*u.arcsec)
coords[5] = SkyCoord(ra=coords[5].ra-4*u.arcsec, dec= coords[5].dec+2*u.arcsec, frame='icrs')
coords[2] = SkyCoord(ra=coords[2].ra+1*u.arcsec, dec=coords[2].dec+2*u.arcsec, frame='icrs')
coords[10] = SkyCoord(ra=coords[10].ra+3*u.arcsec, dec=coords[10].dec+2*u.arcsec)
coords[11] = SkyCoord(ra=coords[11].ra+3*u.arcsec, dec=coords[11].dec+2*u.arcsec)
continuum['band3_GMC']['txt_coords'] = coords

# continuum image for Band 3 SC data
continuum['band3_SC']['imagename'] = cont_Band3_SC
continuum['band3_SC']['vmax'] = 1.4e-4
continuum['band3_SC']['vmin'] = 2*1.4e-5
continuum['band3_SC']['color_scheme'] = 'viridis'
continuum['band3_SC']['txts'] = ['1a','1b','2','3','4','5','7','9']

regionfiles = regionDir + 'source_coords_band3_2016.reg'
coords = import_coords(regionfiles, ra_add=1*u.arcsec, dec_add=-2*u.arcsec)
coords[1] = SkyCoord(ra=coords[1].ra+2*u.arcsec, dec=coords[1].dec+2*u.arcsec, frame='icrs')
coords[3] = SkyCoord(ra=coords[3].ra+0.5*u.arcsec, dec=coords[3].dec+1*u.arcsec, frame='icrs')
continuum['band3_SC']['txt_coords'] = coords

# # continuum image for Band 3 SC data with robust of 0.5 (0.11 arcsec)
continuum['band3_SC_p5'] = copy.deepcopy(continuum['band3_SC'])
continuum['band3_SC_p5']['imagename'] = cont_Band3_SC_p5

# # continuum image for Band 3 SC data, robust 0.5, beam 0.09 arcsec
continuum['band3_SC_p5_009'] = copy.deepcopy(continuum['band3_SC'])
continuum['band3_SC_p5_009']['imagename'] = cont_Band3_SC_p5_009

# continuum image for Band 6 GMC data
continuum['band6_GMC']['imagename'] = cont_Band6_GMC
continuum['band6_GMC']['vmax'] = 5.24e-4
continuum['band6_GMC']['vmin'] = 2*5.3e-5
continuum['band6_GMC']['color_scheme'] = 'hot'
continuum['band6_GMC']['txts'] = ['1','2','3','5','6','7','8','9','10','11','12','13']

regionfiles = regionDir + 'source_coords_band6.reg'
coords = import_coords(regionfiles, ra_add=2*u.arcsec, dec_add=-4*u.arcsec)
coords[4] = SkyCoord(ra=coords[4].ra-4*u.arcsec, dec= coords[4].dec+2*u.arcsec, frame='icrs')
coords[9] = SkyCoord(ra=coords[9].ra+3*u.arcsec, dec=coords[9].dec+2*u.arcsec)
coords[10] = SkyCoord(ra=coords[10].ra+3*u.arcsec, dec=coords[10].dec+2*u.arcsec)
continuum['band6_GMC']['txt_coords'] = coords

# continuum image for Band 7 SC data
continuum['band7_SC']['imagename'] = cont_Band7_SC
continuum['band7_SC']['vmax'] = 4.2e-4
continuum['band7_SC']['vmin'] = 2*4.1e-5
continuum['band7_SC']['color_scheme'] = 'hot'
continuum['band7_SC']['txts'] = ['1a','1b', '2','5','6','7','9']

regionfiles = regionDir + 'source_coords_band7_2016.reg'
coords = import_coords(regionfiles, ra_add=1*u.arcsec, dec_add=-2*u.arcsec)
coords[1] = SkyCoord(ra=coords[1].ra+2*u.arcsec, dec=coords[1].dec+2*u.arcsec, frame='icrs')
coords[4] = SkyCoord(ra=coords[4].ra-2*u.arcsec, dec=coords[4].dec)
continuum['band7_SC']['txt_coords'] = coords

# continuum image for Band 7 SC data with robust of 0.5
continuum['band7_SC_p5'] = copy.deepcopy(continuum['band7_SC'])
continuum['band7_SC_p5']['imagename'] = cont_Band7_SC_p5

# import individual clusters to zoom in 
sys.path.append('configs')
from imageplot_cluster_zoomin import clusters 

# regions to zoom in
region_labels = ['a', 'b', 'c']
features = ['aperture', 'position', 'size']
zooms = dict.fromkeys(region_labels)
for key in zooms.keys():
    zooms[key] = dict.fromkeys(features)

# region a
ra = 15*(12*u.degree+1*u.arcmin+54.762*u.arcsec)
dec = -(18*u.degree+53*u.arcmin+4.4*u.arcsec)
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
zooms['a']['position'] = center 
zooms['a']['size'] = u.Quantity((0.144, 0.23), u.arcmin)
zooms['a']['aperture'] =  SkyRectangularAperture(center, 0.144*u.arcmin, 0.23*u.arcmin) 

# region b
ra = 15*(12*u.degree+1*u.arcmin+53.39*u.arcsec)
dec = -(18*u.degree+53*u.arcmin+8.9*u.arcsec)
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
zooms['b']['position'] = center
zooms['b']['size'] = u.Quantity((0.11, 0.2), u.arcmin)
zooms['b']['aperture'] =  SkyRectangularAperture(center, 0.11*u.arcmin, 0.2*u.arcmin)

# region c
ra = 15*(12*u.degree+1*u.arcmin+55.106*u.arcsec)
dec = -(18*u.degree+52*u.arcmin+41*u.arcsec)
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
zooms['c']['position'] = center
zooms['c']['size'] = u.Quantity((0.46, 0.32), u.arcmin)
zooms['c']['aperture'] =  SkyRectangularAperture(center, 0.46*u.arcmin, 0.32*u.arcmin)

gamma = 1.0

############################################################
# basic settings

testra = 204.97609228
testdec = 0.84611111

linelabel = '$^{12}$CO 1-0'

vmin = 2*1.2e-5

############################################################
# main program

### plot the image


GMC = ['band3_GMC', 'band6_GMC']
band3_SC = ['band3_SC']
band7_SC = ['band7_SC']

add_label = True
overlay_CO_Chris = False
overlay_CO_Nate = True
overlay_FOV = True
overlay_Rcluster = False
draw_region = False

datatypes = ['band3_SC', 'band7_SC', 'band3_GMC', 'band6_GMC']
extension = '.pdf'

for data in datatypes:
    # import image and cut the image. 
    fitsimage = continuum[data]['imagename']
    wcs = fits_import(fitsimage)[0]
    cont_image = fits_import(fitsimage)[1]

    # cut the image 
    if data in GMC:
        ra = GMC_ra
        dec = GMC_dec
        position = SkyCoord(dec=dec, ra=ra, frame='icrs')
        size = u.Quantity((1.5, 1.5), u.arcmin)
    else: 
        ra = SC_ra
        dec = SC_dec
        position = SkyCoord(dec=dec, ra=ra, frame='icrs')
        if data in band3_SC:
            size = u.Quantity((0.7, 0.7), u.arcmin)
        elif data in band7_SC:
            size = u.Quantity((0.7, 0.7), u.arcmin)
    wcs_cut, cont_image_cut = cut_2d(cont_image, position, size, wcs) 
    
    pictureName = 'ngc40389_' + data + extension
 
    fig = plt.figure(figsize=[5,5])
    ax = plt.subplot(111, projection=wcs_cut) 

    # give the default value for vmax and vmin
    gamma = 1.0
    if continuum[data]['vmin'] == None:
        continuum[data]['vmin'] = np.minimum(cont_image_cut)
    if continuum[data]['vmax'] == None:
        continuum[data]['vmax'] = np.maximum(cont_image_cut)   
    if continuum[data]['color_scheme'] == None:
        continuum[data]['color_scheme'] == 'viridis'
    
    im = ax.imshow(cont_image_cut,
                    norm=colors.PowerNorm(gamma=gamma),
                    vmin=continuum[data]['vmin'],
                    vmax=continuum[data]['vmax'], 
                    origin='lower',
                    cmap=continuum[data]['color_scheme'])    
    ax.set_xlabel('J2000 Right Ascension')
    ax.set_ylabel('J2000 Declination')
    ax.set_xlim(0, np.shape(cont_image_cut)[0])
    ax.set_ylim(0, np.shape(cont_image_cut)[1])
    ax.tick_params(labelsize=5, direction='in')

    if add_label == True: 
        coords_pix = []
        for coord in continuum[data]['txt_coords']:
            coord_pix = coord.to_pixel(wcs_cut)
            coords_pix.append(coord_pix)
        for i, txt in enumerate(continuum[data]['txts']):
             plt.text(coords_pix[i][0], coords_pix[i][1],  txt, fontsize=10, color='orange')
        pictureName = pictureName.replace(extension, '_label'+extension)
         
    if overlay_CO_Chris == True: 
        co_mom0_file = Dir + 'ngc4038co.fits'
        wcs_co, data_co = fits_import(co_mom0_file)
        co_contour, footprint = reproject_interp((data_co, wcs_co),
                                                 wcs_cut, 
                                                 shape_out=np.shape(cont_image_cut))
        levels = 90.6*np.array([0.01, 0.016, 0.025, 0.04, 0.06, 0.095, 0.15, 0.23, 0.37, 0.57])
        ax.contour(co_contour, levels=levels, colors='white', linewidths=0.2,
                   origin='lower')
        pictureName = pictureName.replace(extension, '_CO2-1'+extension)        
        
    if overlay_CO_Nate == True: 
        co_mom0_file = Dir + '2018/12CO21/'\
                'ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K.fits'        
        wcs_co, data_co = fits_import(co_mom0_file)
        co_contour, footprint = reproject_interp((data_co, wcs_co), 
                                                wcs_cut,
                                                shape_out=np.shape(cont_image_cut))
        levels = 9.33 * np.array([5, 10, 20, 30, 40]) 
        ax.contour(co_contour, colors='grey', linewidths=0.05, origin='lower', 
                   levels=levels)
        pictureName = pictureName.replace(extension, '_CO2-1Nate'+extension)

    if overlay_FOV == True:  
        if data == 'band3_GMC': 
            ra = SC_ra
            dec = SC_dec
            position = SkyCoord(dec=dec, ra=ra, frame='icrs')
            FOV_2016 = SkyCircularAperture(position, r=0.765*u.arcmin)
            FOV_2016_pix = FOV_2016.to_pixel(wcs_cut)
            FOV_2016_pix.plot(color='red', clip_on=True)
        if data == 'band6_GMC':
            band7_pbimage = SC_dir + 'Band3/'\
                          'ngc40389overlap_band7_range_robust_2_pb.fits'
            wcs_pb, data_pb = fits_import(band7_pbimage)
            levels = [0.21]
            contour, footprint = reproject_interp((data_pb, wcs_pb), 
                                                   wcs_cut, 
                                                   shape_out=np.shape(cont_image_cut))        
            ax.contour(contour, levels=levels,colors='red', linewidths=2.0)
        pictureName = pictureName.replace(extension, '_FOV'+extension)

    if overlay_Rcluster == True: 
        # import the R cluster coordinates
        RSC_cat = pd.read_csv(logDir+'Rclusters_Zhang2001.csv', 
                               index_col = 0, header=None)
        ras = 15*(12*u.degree + 1*u.arcmin + 52.97*u.arcsec)+np.array(RSC_cat[1])*u.arcsec
        decs = -(18*u.degree+52*u.arcmin+8.29*u.arcsec) + np.array(RSC_cat[2])*u.arcsec
        positions = SkyCoord(ra = ras, dec = decs)
        aper = SkyCircularAperture(positions, 0.15*u.arcsec)
        aper_pix = aper.to_pixel(wcs_cut)
        aper_pix.plot(color='white')
        pictureName = pictureName.replace(extension, '_Rcluster'+extension)
    
        
    if draw_region == True:
        for key in zooms.keys():
            aperture = zooms[key]['aperture'].to_pixel(wcs_cut)
            aperture.plot(color='red') 
            pictureName = pictureName.replace(extension, '_'+key+extension)
            plt.savefig(picDir+pictureName, bbox_inches='tight')
            ax.patches[-1].remove()
            pictureName = pictureName.replace('_'+key+extension, extension)
    else:
        plt.savefig(picDir+pictureName, bbox_inches='tight')

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

datatypes = []
# # cut out individual regions for each cluster. 
# for data in datatypes:
#     fitsimage = continuum[data]['imagename']
#     wcs = fits_import(fitsimage)[0]
#     cont_image = fits_import(fitsimage)[1]
#     # cut the image out 
#     if data in zoom_data: 
#         for key in zooms.keys():
#             region_wcs, region_data = cut_2d(cont_image.data, zooms[key]['position'],
#                                              zooms[key]['size'], wcs)
#             outputfits = imageDir + key + '_'+data+'.fits' 
#             header = region_wcs.to_header()
#             hdu = fits.PrimaryHDU(region_data.data, header)
#             hdu.writeto(outputfits, overwrite=True)

