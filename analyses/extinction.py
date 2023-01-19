'''
Calculate the extinction of the star clusters and see if the extinction from
the gas surface density will agree with that from optical data.  
'''

import pandas as pd
import math

###########################################################
# basic settings

D = 22

###########################################################
# main program

#############################
# import quantites

filename = 'tables/density.xlsx'
df = pd.read_excel(filename, sheet_name='star cluster, 0.5', index_col=0)
Sigma_gas = df['Sigma_gas_dust']; Sigma_gas_err = df['Sigma_gas_dust_err']

# import the source size
filename = 'tables/source_size2.xlsx'
df2 = pd.read_excel(filename, sheet_name='robustp5', index_col=0)
radius = df2['physical'] / 2
size = math.pi * radius**2

#############################
# calculate the extinction

# extinction from dust-derived gas surface density
Av = 0.0491 * Sigma_gas
Av_err = 0.0491 * Sigma_gas_err
Av_table = pd.concat([Av, Av_err], axis=1)

# Try to calculate the foreground extinction. 
## import the CO mass from moment 0 maps
df = pd.read_excel('tables/Derived.xlsx', sheet_name='star cluster')
Mgas_cluster = df['Mgas_CO_cube']
Mgas_tot = df['Mgas_CO_mom0']
M_foreground = Mgas_tot - Mgas_cluster


Sigma_gas_fore = M_foreground /size

Sigma_gas_gauss = (2e33*Sigma_gas_fore) / (3.1e18)**2
NH = Sigma_gas_gauss / (2/6e23)
Av_foreground = NH / (1.87e21)

### Try the GMC 
filename = 'tables/Derived.xlsx'
df = pd.read_excel(filename, sheet_name='GMC', index_col=0)
Mgas = df['Mgas_130K']

# import the aperture size
filename = 'flux_measure.xlsx'
df = pd.read_excel(filename, sheet_name='imfit')
major_pc = 4.85 * D * df['major (arcsec)']
minor_pc = 4.85 * D * df['minor (arcsec)']
size = 1.1331 * major_pc * minor_pc * 4

Sigma_gas = Mgas / size
Sigma_gas_gauss = (2e33*Sigma_gas) / (3.1e18)**2
NH = Sigma_gas_gauss / (2/6e23)
Av_GMC = NH / (1.87e21)