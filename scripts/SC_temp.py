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

###########################################################
# directories and files

Dir = '/home/heh15/research/Antennae/'
imageDir=Dir+'images/'
picDir=Dir+'pictures/'
regionDir=Dir+'regions/'
logDir = Dir+'logs/'

GMC_dir = Dir+'2018/'
SC_dir = Dir + '2016/'

comom8_file = SC_dir + '12CO21/ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K_rebin.fits'
comom0_file = SC_dir + '12CO21/ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K_rebin.fits'
_13cofile = GMC_dir + '13CO21/member.uid___A001_X133d_X96f.NGC4038_sci.spw29.cube.I.pbcor.fits'
GMCreg_file = regionDir + 'source_band3_2016_imfit.reg'

###########################################################
# basic settings

galaxy = 'antennae'
alphaCO = 4.3
ratio = 0.7 

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

def Regmask_convert(aperture,data_cut):
    apmask=aperture.to_mask()
    shape=data_cut.shape
    mask=apmask.to_image(shape=((shape[0],shape[1])))
    ap_mask=mask==0
    ap_masked=np.ma.masked_where(ap_mask,data_cut)

    return ap_masked

###########################################################
# main program

## large steller associations
# import the csv file
fluxes = pd.read_csv(logDir+'flux_line.csv')
peak_Jy = fluxes['peak']
mom0_Jy = fluxes['co21 pbcor cube'] 
rms_Jy = 6e-4 
pbcor = [0.5, 0.51, 0.68, 0.69, 0.72, 0.51]
rel_err = rms_Jy / peak_Jy

# # try firecracker
# peak_Jy = 0.016

major = 0.118; minor = 0.092
restfreq = 228.7
Tpeak = peak_Jy / (0.0109 * major * minor * (228.7/115.271)**2)
Tpeak_smooth = Tpeak * major * minor / 0.18**2

TR_bg = 11.07 / (math.exp(11.07/2.72)-1)
Tkin = 11.07 / np.log(1+11.07/(Tpeak+TR_bg))
Tkin_err = rms_Jy / peak_Jy * Tkin

print(Tkin_err)

## substructure for stellar associations
peak_Jy = np.array([0.021, 0.018, 0.016, 0.02])
Tpeak_add = peak_Jy / (0.0109 * major * minor * (228.7/115.271)**2)
Tkin_add = 11.07 / np.log(1+11.07/(Tpeak_add+TR_bg))

# calculate the peak temperature for co3-2 to see if gas is thermalized
# source 2 and 5 are within the field 

peak_Jy = np.array([0.057, 0.069, 0.046])

# # Try firecracker
# peak_Jy = 0.058

major = 0.16; minor = 0.15
restfreq = 344
Tpeak_co32 = peak_Jy / (0.0109 * major * minor * (restfreq/115.271)**2)
Tpeak_co32_smooth = Tpeak_co32 * major * minor / 0.18**2

# In molly Finn's paper, they convolve the beam to 0.018 arcsec.


