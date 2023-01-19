import pandas as pd
import numpy as np
import math
from math import log10, floor
import matplotlib.pyplot as plt

###########################################################
# basic parameters

freq_band3 = 100
freq_band6 = 220
freq_band7 = 340

freq_co21 = 230

co2_1_ratio = 0.7

D_Mpc = 22
D = D_Mpc*1e6*3.1e16
beta = 1.5
z = 0.0055

kappa_345 = 0.9
###########################################################
# functions

def round_sig(x, sig=2):
    '''
    round the x to certain significant figures
    '''
    return round(x, sig-int(floor(log10(abs(x))))-1)


def Mstar_calc(fluxes, fluxes_err):
    L_100GHz_std = fluxes * 1e-29 * 4 * math.pi * D**2
    L_100GHz_erg = L_100GHz_std * 1e7
    Q_photon = 6.3*10**25*freq_band3**0.1*L_100GHz_erg
    Mstar = Q_photon / (4e46)
    Mstar_err = Mstar * fluxes_err / fluxes
    frame = {'Q0': Q_photon, 'Mstar': Mstar, 'Mstar_err': Mstar_err}
    Mstar_table = pd.DataFrame(frame)
    
    return Mstar_table

def Mgas_dust_calc(fluxes, fluxes_err, T, T_err=0):
    mass_dust = 74220 * fluxes / 1000 * D_Mpc**2 * np.exp(17.0/T)/kappa_345
    flux_relerr =  fluxes_err / fluxes
    T_relerr = (np.exp(17/(T-T_err)) - np.exp(17/T)) / (np.exp(17/T))
    mass_relerr = np.sqrt(flux_relerr**2 + T_relerr**2)
    mass_dust_err = mass_dust * mass_relerr
    mass_gas = mass_dust * 120
    mass_gas_err = mass_dust_err * 120
    frame = {'Mdust': mass_dust, 'Mdust_err': mass_dust_err, 
             'Mgas': mass_gas, 'Mgas_err': mass_gas_err}    
    Mgas_table = pd.DataFrame(frame)
    
    return Mgas_table

def Mgas_CO_calc(fluxes, fluxes_err):
    mass_gas = fluxes / (4*co2_1_ratio) * 1.05e4* D_Mpc**2 / (1+z)
    mass_gas_err = mass_gas * fluxes_err / fluxes
    frame = {'Mgas': mass_gas, 'Mgas_err': mass_gas_err}
    Mgas_table = pd.DataFrame(frame)
    
    return Mgas_table

###########################################################
# main program

### import the flux measurements


statistics = ['Q0','Mstar', 'Mstar_err', 'Mdust_130K', 
                 'Mdust_60K', 'Mdust_160K', 'Mgas_130K','Mgas_60K', 
                 'Mgas_160K', 'Mgas_err', 'Mgas_CO_mom0', 
                 'Mgas_CO_err_mom0', 'Mgas_CO_cube', 'Mgas_CO_err_cube']

# read the data from 'flux_measure.xlsx' and 'flux_split.xlsx'
df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')
df_add = pd.read_excel('flux_measure.xlsx', sheet_name='imfit_add')
df_line = pd.read_excel('flux_measure.xlsx', sheet_name='line')
df_line_add = pd.read_excel('flux_measure.xlsx', sheet_name='line_add')
df_GMC_Tkin = pd.read_excel('flux_measure.xlsx', sheet_name='line_GMC')

# preprocessing for the data table
df['band3 flux (mJy)'][1] = np.nan
df['band 3 (high res)'][8] = np.nan
df['band 7 (high res)'][3:5] = np.nan
df['band 7 (high res)'][8] = np.nan
# df['band 7 (high res)'][9] = np.nan

# create tables
mass_SC = pd.DataFrame(index=df.index)
mass_SC_p5 = pd.DataFrame(index=df.index)
mass_GMC = pd.DataFrame(index=df.index)
mass_SC_add = pd.DataFrame(index=df_line_add.index)

### Calculate the stellar mass for star cluster data.
# Murphy et al. 2011 & Leroy et al. 2018

# mass for robust 2 image
fluxes = df['band 3 (high res)']; fluxes_err = df['flux uncertainty.1']
Mstar_table = Mstar_calc(fluxes, fluxes_err)
mass_SC = pd.concat([mass_SC, Mstar_table], axis=1)

# mass for robust 0.5 image
fluxes = df['band 3 (high res, 0.5)']; fluxes_err = df['flux uncertainty.3']
Mstar_table = Mstar_calc(fluxes, fluxes_err)
mass_SC_p5 = pd.concat([mass_SC_p5, Mstar_table], axis=1)

# mass for substructures
fluxes = 2*df_add['flux, rob0.5, 0.09']; fluxes_err = 2*df_add['uncertainty']
Mstar_table = Mstar_calc(fluxes, fluxes_err)
mass_SC_add = pd.concat([mass_SC_add, Mstar_table], axis=1)

# mass for GMCs
fluxes = df['band3 flux (mJy)']; fluxes_err = df['flux uncertainty']
Mstar_table = Mstar_calc(fluxes, fluxes_err)
mass_GMC = pd.concat([mass_GMC, Mstar_table], axis=1)

# round the error
indexes = mass_SC.index.values
for x in indexes:
    if np.isnan(mass_SC['Mstar_err'][x]) == False:
        mass_SC['Mstar_err'][x] = round_sig(mass_SC['Mstar_err'][x], sig=1)
        mass_SC_p5['Mstar_err'][x] = round_sig(mass_SC_p5['Mstar_err'][x], 
                                               sig=1)

### Calculate the dust mass and gas mass 

# imported the splitted dust flux
df1 = pd.read_excel('tables/flux_split.xlsx', sheet_name='star cluster')
df2 = pd.read_excel('tables/flux_split.xlsx', sheet_name='star cluster 0.5')
df3= pd.read_excel('tables/flux_split.xlsx', sheet_name='SC, add')

fluxes1 = df1['dust_flux']; fluxes1_err = df1['dust_err']
fluxes2 = df2['dust_flux']; fluxes2_err = df2['dust_err']
fluxes3 = 2 * df3['dust_flux']; fluxes3_err = 2 * df3['dust_err']
 
## dust mass and gas mass for star clusters 
# Finn et al. 2019; Wilson et al. 2008
# Dust temperature constraint 60 - 160 K, from Leroy+2018

T = 130
Mgas_table = Mgas_dust_calc(fluxes1, fluxes1_err, T, T_err=0)
mass_SC['Mgas_130K'] = Mgas_table['Mgas']
mass_SC['Mgas_130K_err'] = Mgas_table['Mgas_err']
Mgas_table = Mgas_dust_calc(fluxes2, fluxes2_err, T, T_err=0)
mass_SC_p5['Mgas_130K'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_130K_err'] = Mgas_table['Mgas_err']

T = 60
Mgas_table = Mgas_dust_calc(fluxes1, fluxes1_err, T, T_err=0)
mass_SC['Mgas_60K'] = Mgas_table['Mgas']
mass_SC['Mgas_60K_err'] = Mgas_table['Mgas_err']
Mgas_table = Mgas_dust_calc(fluxes2, fluxes2_err, T, T_err=0)
mass_SC_p5['Mgas_60K'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_60K_err'] = Mgas_table['Mgas_err']

T = 160
Mgas_table = Mgas_dust_calc(fluxes1, fluxes1_err, T, T_err=0)
mass_SC['Mgas_160K'] = Mgas_table['Mgas']
mass_SC['Mgas_160K_err'] = Mgas_table['Mgas_err']
Mgas_table = Mgas_dust_calc(fluxes2, fluxes2_err, T, T_err=0)
mass_SC_p5['Mgas_160K'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_160K_err'] = Mgas_table['Mgas_err']

T = 40
Mgas_table = Mgas_dust_calc(fluxes1, fluxes1_err, T, T_err=0)
mass_SC['Mgas_40K'] = Mgas_table['Mgas']
mass_SC['Mgas_40K_err'] = Mgas_table['Mgas_err']
Mgas_table = Mgas_dust_calc(fluxes2, fluxes2_err, T, T_err=0)
mass_SC_p5['Mgas_40K'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_40K_err'] = Mgas_table['Mgas_err']

lineMeasurement = pd.read_excel('flux_measure.xlsx', sheet_name='line')
T = lineMeasurement['Tkin']
Mgas_table = Mgas_dust_calc(fluxes1, fluxes1_err, T, T_err=0)
mass_SC['Mgas_Tco'] = Mgas_table['Mgas']
mass_SC['Mgas_Tco_err'] = Mgas_table['Mgas_err']
Mgas_table = Mgas_dust_calc(fluxes2, fluxes2_err, T, T_err=0)
mass_SC_p5['Mgas_Tco'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_Tco_err'] = Mgas_table['Mgas_err']

# gas mass for substructures
lineMeasurement = pd.read_excel('flux_measure.xlsx', sheet_name='line_add')
T = lineMeasurement['Tkin']
Mgas_table = Mgas_dust_calc(fluxes3, fluxes3_err, T, T_err=0)
mass_SC_add['Mgas_Tco'] = Mgas_table['Mgas']
mass_SC_add['Mgas_Tco_err'] = Mgas_table['Mgas_err']

# dust mass and gas mass for GMC
T = 20
df3 = pd.read_excel('tables/flux_split.xlsx', sheet_name='GMC')
fluxes = df3['dust_band7']; fluxes_err = df3['band7_err']
Mgas_table = Mgas_dust_calc(fluxes, fluxes_err, T, T_err=0)
mass_GMC['Mgas_20K'] = Mgas_table['Mgas']
mass_GMC['Mgas_20_err'] = Mgas_table['Mgas_err']

# dust mass and gas mass for GMC with CO temperataure
Tkin = df_GMC_Tkin['Tkin']
Tkin_err = df_GMC_Tkin['Tkin_err']
Mgas_table = Mgas_dust_calc(fluxes, fluxes_err, Tkin, T_err=Tkin_err)
mass_GMC['Mdust_Tco'] = Mgas_table['Mdust']
mass_GMC['Mdust_Tco_err'] = Mgas_table['Mdust_err']
mass_GMC['Mgas_Tco'] = Mgas_table['Mgas']
mass_GMC['Mgas_Tco_err'] = Mgas_table['Mgas_err']

### Calculate the CO mass

# CO mass measured from cubes
fluxes = df_line['co21 pbcor cube']; fluxes_err = df_line['uncertainty']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC['Mgas_CO_cube'] = Mgas_table['Mgas']
mass_SC['Mgas_CO_cube_err'] = Mgas_table['Mgas_err']

fluxes = df_line['co21 pbcor cube, 0.5']
fluxes_err = df_line['uncertainty.2']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC_p5['Mgas_CO_cube'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_CO_cube_err'] = Mgas_table['Mgas_err']

# CO mass from moment 0 maps
fluxes = df_line['co21 pbcor mom0']; fluxes_err = df_line['uncertainty.1']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC['Mgas_CO_mom0'] = Mgas_table['Mgas']
mass_SC['Mgas_CO_mom0_err'] = Mgas_table['Mgas_err']

fluxes = df_line['co21 pbcor mom0, 0.5']
fluxes_err = df_line['uncertainty.3']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC_p5['Mgas_CO_mom0'] = Mgas_table['Mgas']
mass_SC_p5['Mgas_CO_mom0_err'] = Mgas_table['Mgas_err']

## CO mass for additional apertures. 

# CO mass measured from cubes
fluxes = 2 * df_line_add['co21 pbcor cube']
fluxes_err = 2 * df_line_add['uncertainty.2']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC_add['Mgas_CO_cube'] = Mgas_table['Mgas']
mass_SC_add['Mgas_CO_cube_err'] = Mgas_table['Mgas_err']

fluxes = 2 * df_line_add['co21 pbcor mom0']
fluxes_err = 2* df_line_add['uncertainty.3']
Mgas_table = Mgas_CO_calc(fluxes, fluxes_err)
mass_SC_add['Mgas_CO_mom0'] = Mgas_table['Mgas']
mass_SC_add['Mgas_CO_mom0_err'] = Mgas_table['Mgas_err']


mass_SC_add.index = df_line_add['source']

print(np.log10(mass_SC_p5['Mgas_Tco']/120))
print(1/np.log(10)*mass_SC_p5['Mstar_err']/mass_SC_p5['Mstar'])
print(1/np.log(10)*mass_SC_p5['Mgas_Tco_err']/mass_SC_p5['Mgas_Tco'])

### save the table. 
with pd.ExcelWriter('tables/mass.xlsx') as writer:  
    mass_SC.to_excel(writer, sheet_name='star cluster')
    mass_SC_p5.to_excel(writer, sheet_name='star cluster, 0.5')
    mass_SC_add.to_excel(writer, sheet_name='star cluster, add')
    mass_GMC.to_excel(writer, sheet_name='GMC')
    
    
# show the GMC mass 
print(np.log10(mass_GMC['Mdust_Tco']))
print(0.434*mass_GMC['Mdust_Tco_err']/mass_GMC['Mdust_Tco'])
print(np.log10(mass_GMC['Mgas_Tco']))
print(0.434*mass_GMC['Mgas_Tco_err']/mass_GMC['Mgas_Tco']) 
