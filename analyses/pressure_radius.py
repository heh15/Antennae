'''
Try the pressure balance to see what radius it gives me
Turbulent pressure = (thermal ionized gas pressure+radiation pressure)
'''

import pandas as pd
import numpy as np
import math

###########################################################
# basic parameters
mh = 1.67e-24 # in g
c = 3e10 # in cm 

pc_cm = 3.1e18
Msun_g = 2e33
Msun_Lsun = 1100
Lsun_erg = 3.8e33
k_boltz = 1.38e-16

###########################################################
# main program

# the pressure from table 
pressure_cluster = 10**np.array([9.0, 8.8, 8.0, 7.7, 8.4,8.9])
M_star = 10**np.array([6.2, 6.0, 5.8, 5.7, 5.1, 5.5])
M_gas = 10**np.array([5.4, 6.8, 6.4, 6.7, 6.3, 6.3])
M_tot = M_star + M_gas
T = np.array([40, 53, 42, 48, 48, 38])
Rh = np.array([4.8, 6.9, 9.0, 14, 7.5, 3.6])

Sigma_tot = 10**np.array([4.4, 4.7, 4.1, 3.9, 4.1, 4.7])

# Calculate the pressure of ionizing photons
# M/(mh*4/3*pi*r**3)*k*T
coeff1 = M_tot*Msun_g / (mh*4/3*math.pi*pc_cm**3) * T
pressure_ion = coeff1 / Rh**3

# Calculate the radiation pressure
# Ksai * M / (4*pi*r**2)  / c
coeff2 = 2* M_star*Msun_Lsun*Lsun_erg / (4*math.pi*pc_cm**2) / c / k_boltz
pressure_rad = coeff2 / Rh**2