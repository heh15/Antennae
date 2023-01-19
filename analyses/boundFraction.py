'''
The concentration of free-free emission versus dust emission
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import math

#############################
# import antennae data
## import free-free emission
df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')

df['band3 flux (mJy)'][1] = np.nan
df['band 3 (high res, 0.5)'][8] = np.nan

flux_GMC = df['band3 flux (mJy)'].astype('float32')
flux_GMC_err = df['flux uncertainty'].astype('float32')

flux_SC = df['band 3 (high res, 0.5)'].astype('float32')
flux_SC[0] = flux_SC[0] + flux_SC[1].astype('float32')
ratio = flux_SC/ df['band3 flux (mJy)']

flux_SC_err = df['flux uncertainty.3']
flux_SC_err[0] = np.sqrt(flux_SC_err[0]**2 + flux_SC_err[1]**2)
ratio_err = ratio * np.sqrt((flux_SC_err/flux_SC)**2 + 
                            (flux_GMC_err/flux_GMC)**2)
uplims = np.full(np.shape(flux_SC), fill_value=False)
uplims[6] = True
xuplims = np.full(np.shape(flux_SC), fill_value=False)
xuplims[4] = True

## import the dust emission
SC_band7 = pd.read_excel('tables/flux_split.xlsx', sheet_name = 'star cluster 0.5')
GMC_band6 = pd.read_excel('tables/flux_split.xlsx', sheet_name = 'GMC')


flux_SC = SC_band7['dust_flux']; flux_SC_err = SC_band7['dust_err']
flux_SC[0] = flux_SC[0] + flux_SC[1]
flux_GMC = GMC_band6['dust_band7']; flux_GMC_err = GMC_band6['band7_err']
dust_ratio = flux_SC/flux_GMC
dust_ratio_err = dust_ratio * np.sqrt((flux_SC_err/flux_SC)**2 + 
                            (flux_GMC_err/flux_GMC)**2)

### import the GMC mass. 
mass_SC = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster, 0.5')
mass_GMC = pd.read_excel('tables/mass.xlsx', sheet_name='GMC')

SC_Mstar = mass_SC['Mstar']; SC_MstarErr = mass_SC['Mstar_err']
SC_Mgas = mass_SC['Mgas_Tco']; SC_Mgaserr = mass_SC['Mgas_Tco_err']
SC_Mtot = SC_Mstar + SC_Mgas 
SC_Mtoterr = mass_SC['Mstar_err'] + mass_SC['Mgas_Tco_err']

GMC_M = mass_GMC['Mgas_Tco']; GMC_Merr = mass_GMC['Mgas_Tco_err']

### calculate the GMC surface density 
df2 = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')
major_pc = 4.85*22*df2['major (arcsec)']
minor_pc = 4.85*22*df2['minor (arcsec)']
areas = 1.1331 * major_pc * minor_pc 
surf_GMC = GMC_M / areas
surf_err_GMC = GMC_Merr / GMC_M * surf_GMC

### calculate the mean gas surface density (Wilson+2000)
SGMC_names = ['1', '2', '3', '4', '5']
SGMC_areas = math.pi/4*np.array([1400, 1100, 1300, 1000, 800])**2
SGMC_mass = np.array([6.3, 3.9, 2.3, 3.7, 1.3])*1e8
SGMC_surf = SGMC_mass / SGMC_areas

surf_gas = np.full(np.shape(surf_GMC), np.nan)
surf_gas[0:2] = SGMC_surf[3]
surf_gas[5:8] = SGMC_surf[0]
surf_gas[2] = SGMC_surf[2]



#############################
# import other literature data

columns = ['CFE', 'CFE_err', 'Sig_gas', 'Sig_gas_err', 'ref']
CFE = pd.DataFrame(columns=columns)

## Adamo+2020
arr = pd.DataFrame(columns=columns)
arr['CFE'] = np.array([0.389, 0.484, 0.831, 0.998, 0.541, 0.623, 0.32, 0.36, 
                       0.592, 0.626, 0.414, 0.49, 0.698, 0.843, 0.408, 0.507])
arr['CFE_err'] = np.array([0.017, 0.03, 0.152, 0.158, 0.032, 0.042, 0.047, 
                           0.053, 0.066, 0.067, 0.038, 0.044, 0.049, 0.274, 
                           0.02, 0.026])
Sig_SFR = np.array([0.07, 0.26, 0.34, 1.54, 0.57, 1.52, 0.28, 0.49, 0.4, 0.62,
                    0.31, 0.95, 0.46, 3.59, 0.13, 0.23])
Sig_SFR_err = np.array([0.01, 0.02, 0.03, 0.15, 0.06, 0.15, 0.03, 0.05, 0.04,
                        0.06, 0.03, 0.09, 0.05, 0.36, 0.01, 0.02])
arr['Sig_gas'] = (Sig_SFR/2.5e-4)**(1/1.4)
arr['Sig_gas_err'] = 1.4 * Sig_SFR_err / Sig_SFR * arr['Sig_gas']
arr['ref'] = 'Adamo+2020'

CFE = CFE.append(arr, ignore_index=True)

## Kruijssen+2012
arr = pd.DataFrame(columns=columns)
arr['CFE'] = np.array([0.052, 0.05, 0.032, 0.139, 0.229, 0.01, 0.18, 0.162,
                       0.08, 0.125, 0.025, 0.50, 0.042, 0.058, 0.07])
arr['CFE_err'] = np.array([0.003, 0, 0.002, 0.008, 0.073, 0.006, 0, 0.047, 
                           0, 0.0025, 0.003, 0.13, 0.002, 0.005, 0.07])
arr['Sig_gas'] = 10**np.array([0.67, 0.93, 0.88, 1.33, 2.1, 0.59, 1.47, 1.7, 
                               1.09, 1.3, 0.84, 1.98, 0.96, 1.04, 0.97])
arr['Sig_gas_err'] = 0
arr['ref'] = 'Kruijssen+2012'

CFE = CFE.append(arr, ignore_index=True)

#############################
# plot the fraction versus the GMC mass 

# ratio[3,4,9] = np.nan
txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((GMC_M+0.05))
xtext[6] = xtext[6] / 1.2
ytext = np.array((0.02+ratio))
ytext[5] = ytext[5] -0.1
ytext1 = np.array((0.02+dust_ratio))
fig = plt.figure(figsize=(6, 6)) 
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')

plt.ylim([0.05,2])
# plt.xlim([1e6, 1e8])

plt.errorbar(GMC_M, ratio,
             xerr=GMC_Merr, yerr=ratio_err, uplims=uplims, xuplims=xuplims,
             fmt='o', color = 'tab:orange', markersize=12, label='free-free')
plt.errorbar(GMC_M, dust_ratio,
             xerr=GMC_Merr, yerr=dust_ratio_err, 
             fmt='o', color = 'tab:blue', markersize=12, label='dust emission')
for i, txt in enumerate(txts):
    ax.annotate(txt, (GMC_M[i], ratio[i]), 
                (xtext[i], ytext[i]), fontsize=20)
    ax.annotate(txt, (GMC_M[i], dust_ratio[i]), 
                (xtext[i], ytext1[i]), fontsize=20)

plt.plot([0, ax.get_xlim()[1]], [1, 1], color='black', linestyle='--')
plt.legend(fontsize=15, framealpha=0.5, loc='lower left')

ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, 
                                                    symbol='%', 
                                                    is_latex=False))
ax.set_xlabel(r'$M_{\mathrm{GMC}}$ (M$_{\odot}$)', fontsize=30)
ax.set_ylabel(r'YMC/GMC flux ratio', fontsize=30)
ax.tick_params(labelsize = 20)
plt.tight_layout()
plt.savefig('pictures/fraction.pdf')


#############################
# plot the fraction versus gas surface density

ratio[3,4] = np.nan
txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xdata = np.copy(surf_GMC)
ydata = np.copy(ratio)
ydata_err = np.copy(ratio_err)
xtext = np.array((surf_GMC/10**0.04))
ytext = np.array((ratio/10**0.04))
ytext[5] = ytext[5] * 1.2
xtext[0] = xtext[0] * 1.3
ytext[2] = ytext[2] / 1.3
xtext[6] = xtext[6] * 1.3
xtext[7] = xtext[7] * 1.3
ytext[7] = ytext[7] / 1.1
xtext[9] = xtext[9] * 1.1
ytext[9] = ytext[9] * 1.2
# ytext[5] = ytext[5] -0.1
fig = plt.figure(figsize=(6, 6)) 
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.xlim([1,1.5e4])
plt.plot([0, ax.get_xlim()[1]], [1, 1], color='black', linestyle='--')
plt.ylim([0.01,2])

plt.errorbar(xdata, ydata,
#             xerr=surf_err_GMC, 
             yerr=ydata_err, uplims=uplims,
             fmt='o', color = 'tab:orange', markersize=12,
             label='This work')
for i, txt in enumerate(txts):
    ax.annotate(txt, (xdata[i], ydata[i]), 
                (xtext[i], ytext[i]), fontsize=20)

# plot the bound fraction for literature data
colors = ['blue', 'red']
for i, ref in enumerate(pd.unique(CFE['ref'])):
    CFE_sin = CFE.loc[CFE['ref'] == ref]
    plt.errorbar(CFE_sin['Sig_gas'], CFE_sin['CFE'], xerr=CFE_sin['Sig_gas_err'], 
                 yerr=CFE_sin['CFE_err'], fmt='.', color=colors[i], label=ref)

# plot the theoretical bound fraction based on Kruijssen+2012
Sigma_theory = 10**np.arange(0, 4.6, 0.1)
Sigma_SFR = 2.5e-4*Sigma_theory**1.4
Gamma = (1.15 + 0.6*Sigma_SFR**(-0.4)+0.05*Sigma_SFR**-1)**-1

plt.plot(Sigma_theory, Gamma, color='black')
plt.legend(fontsize=15, framealpha=0.5)

ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, 
                                                    symbol='%', 
                                                    is_latex=False))
ax.set_xlabel(r'$\Sigma_{\mathrm{GMC}}$ (M$_{\odot}$ pc$^{-2}$)', fontsize=30)
ax.set_ylabel(r'CFE', fontsize=30)
ax.tick_params(labelsize = 20)
plt.tight_layout()
plt.savefig('pictures/fraction_surfgas.pdf')