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

comom8_file = GMC_dir + '12CO21/ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K_rebin.fits'
comom8_file2 = GMC_dir + '12CO21/ngc_4038_4039_12m_ext+12m_com+7m_co21_flat_round_k_rebin_5sig_regrid_mom8.fits'
comom0_file = GMC_dir + '12CO21/ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K_rebin.fits'


_13cofile = GMC_dir + '13CO21/member.uid___A001_X133d_X96f.NGC4038_sci.spw29.cube.I.pbcor.fits'
GMCreg_file = regionDir + 'source_band3_imfit.reg'

###########################################################
# basic settings

galaxy = 'antennae'
alphaCO = 4.3
ratio = 0.7

rms_K = 0.25

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

wcs, Tpeak = fits_import(comom8_file)
wcs, T_mom0 = fits_import(comom0_file)
wcs, Tpeak_npbcor = fits_import(comom8_file2)

# exclude the pixels with peak greater than 10 sigma
cut_off = 10 * rms_K
Tpeak[np.where(Tpeak_npbcor < cut_off)] = np.nan
nan_mask = np.ma.masked_invalid(Tpeak).mask

## Calculate the temperature. 

# background temperature
TR_bg = 11.07 / (math.exp(11.07/2.72)-1)

# calculate excitation temperature using modified version of equation 11 in 
# Heidermann+2010, assuming optical depth to be infinite
Tkin = 11.07 / np.log(1+11.07/(Tpeak+TR_bg))

## Calculate the molecular gas surface density
Sig_mol = T_mom0 / ratio * alphaCO

### Calculate the temperature and surface density for GMC apertures
# read the ds9 regions
regs = read_ds9(GMCreg_file)
regs_pix = []
clusters_Tpeak = []
clusters_Tmom0 = []
for reg in regs:
    reg.width = reg.width / 1.0
    reg.height = reg.height / 1.0
    reg_pix = reg.to_pixel(wcs)
    regs_pix.append(reg_pix)
    reg_mask = Regmask_convert(reg_pix, Tpeak)
    reg_mask = np.ma.masked_array(reg_mask, nan_mask)
    clusters_Tpeak.append(np.ma.max(reg_mask))
    reg_mask = Regmask_convert(reg_pix, T_mom0)
    clusters_Tmom0.append(np.ma.max(reg_mask))

clusters_Tpeak = np.array(clusters_Tpeak)
clusters_Tmom0 = np.array(clusters_Tmom0) 

clusters_Tkin = 11.07 / np.log(1+11.07/(clusters_Tpeak+TR_bg))
clusters_sigmol = clusters_Tmom0 / ratio * alphaCO
pbcor = np.array([0.9, 0.95, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.95, 0.95, 0.95, 0.95, 0.7])
clusters_Tkin_err = rms_K / clusters_Tpeak * clusters_Tkin
print(clusters_Tkin)
print(clusters_Tkin_err)

# fig = plt.figure()
# plt.imshow(Tpeak, origin='lower')
# for reg_pix in regs_pix:
#     reg_pix.plot(color='red')
# plt.show()

txts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
xtexts = clusters_sigmol*10**0.03
ytexts = clusters_Tkin

fig = plt.figure(figsize=(8,6))
plt.xscale('log')
plt.yscale('log')
plt.scatter(Sig_mol.flatten(), Tkin.flatten(), marker='.', label='all pixels')
plt.scatter(clusters_sigmol, clusters_Tkin, marker='o', label='YMCs')
for i, txt in enumerate(txts):
    plt.annotate(txt, (clusters_sigmol[i], clusters_Tkin[i]), 
                (xtexts[i], ytexts[i]), fontsize=20)
plt.xlabel('$\mathrm{\Sigma_{mol}}$ ($M_{\odot}$ pc$^{-2}$)', fontsize=20)
plt.ylabel('T$_{\mathrm{kin}}$ (K)', fontsize=20)
plt.legend(fontsize=15)
plt.tick_params(labelsize = 20)
fig.tight_layout()
plt.show()
plt.savefig(picDir+'GMC_LTE_temperature.pdf')



