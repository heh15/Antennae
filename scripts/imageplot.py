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

############################################################
# directories and files

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'region/'
logDir = Dir+'logs/'

GMC_dir = Dir+'2018/'
SC_dir = Dir + '2016/'

cont_Band3_GMC = Dir + '2018/cont_100GHz/image/'\
                       'ngc4038_band3_cont_12m_7m_pbcor.fits'
cont_Band3_SC = Dir + '2016/Band3/ngc40389overlap_band3_uvrange_robust_2_smooth_pbcor.fits' 

cont_Band6_GMC = Dir + '2018/cont_200GHz/image/'\
                       'ngc4038_band6_cont_12m_7m_pbcor.fits'
cont_Band7_SC = Dir + '2016/Band3/ngc40389overlap_band7_range_robust_2_smooth_pbcor.fits'

############################################################
# basic settings
galaxy='antennae'
line='100 GHz'

GMC_ra = 15 * (12*u.degree + 1*u.arcmin + 53.192*u.arcsec)
GMC_dec = -(18*u.degree + 52*u.arcmin + 31.8*u.arcsec) 
SC_ra = 15*(12*u.degree + 1*u.arcmin + 55*u.arcsec)
SC_dec = -(18*u.degree + 52*u.arcmin + 51*u.arcsec)
  

datatypes = ['band3_GMC', 'band3_SC', 'band6_GMC', 'band7_SC', 'band3_GMC_zoom', 
            'band3_SC_zoom', 'band3_GMC_overlay', 'band6_GMC_zoom', 'band7_SC_zoom']

datatypes = ['band3_GMC', 'band3_SC', 'band6_GMC', 'band7_SC']
parameters = ['imagename']
continuum = dict.fromkeys(datatypes)
for key in continuum.keys():
    continuum[key] = {}    

# continuum image for Band 3 GMC data
continuum['band3_GMC']['imagename'] = cont_Band3_GMC
continuum['band3_GMC']['vmax'] = 1.18e-4
continuum['band3_GMC']['vmin'] = 2*1.2e-5
continuum['band3_GMC']['color_scheme'] = 'viridis'

# # continuum image for band 3 GMC zoom-in 
# continuum['band3_GMC_zoom'] = continuum['band3_GMC']
# 
# # continuum image for band 3 GMC overlay
# continuum['band3_GMC_overlay'] = continuum['band3_GMC']

# continuum image for Band 3 SC data
continuum['band3_SC']['imagename'] = cont_Band3_SC
continuum['band3_SC']['vmax'] = 1.4e-4
continuum['band3_SC']['vmin'] = 2*1.4e-5
continuum['band3_SC']['color_scheme'] = 'viridis'

# # continuum image for band 3 SC zoom-in
# continuum['band3_SC_zoom'] = continuum['band3_SC']

# continuum image for Band 6 GMC data
continuum['band6_GMC']['imagename'] = cont_Band6_GMC
continuum['band6_GMC']['vmax'] = 5.24e-4
continuum['band6_GMC']['vmin'] = 2*5.3e-5
continuum['band6_GMC']['color_scheme'] = 'hot'

# # continuum image for band 6 zoom-in
# continuum['band6_GMC_zoom'] = continuum['band6_GMC']

# continuum image for Band 7 SC data
continuum['band7_SC']['imagename'] = cont_Band7_SC
continuum['band7_SC']['vmax'] = 4.2e-4
continuum['band7_SC']['vmin'] = 2*4.1e-5
continuum['band7_SC']['color_scheme'] = 'hot'

# # continuum image for band 7 zoom-in
# continuum['band7_SC_zoom'] = continuum['band7_SC']

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

############################################################
# basic settings

testra = 204.97609228
testdec = 0.84611111

linelabel = '$^{12}$CO 1-0'

vmin = 2*1.2e-5

############################################################
# main program

### plot the image
GMC = ['band3_GMC', 'band6_GMC', 'band3_GMC_zoom', 
        'band3_GMC_overlay', 'band6_GMC_zoom']
band3_SC = ['band3_SC', 'band3_SC_zoom']
band6_GMC = ['band6_GMC', 'band6_GMC_zoom', 'band6_GMC_overlay']
band7_SC = ['band7_SC', 'band7_SC_zoom']
zoom_data = ['band3_GMC_zoom', 'band3_SC_zoom','band6_GMC_zoom', 
            'band7_SC_zoom']
overlay_data = ['band3_GMC_overlay']

GMC = ['band3_GMC', 'band6_GMC']
SC = ['band3_SC', 'band6_SC']

overlay_CO = True
overlay_FOV = True
overlay_Rcluster = True
draw_region = True

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
        size = u.Quantity((2.0, 2.0), u.arcmin)
    else: 
        ra = SC_ra
        dec = SC_dec
        position = SkyCoord(dec=dec, ra=ra, frame='icrs')
        if data in band3_SC:
            size = u.Quantity((1.2, 1.2), u.arcmin)
        elif data in band7_SC:
            size = u.Quantity((0.7, 0.7), u.arcmin)
    wcs_cut, cont_image_cut = cut_2d(cont_image, position, size, wcs) 
    
    pictureName = 'ngc40389_' + data + '.png' 
 
    fig = plt.figure(figsize=[10,10], dpi=120)
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
    
    if overlay_CO == True: 
        co_mom0_file = Dir + 'ngc4038co.fits'
        wcs_co, data_co = fits_import(co_mom0_file)
        co_contour, footpring = reproject_interp((data_co, wcs_co),
                                                 wcs_cut, 
                                                 shape_out=np.shape(cont_image_cut))
        levels = 90.6*np.array([0.01, 0.016, 0.025, 0.04, 0.06, 0.095, 0.15, 0.23, 0.37, 0.57])
        ax.contour(co_contour, levels=levels, colors='white', linewidths=0.2,
                   origin='lower')
        pictureName = pictureName.replace('.png', '_CO2-1.png')        

    if overlay_FOV == True:  
        if data == 'band3_GMC': 
            ra = SC_ra
            dec = SC_dec
            position = SkyCoord(dec=dec, ra=ra, frame='icrs')
            FOV_2016 = SkyCircularAperture(position, r=0.765*u.arcmin)
            FOV_2016_pix = FOV_2016.to_pixel(wcs_cut)
            FOV_2016_pix.plot(color='red', clip_on=False)
        if data == 'band6_GMC':
            band7_pbimage = SC_dir + 'Band3/'\
                          'ngc40389overlap_band7_range_robust_2_pb.fits'
            wcs_pb, data_pb = fits_import(band7_pbimage)
            levels = [0.21]
            contour, footprint = reproject_interp((data_pb, wcs_pb), 
                                                   wcs_cut, 
                                                   shape_out=np.shape(cont_image_cut))        
            ax.contour(contour, levels=levels,colors='red', linewidths=2.0)
        pictureName = pictureName.replace('.png', '_FOV.png')

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
        pictureName = pictureName.replace('.png', '_Rcluster.png')

    if draw_region == True:
        for key in zooms.keys():
            aperture = zooms[key]['aperture'].to_pixel(wcs_cut)
            aperture.plot(color='red') 
            pictureName = pictureName.replace('.png', '_'+key+'.png')
            plt.savefig(picDir+pictureName)
            ax.patches[-1].remove()
            pictureName = pictureName.replace('_'+key+'.png', '.png')
    else:
        plt.savefig(picDir+pictureName)


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

