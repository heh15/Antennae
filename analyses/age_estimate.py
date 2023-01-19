import math
import pandas as pd
import numpy as np

# age estimate for star clusters

d_Mpc = 22
freq_GHz = 100
sigma = 5.6e-8

# There are 13 radio objects. Exclude two nucleus and one source near the nucleus, 
# we have 10 sources. 

age = 16e6
age_young = 16e6 * 10 / 150

# set the sensitivity limit using GMC data
# assuming 80% of flux comes from star cluster. 

GMC_sensitivity = 1.2e-5
threshold = 6e-5
flux_low = 6e-5 * 0.8

# calculate the ionized phton (Murphy+11)
L_low = (flux_low*1e-23) * 4 * math.pi * (d_Mpc*1e6*3.1e18)**2
Q_low = 6.3e25 * 100**0.1 * L_low
# calculate the mass (Leroy+18)
M_low = Q_low / (4e46)

### Calculate the number of optical clusters with mass above that value
M_low = 7.2e4
N_optical =  (1e4/M_low-0.01) / (1-0.01) * 1600
print('Number of Optical Clusters: '+str(N_optical))
N_radio = 17
age = N_radio / N_optical * 16
print('Age: '+str(age)+' Myr')

### age estimate for individual star cluster. (Rico-Villas+2019)
## assuming temperature to be 150 K
sizes = pd.read_excel('tables/source_size.xlsx', sheet_name='robustp5')
FWHMs_pc = sizes['physical']
r = FWHMs_pc / 2

T = 40
Lapp = 4 * math.pi * sigma * T**4 * (3.1e16*r)**2 / 3.8e26
Lp = 0.1 * Lapp
# Lp is the upper limit

# assuming the light/mass ratio to be 1000
Mass = pd.read_excel('tables/Derived.xlsx', sheet_name='star cluster')
M_star =  Mass['Mstar']
L_star = 1000*M_star

L_ratio = Lp / L_star
# The ratios are all much greater than 0.05, suggest they are young clusters
# However, Lp is the upper limit of the cluster.
ages = 1 / (1+L_ratio) * 10**5
ages[L_ratio < 0.05] = 10**5

### Divide the efficiency by efficiency per free-fall time
SC_band7 = pd.read_excel('tables/Derived.xlsx', sheet_name = 'star cluster')
Mstar = SC_band7['Mstar']
Mgas = SC_band7['Mgas_CO_cube']

effs = Mstar / (Mstar+Mgas)
ages_eff = effs / 0.1 * 10**5


