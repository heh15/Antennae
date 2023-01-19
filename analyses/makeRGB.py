import numpy as np
import pandas as pd
import aplpy
from reproject import reproject_exact
from reproject import reproject_interp
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from reproject.mosaicking import find_optimal_celestial_wcs
# import img_scale as IS
from astropy.visualization import AsymmetricPercentileInterval, simple_norm


###########################################################
# directories

imageDir = '../images/'

###########################################################
# functions

def fits_import(fitsimage, item=0):
    '''
    Import the fits image data.
    ------
    Parameters:
    fitsimage: string
        Path to the fits image.
    item:
        index number in fits hdu file that contains actual data
    '''
    hdr = fits.open(fitsimage)[item].header
    wcs = WCS(hdr).celestial
    data=fits.open(fitsimage)[item].data
    data=np.squeeze(data)

    return wcs, data

def reproject_north(data, wcs):
    '''
    Parameters
    ----------
    data : np.2darray
        Data of the image
    wcs : wcs
        WCS information of the image

    Returns
    -------
    wcs_north : wcs
        Output wcs point to the north
    data_north : np.2darray
        Reprojected data

    '''
    wcs_north = WCS(naxis=2)
    wcs_north.wcs.crval = wcs.wcs.crval
    wcs_north.wcs.crpix = wcs.wcs.crpix
    cd = wcs.wcs.cd
    wcs_north.wcs.cd = np.sqrt(cd[0,0]**2+cd[1,0]**2)*np.array([[-1,0],[0,1]])
    wcs_north.wcs.ctype = ['RA---SIN', 'DEC--SIN']
    data_north, footprint = reproject_exact((data, wcs), wcs_north,
                                            shape_out=np.shape(data))

    return wcs_north, data_north

def output_fits(fitsimage, data, wcs):
    '''
    Parameters
    ----------
    fitsimage : str
        Filename of the fits image
    data : np.2darray
        Data of the image
    wcs : wcs
        wcs information

    Returns
    -------
    None.

    '''
    header = wcs.to_header()
    hdu = fits.PrimaryHDU(data, header)
    hdu.writeto(fitsimage, overwrite=True)

    return


###########################################################
# main program

I_fits = imageDir+'Antennae_I_ib5u20090_drz.fits'
V_fits = imageDir+'Antennae_V_ib5820080_drz.fits'
U_fits = imageDir+'Antennae_U_ib5u12050_drz.fits'

# # reproject the I data to the north
# wcs_I, data_I = fits_import(I_fits, item=1)
# wcs_north, data_I_north = reproject_north(data_I, wcs_I)
# output_fits(imageDir+'Antennae_I_north.fits', data_I_north, wcs_north)

# import the reprojected I data
wcs_I, data_I = fits_import(imageDir+'Antennae_I_north.fits')

# # reproject V and U band image
# wcs_V, data_V = fits_import(V_fits,item=1)
# wcs_U, data_U = fits_import(U_fits,item=1)
# data_V, footprint = reproject_interp((data_V, wcs_V), wcs_I, 
#                                   shape_out=np.shape(data_I))
# data_U, footprint = reproject_interp((data_U, wcs_U), wcs_I, 
#                                   shape_out=np.shape(data_I))
# output_fits(imageDir+'Antennae_V_north.fits',data_V, wcs_I)
# output_fits(imageDir+'Antennae_U_north.fits',data_U,wcs_I)

data_V = fits_import(imageDir+'Antennae_V_north.fits')[1]
data_U = fits_import(imageDir+'Antennae_U_north.fits')[1]


aplpy.make_rgb_image([imageDir+'Antennae_I_north.fits', 
                      imageDir+'Antennae_V_north.fits',
                      imageDir+'Antennae_U_north.fits'], 
                      imageDir+'Antennae_IUV.png',
                      pmax_b=99.5, pmin_b=0.5)

## overlay other data/annotation on the image

# # method 1
# image = np.flipud(plt.imread(imageDir+'Antennae_IUV.png'))
# fig = plt.figure()
# ax = plt.subplot(111, projection=wcs_I)
# ax.imshow(image)
# plt.savefig(imageDir+'Antennae_IUV.pdf', dpi=500)

# method 2
f = aplpy.FITSFigure(imageDir+'Antennae_I_north.fits')
f.show_rgb(imageDir+'Antennae_IUV.png')
f.ax.annotate('Antennae', (0.1, 0.8), xycoords='axes fraction', color='white',
              fontsize=15)
f.savefig(imageDir+'Antennae_IUV.pdf', dpi=300)
