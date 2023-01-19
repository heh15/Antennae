import pandas as pd
import math
import numpy as np

###########################################################
# basic settings

D = 22
k = 1.38e-23
G = 6.67e-11

###########################################################
# main program


## Calculate the ionized photon density for antennae galaxy
df = pd.read_excel('tables/Derived.xlsx', sheet_name='star cluster', 
                   index_col=0)
Qphoton = df['Q0']
df2 = pd.read_excel('tables/source_size.xlsx', sheet_name='robustp5')
rs = df2['physical'] / 2.0

Mion = 684 * (Qphoton/1e51)**0.5 * rs**1.5
nion = 4850 * (Qphoton/1e51)**0.5 * rs**(-1.5)

df_add = pd.read_excel('tables/Mstar.xlsx', sheet_name='robust0.5, 0.09', 
                       index_col=0)
Q0_add = df_add['Q0']
df_add2 = pd.read_excel('tables/source_size.xlsx', sheet_name='robustp5_add', 
                        index_col=0)
rs_add = df_add2['physical'] / 2.0

Mion_add = 684 * (Q0_add/1e51)**0.5 * rs_add**1.5
nion_add = 4850 * (Q0_add/1e51)**0.5 * rs_add**(-1.5)


# Compare the gas density with ionized photon density for Leroy+2018
filename='tables/NGC253_ascii.txt'
Leroy_table1 = pd.read_csv(filename, skiprows=6, header=None, skipfooter=2, 
                           sep='\t',index_col=0)
filename='tables/NGC253II_ascii.txt'
Leroy_table2 = pd.read_csv(filename, skiprows=6, header=None, skipfooter=4,
                           sep='\t', index_col=0)
Mgas = Leroy_table2[2]
Mstar = Leroy_table2[3]
Mtot = Mgas + Mstar

rho_gas = 10**Leroy_table2[5] * Mgas /  Mtot
n_gas = rho_gas * 2e33 / (3.1e18)**3 * 3e23 

# export it to the density.xlsx
density = pd.read_excel('tables/density.xlsx')
density['n_ion (per cc)'] = nion

with pd.ExcelWriter('tables/density.xlsx') as writer:  
    density.to_excel(writer)

