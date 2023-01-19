import pandas as pd
import numpy as np
import math
from math import log10, floor

#############################################################################
# basic settings
freq_band3 = 100
freq_band6 = 220
freq_band7 = 340

freq_co21 = 230

co2_1_ratio = 0.7

D_Mpc = 22
D = D_Mpc*1e6*3.1e16
beta = 1.5
z = 0.0055

#############################################################################
# functions

def round_sig(x, sig=2):
    '''
    round the x to certain significant figures
    '''
    return round(x, sig-int(floor(log10(abs(x))))-1)

def freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                 lowBand_err=0, highBand_err=0):
    '''
    subtract the free-free emission
    '''
    fluxes = pd.DataFrame()
    ff_flux =  lowBand_flux * (high_freq/low_freq)**(-0.1)
    ff_err = ff_flux * (lowBand_err/lowBand_flux)

    # subtract to get the dust emission
    dust_flux = highBand_flux - ff_flux
    sum_square = (ff_err**2 + highBand_err**2).astype(np.float64)
    dust_err = np.sqrt(sum_square)
    ff_frac = ff_flux / highBand_flux
    sum_square = ((ff_err/ff_flux)**2
              + (highBand_err/highBand_flux)**2).astype(np.float64)
    frac_err = ff_frac * np.sqrt(sum_square)
    frame = {'ff_flux': ff_flux, 'ff_err': ff_err, 'dust_flux': dust_flux,
             'dust_err': dust_err, 'ff_frac': ff_frac, 'frac_err': frac_err}
    fluxes = pd.DataFrame(frame)
    
    return fluxes

#############################################################################
# main program

# import and preprocess data
df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')
df['band3 flux (mJy)'][1] = np.nan
df['band 3 (high res)'][8] = np.nan
df['band 7 (high res)'][3:5] = np.nan
df['band 7 (high res)'][8] = np.nan
# df['band 7 (high res)'][9] = np.nan

statistics_SC = ['ff_flux', 'ff_err', 'dust_flux', 'dust_err', 'ff_frac',
                 'frac_err']
statistics_GMC = ['ff_flux', 'ff_err', 'dust_flux', 'dust_err', 'dust_band7', 
                  'band7_err']

### split the free-free emission from dust emission in Band 7. 


## calculate free-free emission in band 7 for star cluster data. 
high_freq = freq_band7; low_freq = freq_band3
lowBand_flux = df['band 3 (high res)']; lowBand_err = df['flux uncertainty.1']
highBand_flux = df['band 7 (high res)']; highBand_err = df['flux uncertainty.2']

fluxes_SC = freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                      lowBand_err=lowBand_err, 
                      highBand_err=highBand_err)

# Try determine the band 6 free-free fraction for star clusters
fluxes_SC['dust_band6'] = fluxes_SC['dust_flux']*(freq_band6/freq_band7)**(beta+2)
fluxes_SC['dust_band6_err'] = fluxes_SC['dust_band6']*\
    (fluxes_SC['dust_err']/fluxes_SC['dust_flux'])
    
fluxes_SC['freefree_band6'] = lowBand_flux * (freq_band6/low_freq)**(-0.1)

## for star cluster with robust parameter of 0.5.
high_freq = freq_band7; low_freq = freq_band3
lowBand_flux = df['band 3 (high res, 0.5)']; lowBand_err = df['flux uncertainty.3']
highBand_flux = df['band 7 (high res, 0.5)']; highBand_err = df['flux uncertainty.4']

fluxes_SC_p5 = freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                      lowBand_err=lowBand_err, 
                      highBand_err=highBand_err)


# larger apertures applied to robust 0.5 images
high_freq = freq_band7; low_freq = freq_band3
df1 = pd.read_excel('flux_measure.xlsx', sheet_name='flux_check')
lowBand_flux = df1['band3 (robust 0.5, 0.11)']; lowBand_err = df1['flux uncertainty']
highBand_flux = df1['band7 (robust 0.5)']; highBand_err = df1['flux uncertainty.2']

fluxes_check = freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                      lowBand_err=lowBand_err, 
                      highBand_err=highBand_err)

# apertures for substructures
high_freq = freq_band7; low_freq = freq_band3
df_add = pd.read_excel('flux_measure.xlsx', sheet_name='imfit_add')
lowBand_flux = df_add['flux, rob0.5, 0.09']; lowBand_err = df_add['uncertainty']
highBand_flux = df_add['band7 flux']; highBand_err = df_add['uncertainty.1']

fluxes_SC_add = freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                      lowBand_err=lowBand_err, 
                      highBand_err=highBand_err)

## for GMC data
high_freq = freq_band6; low_freq = freq_band3
lowBand_flux = df['band3 flux (mJy)']; lowBand_err = df['flux uncertainty']
highBand_flux = df['band6 flux (mJy)']; highBand_err = df['band 6 uncertainty']

fluxes_GMC = freefree_sub(lowBand_flux, highBand_flux, low_freq, high_freq, 
                      lowBand_err=lowBand_err, 
                      highBand_err=highBand_err)

fluxes_GMC['dust_band7'] = fluxes_GMC['dust_flux']*(freq_band7/freq_band6)**(beta+2)
fluxes_GMC['band7_err'] = fluxes_GMC['dust_band7']*\
    (fluxes_GMC['dust_err']/fluxes_GMC['dust_flux'])
    
    
with pd.ExcelWriter('tables/flux_split.xlsx') as writer:  
    fluxes_SC.to_excel(writer, sheet_name='star cluster')
    fluxes_SC_p5.to_excel(writer, sheet_name='star cluster 0.5')
    fluxes_check.to_excel(writer, sheet_name='SC, check')
    fluxes_SC_add.to_excel(writer, sheet_name='SC, add')
    fluxes_GMC.to_excel(writer, sheet_name='GMC')


