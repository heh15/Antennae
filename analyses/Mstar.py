import pandas as pd
import math
import numpy as np
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


#############################################################################
# main program

statistics_SC = ['Q0', 'Mstar', 'Mstar_err']

### Calculate the stellar mass for star cluster data
# The image parameter, robust 0.5, 0.09 arcsec resolution

# import and preprocess data
df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit_add')
SC_properties = pd.DataFrame(columns=statistics_SC)

# Murphy et al. 2011 & Leroy et al. 2018
L_100GHz_std = df['flux, rob0.5, 0.09']*1e-29*4*math.pi*D**2
L_100GHz_erg = L_100GHz_std*1e7
Q_photon = 6.3*10**25*freq_band3**0.1*L_100GHz_erg
SC_properties['Q0'] = Q_photon / 0.5
SC_properties['Mstar'] = Q_photon/(4e46) / 0.5
SC_properties['Mstar_err'] = SC_properties['Mstar']*\
    df['uncertainty']/df['flux, rob0.5, 0.09'] / 0.5

indexes = SC_properties.index.values
for x in indexes:
    if np.isnan(SC_properties['Mstar_err'][x]) == False:
        SC_properties['Mstar_err'][x] = \
            round_sig(SC_properties['Mstar_err'][x], sig=1)

SC_properties.index = df['source']
        
with pd.ExcelWriter('tables/Mstar.xlsx') as writer:  
    SC_properties.to_excel(writer, sheet_name = 'robust0.5, 0.09')

    