import pandas as pd
import math
import numpy as np

### calculate the surface density of the gas from the gas mass from dust and 
# gas mass from CO maps

'''
The density can be used to:
1) Calculate efficiency per-freefall time
2) Compare with number density of ionized ions
3) calculate the dust optical depth
'''

#############################
# import the data
# Get the mass of gas from Derived.xlsx
SC =  pd.read_excel('tables/mass.xlsx', sheet_name='star cluster, 0.5')
Mgas_dust = SC['Mgas_Tco']; Mgas_dust_err = SC['Mgas_Tco_err']
Mgas_CO = SC['Mgas_CO_cube']
Mstar = SC['Mstar']; Mstar_err = SC['Mstar_err']
Mtot = Mstar + Mgas_dust
Mtot_err = np.sqrt(Mstar_err**2+Mgas_dust_err**2) 

# Get the density for GMCs
GMC = pd.read_excel('tables/mass.xlsx', sheet_name='GMC')

# get the aperture size for GMCs
GMC2 = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')

#############################
# calculate densities for star clusters

# create a dataframe table
density = pd.DataFrame(index=SC.index)

# Get the radius from source_size.xlsx
FWHM = pd.read_excel('tables/source_size2.xlsx', sheet_name='robustp5')
radius = FWHM['physical'] / 2.0
radius_err = FWHM['physical_err'] / 2.0
size = math.pi * (radius)**2

# calculate the total surface density
Sigma_tot = Mtot / size
Sigma_tot_err = np.sqrt((Mtot_err/Mtot)**2+(2*radius_err/radius)**2) *Sigma_tot

density['Sigma_tot'] = Sigma_tot
density['Sigma_tot_err'] = Sigma_tot_err

# calculate the surface density
Sigma_gas_dust = Mgas_dust / size
Sigma_gas_dust_err = Sigma_gas_dust *\
            np.sqrt((Mgas_dust_err/Mgas_dust)**2+(2*radius_err/radius)**2)
Sigma_gas_co = Mgas_CO / size

density['Sigma_gas_dust'] = Sigma_gas_dust
density['Sigma_gas_dust_err'] = Sigma_gas_dust_err
density['Sigma_gas_co'] = Sigma_gas_co

# calculate the number density
rho_gas_dust = Sigma_gas_dust / (2*radius)
rho_gas_co = Sigma_gas_co / (2*radius)

density['rho_gas_dust (solar mass/pc^2)'] = rho_gas_dust
density['rho_gas_co (solar mass/pc^2)'] = rho_gas_co

n_gas_dust = rho_gas_dust * 2e33 / (3.1e18)**3 * 3e23
n_gas_co = rho_gas_co * 2e33 / (3.1e18)**3 * 3e23

density['n_gas_dust (per cc)'] = n_gas_dust
density['n_gas_co (solar mass/pc^2)'] = n_gas_co

    
#############################
# calculate density for GMCs

# import the gas mass
Mgas_dust = GMC['Mgas_Tco']; Mgas_dust_err = GMC['Mgas_Tco_err']

# import aperture area
major = GMC2['major (arcsec)']
minor = GMC2['minor (arcsec)']
major_pc = 4.85 * 22 * major
minor_pc = 4.85 * 22 * minor
areas = 1.1331 * major_pc * minor_pc

density_GMCs = pd.DataFrame(index=GMC.index)
density_GMCs['Sigma_gas_dust'] = Mgas_dust / areas
density_GMCs['Sigma_gas_dust_err'] = Mgas_dust_err / areas


#############################
# export the table

# export results into density.xlsx
with pd.ExcelWriter('tables/density.xlsx') as writer:  
    density.to_excel(writer, sheet_name='star cluster, 0.5')
    density_GMCs.to_excel(writer, sheet_name='GMC')

# show density 
print(np.log10(Sigma_tot))
print(0.434* (Sigma_tot_err/Sigma_tot))

# show the gas surface density for GMCs
GMC_dens_log = np.log10(density_GMCs['Sigma_gas_dust'])
GMC_denserr_log = 0.434* (density_GMCs['Sigma_gas_dust_err']/
                          density_GMCs['Sigma_gas_dust'])
print(pd.concat([GMC_dens_log, GMC_denserr_log], axis=1))