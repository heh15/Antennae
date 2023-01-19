import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


###########################################################
# functions

###########################################################

# read the flux from robust 2
flux_standard = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')
flux_splitted1 = pd.read_excel('tables/flux_split.xlsx', sheet_name='star cluster')
flux_splitted2 = pd.read_excel('tables/flux_split.xlsx', sheet_name= 'star cluster 0.5')


Band3_flux = flux_standard['band 3 (high res)']
Band3_uncertainty = flux_standard['flux uncertainty.1']

Band3_flux[8] = np.nan

Band7_flux = flux_standard['band 7 (high res)']
Band7_uncertainty = flux_standard['flux uncertainty.2']

# read the flux from robust 0.5
flux_check = pd.read_excel('flux_measure.xlsx', sheet_name='flux_check')
Band3_flux1 = flux_check['band3 (robust 0.5, 0.11)']
Band3_uncertainty1 = flux_check['flux uncertainty']

Band7_flux1 = flux_check['band7 (robust 0.5)']
Band7_uncertainty1 = flux_check['flux uncertainty.2']

# flux measured from large apertures to robust 0.5 images
Band3_flux2 = flux_standard['band 3 (high res, 0.5)']
Band3_uncertainty2 = flux_standard['flux uncertainty.3']

Band7_flux2 = flux_standard['band 7 (high res, 0.5)']
Band7_uncertainty2 = flux_standard['flux uncertainty.4']

# average intensity for the band 7
major = flux_standard['major (arcsec).1']; minor = flux_standard['minor (arcsec).1']
Band7_intensity = Band7_flux / (1.1331*major*minor) * 0.134**2
Band7_I_uncertainty = Band7_uncertainty / (1.1331*major*minor/0.134**2)
Band7_K = Band7_intensity / (0.0109 * 0.134**2 * (345/115.27)**2)
Band7_K_err = Band7_I_uncertainty / (0.0109 * 0.134**2 * (345/115.27)**2)

dust_flux = flux_splitted1['dust_flux']; dust_err = flux_splitted1['dust_err']
dust_intensity = dust_flux / (1.1331*major*minor) * 0.134**2
dust_I_uncertainty = dust_err / (1.1331*major*minor/0.134**2)
dust_K = dust_intensity / (0.0109 * 0.134**2 * (345/115.27)**2)
dust_K_err = dust_I_uncertainty / (0.0109 * 0.134**2 * (345/115.27)**2)

major = flux_standard['major']; minor = flux_standard['minor']
Band7_intensity2 = Band7_flux2 / (1.1331*major*minor) * 0.11**2
Band7_I_uncertainty2 = Band7_uncertainty2 / (1.1331*major*minor/0.11**2)
Band7_K2 = Band7_intensity2 / (0.0109 * 0.11**2 * (345/115.27)**2)
Band7_K_err2 = Band7_I_uncertainty2 / (0.0109 * 0.11**2 * (345/115.27)**2)

dust_flux2 = flux_splitted2['dust_flux']; dust_err2 = flux_splitted2['dust_err']
dust_intensity2 = dust_flux2 / (1.1331*major*minor) * 0.11**2
dust_I_uncertainty2 = dust_err2 / (1.1331*major*minor/0.11**2)
dust_K2 = dust_intensity2 / (0.0109 * 0.11**2 * (345/115.27)**2)
dust_K_err2 = dust_I_uncertainty2 / (0.0109 * 0.11**2 * (345/115.27)**2)

### comparison between fluxes for band 3  
txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((Band3_flux+0.02))
ytext = np.array((Band3_flux1+0.02))
ytext[7] = ytext[7] - 0.03

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(Band3_flux, Band3_flux1, xerr=Band3_uncertainty, 
             yerr=Band3_uncertainty1, linestyle='', marker='.',
             label='large aperture')
plt.errorbar(Band3_flux, Band3_flux2, xerr=Band3_uncertainty, 
             yerr=Band3_uncertainty2, linestyle='', marker='.', 
             label='small aperture')
plt.legend(fontsize=20)
plt.plot([0, ax.get_xlim()[1]], [0, ax.get_xlim()[1]], color='black', 
         linestyle='--')
plt.plot([0, ax.get_ylim()[1]], [0, 0.7*ax.get_ylim()[1]], color='black', 
         linestyle='--')
plt.plot([0, ax.get_ylim()[1]], [0, 0.5*ax.get_ylim()[1]], color='black', 
         linestyle='--')
plt.annotate('1.0', (0.035, 0.035), (0.035, 0.035*1.2), fontsize=17)
plt.annotate('0.7', (0.035, 0.035*0.7), (0.035, 0.035*0.7*1.2), fontsize=17)
plt.annotate('0.5', (0.035, 0.035*0.5), (0.035, 0.035*0.5*1.2), fontsize=17)
for i, txt in enumerate(txts):
    plt.annotate(txt, (Band3_flux[i], Band3_flux1[i]), 
                (xtext[i], ytext[i]), fontsize=17)
plt.xlabel('band 3 robust 2 flux (mJy)', fontsize=30)
plt.ylabel('band 3 robust 0.5 flux (mJy)', fontsize=30)
plt.tick_params(labelsize=20)
fig.tight_layout()
plt.savefig('pictures/Band3_robust_test.pdf')

### comparison between fluxes for band 7
txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((Band7_flux+0.02))
ytext = np.array((Band7_flux1+0.02))
ytext[7] = ytext[7] - 0.03

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(Band7_flux, Band7_flux1, xerr=Band7_uncertainty, 
             yerr=Band7_uncertainty1, linestyle='', marker='.',
             label='large aperture')
plt.errorbar(Band7_flux, Band7_flux2, xerr=Band7_uncertainty, 
             yerr=Band7_uncertainty2, linestyle='', marker='.', 
             label='small aperture')
plt.legend(fontsize=20)
plt.plot([0, ax.get_xlim()[1]], [0, ax.get_xlim()[1]], color='black', 
          linestyle='--')
plt.plot([0, ax.get_ylim()[1]], [0, 0.7*ax.get_ylim()[1]], color='black', 
          linestyle='--')
plt.plot([0, ax.get_ylim()[1]], [0, 0.5*ax.get_ylim()[1]], color='black', 
          linestyle='--')
plt.annotate('1.0', (0.55, 0.55), (0.55, 0.55*1.1), fontsize=17)
plt.annotate('0.7', (0.55, 0.55*0.55), (0.55, 0.55*0.7*1.1), fontsize=17)
plt.annotate('0.5', (0.55, 0.55*0.5), (0.55, 0.55*0.5*1.1), fontsize=17)
for i, txt in enumerate(txts):
    plt.annotate(txt, (Band7_flux[i], Band7_flux1[i]), 
                (xtext[i], ytext[i]), fontsize=17)
plt.xlabel('band 7 robust 2 flux (mJy)', fontsize=30)
plt.ylabel('band 7 robust 0.5 flux (mJy)', fontsize=30)
plt.tick_params(labelsize=20)
fig.tight_layout()
plt.savefig('pictures/Band7_robust_test.pdf')

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((dust_K*1.05))
ytext = np.array((dust_K2*1.05))
ytext[7] = ytext[7] - 0.03

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(dust_K, dust_K2, xerr=dust_K_err, 
             yerr=dust_K_err2, linestyle='', marker='.',
             label='large aperture')
plt.plot([0, ax.get_xlim()[1]], [0, ax.get_xlim()[1]], color='black', 
          linestyle='--')
for i, txt in enumerate(txts):
    plt.annotate(txt, (dust_K[i], dust_K2[i]), 
                (xtext[i], ytext[i]), fontsize=17)
plt.xlabel('Robust 2 Dust T$_B$ (K)', fontsize=30)
plt.ylabel('Robust 0.5 Dust T$_B$ (K)', fontsize=30)
plt.tick_params(labelsize=20)
fig.tight_layout()
plt.savefig('pictures/Dust_intensity.pdf')