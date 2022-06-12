from astropy import units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
import numpy as np
from reproject import reproject_interp
from reproject import reproject_exact
from regions import read_ds9

###########################################################
# directories

Dir = '/home/heh15/research/Antennae/'
picDir = Dir+'pictures/'
regionDir = Dir+'regions/'
HST_Dir = Dir+'HST/'
MUSE_Dir = Dir+'MUSE/'
imageDir = Dir+'images/'

###########################################################
# functions

def fits_import(fitsimage, item=0):
    hdr = fits.open(fitsimage)[item].header
    wcs = WCS(hdr).celestial
    data=fits.open(fitsimage)[item].data
    data=np.squeeze(data)
    data_masked=np.ma.masked_invalid(data)

    return wcs, data

def Regmask_convert(aperture,data_cut):
    apmask=aperture.to_mask()
    shape=data_cut.shape
    mask=apmask.to_image(shape=((shape[0],shape[1])))
    ap_mask=mask==0
    ap_masked=np.ma.masked_where(ap_mask,data_cut)

    return ap_masked

###########################################################
# main program

# import the data file
Pbeta_fitsfile = 'ib5u91050_drz.fits'
Pbeta_wcs, Pbeta_data = fits_import(Pbeta_fitsfile, item=1)
hdul = fits.open(Pbeta_fitsfile)

J_fitsfile = 'ib5u20060_drz.fits'
J_wcs, J_data = fits_import(J_fitsfile, item=1)

# reproject the data
J_data_rproj, footprint = reproject_exact((J_data, J_wcs), Pbeta_wcs,
                                shape_out=np.shape(Pbeta_data))

# save the reprojected J band image
outputfits = 'Antennae_J_reproject.fits'
hdr = Pbeta_wcs.to_header()
hdu = fits.PrimaryHDU(J_data_rproj, hdr)
hdu.writeto(outputfits, overwrite=True)

# pick out the pixels in the background subtraction region files
J_pixels = []; Pbeta_pixels = []
regionfiles = regionDir+'contsub.reg'
regions = read_ds9(regionfiles)
for region in regions:
    region_pix = region.to_pixel(Pbeta_wcs)
    regionMasked_J = Regmask_convert(region_pix,J_data_rproj)
    J_pixels += list(regionMasked_J[regionMasked_J.mask==False]) 
    regionMasked_Pbeta = Regmask_convert(region_pix, Pbeta_data)
    Pbeta_pixels += list(regionMasked_Pbeta[regionMasked_Pbeta.mask==False])

J_pixels = np.array(J_pixels); Pbeta_pixels = np.array(Pbeta_pixels)
x = J_pixels[:,np.newaxis]; y = Pbeta_pixels
a, _, _, _ = np.linalg.lstsq(x, y)
print(a)

# plt the correlation
fig = plt.figure()
plt.scatter(J_pixels, Pbeta_pixels)
plt.plot(x, a*x, 'r-')
plt.xlabel('J Band (electrons/s)')
plt.ylabel(r'Pa$\beta$ (electrons/s)')
plt.savefig(picDir+'continuum_sub_scaleFactor.pdf', bbox_inches='tight', pad_inches=0.2)

# subtract the continuum
Pbeta_data_contsub = Pbeta_data - a[0]*J_data_rproj

# save the subtracted continuum into fitsfile
hdul[1].data = Pbeta_data_contsub

outputfits = 'Antennae_Pbeta_contsub.fits'
# hdr = Pbeta_wcs.to_header()
# hdu = fits.PrimaryHDU(Pbeta_data_contsub, hdr)
hdul.writeto(outputfits, overwrite=True)
