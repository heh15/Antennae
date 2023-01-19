# Deconvolution of the beam to see the actual size of the sources. 

# actual size, deconvolve the beam

import astropy
from radio_beam import Beam
from astropy import units as u
import math

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def deconvolve(SC_size, little_beam):
    for i in SC_size.index:
        major = SC_size['major'][i] * u.arcsec
        minor = SC_size['minor'][i] * u.arcsec
        pa = SC_size['pa'][i] * u.deg
        big_beam = Beam(major, minor, pa)
        try: 
            beam_recovered = big_beam.deconvolve(little_beam).to_header_keywords()
        except:
            print('Cannot deconvolve the beam')
            beam_recovered = big_beam.to_header_keywords()
        if math.isnan(beam_recovered['BMAJ']):
            SC_size['major_orig'][i] = np.nan
            SC_size['minor_orig'][i] = np.nan
            SC_size['pa_orig'][i] = np.nan
            continue
        SC_size['major_orig'][i] = round_sig(beam_recovered['BMAJ']*3600)
        SC_size['minor_orig'][i] = round_sig(beam_recovered['BMIN']*3600)
        SC_size['pa_orig'][i] = round(beam_recovered['BPA'], 2)
    
    return 0

def deconvolve_individual(SC_size, i, little_beam):
    major = SC_size['major'][i] * u.arcsec
    minor = SC_size['minor'][i] * u.arcsec
    pa = SC_size['pa'][i] * u.deg
    big_beam = Beam(major, minor, pa)
    try: 
        beam_recovered = big_beam.deconvolve(little_beam).to_header_keywords()
    except:
        print('Cannot deconvolve the beam')
        beam_recovered = big_beam.to_header_keywords()
    SC_size['major_orig'][i] = round_sig(beam_recovered['BMAJ']*3600)
    SC_size['minor_orig'][i] = round_sig(beam_recovered['BMIN']*3600)
    SC_size['pa_orig'][i] = round(beam_recovered['BPA'], 2)
    
    return 0


df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')
df['band3 flux (mJy)'][1] = np.nan
df['band 3 (high res)'][8] = np.nan

beam_quantities = ['major', 'minor', 'pa', 'major_orig', 'minor_orig', 
                   'pa_orig']
SC_size = pd.DataFrame(columns=beam_quantities, index=df.index)
SC_size['major'] = df['major (arcsec).1']
SC_size['minor'] = df['minor (arcsec).1']
SC_size['pa'] = df['PA (deg).1']

# Deconvolve the beam   
little_beam = Beam(0.134*u.arcsec, 0.134*u.arcsec, 0*u.deg)
deconvolve(SC_size, little_beam)

SC_size['physical'] = SC_size['major_orig'] * 4.85 * 22

## deconvolve the size of aperture derived from robust 0.5 image
SC_size1 = pd.DataFrame(columns=beam_quantities, index=df.index)
SC_size1['major'] = df['major.1']
SC_size1['minor'] = df['minor.1']
SC_size1['pa'] = df['pa.1']

# little_beam = Beam(0.087*u.arcsec, 0.074*u.arcsec, 49*u.deg)
little_beam = Beam(0.09*u.arcsec, 0.09*u.arcsec, 0*u.deg)
deconvolve(SC_size1, little_beam)
SC_size1['resolved'] = df['Resolved.1']
SC_size1['S/N'] = df['S/N']

# aperture 6 
little_beam = Beam(0.11*u.arcsec, 0.11*u.arcsec, 0*u.deg)
deconvolve_individual(SC_size1, 6, little_beam)

# get the physical size of the source 
SC_size1['physical'] = SC_size1['major_orig'] * 4.85 * 22

## deconvolve the point sources that broken into multiple sources
df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit_add')
SC_size2 = pd.DataFrame(columns=beam_quantities, index=df.index)
SC_size2['major'] = df['major']
SC_size2['minor'] = df['minor']
SC_size2['pa'] = df['PA']


little_beam = Beam(0.09*u.arcsec, 0.09*u.arcsec, 0*u.deg)
deconvolve(SC_size2, little_beam)
SC_size2.index = df['source']

# get the upper limit of the source 9
minor_9a = SC_size2['minor']['9a']
minor_9b = SC_size2['minor']['9b']
SC_size2['minor']['9a'] =  0.1
SC_size2['minor']['9b'] = 0.1
deconvolve_individual(SC_size2, 6, little_beam)
deconvolve_individual(SC_size2, 7, little_beam)

SC_size2['minor']['9a'] = minor_9a
SC_size2['minor']['9b'] = minor_9b

# get the upper limit of the source 1bi
minor_1bi = SC_size2['minor']['1b i']
SC_size2['minor']['1b i'] =  0.1
deconvolve_individual(SC_size2, 0, little_beam)
SC_size2['minor']['1b i'] = minor_1bi

# calculate the physical size
SC_size2['physical'] = SC_size2['major_orig'] * 4.85 * 22

# with pd.ExcelWriter('tables/source_size.xlsx') as writer:  
#     SC_size.to_excel(writer, sheet_name = 'robust2')
#     SC_size1.to_excel(writer, sheet_name = 'robustp5')
#     SC_size2.to_excel(writer, sheet_name='robustp5_add')    
    
    
 