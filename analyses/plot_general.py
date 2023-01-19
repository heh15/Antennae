import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import rsmf
# formatter = rsmf.setup(r"\documentclass[a4paper,12pt,noarxiv]{quantumarticle}")

df = pd.read_excel('flux_measure.xlsx', sheet_name='imfit')

df['band3 flux (mJy)'][1] = np.nan
df['band 3 (high res)'][8] = np.nan

flux_GMC = df['band3 flux (mJy)'].astype('float32')
flux_GMC_err = df['flux uncertainty'].astype('float32')

flux_SC = df['band 3 (high res)'].astype('float32')
flux_SC[0] = flux_SC[0] + flux_SC[1].astype('float32')
ratio = flux_SC/ df['band3 flux (mJy)']

flux_SC_err = df['flux uncertainty.1']
flux_SC_err[0] = np.sqrt(flux_SC_err[0]**2 + flux_SC_err[1]**2)
ratio_err = ratio * np.sqrt((flux_SC_err/flux_SC)**2 + 
                            (flux_GMC_err/flux_GMC)**2)

# ratio[3,4,9] = np.nan
# txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
#         '11', '12','13']
# xtext = np.array((flux_GMC+0.05))
# ytext = np.array((0.02+ratio))
# ytext[5] = ytext[5] -0.1
# fig = plt.figure(figsize=(10, 10)) 
# ax = plt.subplot(111)
# plt.xscale('log')
# plt.yscale('log')
# plt.errorbar(flux_GMC, ratio,
#              xerr=flux_GMC_err, yerr=ratio_err, 
#              fmt='o', color = 'tab:blue', markersize=12)
# for i, txt in enumerate(txts):
#     ax.annotate(txt, (flux_GMC[i], ratio[i]), 
#                 (xtext[i], ytext[i]), fontsize=12)
# plt.plot([0, ax.get_xlim()[1]], [1, 1], color='black', linestyle='--')
# plt.xlabel(r'$F_{\mathrm{100GHz, GMC}}$ (mJy)', fontsize=30)
# plt.ylabel(r'$F_{\mathrm{100GHz, SC}}/F_{\mathrm{100GHz, GMC}}$ (mJy)', fontsize=30)
# plt.tick_params(labelsize = 20)
# plt.tight_layout()
# plt.savefig('pictures/fraction.pdf')

### plot the fraction of dust emission
SC_band7 = pd.read_excel('tables/Derived.xlsx', sheet_name = 'star cluster')
GMC_band6 = pd.read_excel('tables/Derived.xlsx', sheet_name = 'GMC')

flux_SC = SC_band7['dust_flux']; flux_SC_err = SC_band7['dust_err']
flux_SC[0] = flux_SC[0] + flux_SC[1]
flux_GMC = GMC_band6['dust_band7']; flux_GMC_err = GMC_band6['band7_err']
dust_ratio = flux_SC/flux_GMC
ratio_err = ratio * np.sqrt((flux_SC_err/flux_SC)**2 + 
                            (flux_GMC_err/flux_GMC)**2)

# txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
#         '11', '12','13']
# xtext = np.array((flux_GMC+0.05))
# ytext = np.array((0.02+dust_ratio))
# fig = plt.figure(figsize=(10, 10))
# ax = plt.subplot(111)
# plt.xscale('log')
# plt.yscale('log')
# plt.errorbar(flux_GMC, dust_ratio,
#              xerr=flux_GMC_err, yerr=ratio_err, 
#              fmt='o', color = 'red', markersize=12)
# plt.plot([0, ax.get_xlim()[1]], [1, 1], color='black', linestyle='--')
# for i, txt in enumerate(txts):
#     ax.annotate(txt, (flux_GMC[i], dust_ratio[i]), 
#                 (xtext[i], ytext[i]), fontsize=12)
# plt.xlabel(r'$F_{\mathrm{340GHz, GMC}}$ (mJy)', fontsize=30)
# plt.ylabel(r'$F_{\mathrm{340GHz, SC}}/F_{\mathrm{340GHz, GMC}}$ (mJy)', fontsize=30)
# plt.tick_params(labelsize=20)
# plt.tight_layout()
# plt.savefig('pictures/dust_fraction.pdf')

### plot the free-free fraction of these star clusters. 
Leroy_ffrac = [0.03, 0.04, 0.01, 0.07, 0.13, 0.63, 0.07, 0.05, 0.32, 
               0.11, 0.41, 0.71, 0.04, 0.07]
Leroy_ffrac_err = [0.01, 0.01, 0.01, 0.02, 0.02, 0.4, 0.05, 0.02, 
                   0.1, 0.06, 0.11, 0.23, 0.02, 0.01]
Leroy_mstar = 10**np.array([4.3, 4.3, 4.1, 5.0, 5.4, 5.3, 4.5, 4.8, 5.5, 5.3,
                            5.6, 6.0, 4.8, 5.5])
ffrac = SC_band7['ff_frac']; ffrac_err = SC_band7['frac_err']
Mstar = SC_band7['Mstar']; Mstar_err = SC_band7['Mstar_err']

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((10**0.01*Mstar))
ytext = np.array((0.02+ffrac))
ytext[5] = ytext[5]-0.06
fig = plt.figure(figsize=(10,10))
ax = plt.subplot(111)
ax.set_xscale('log')
plt.errorbar(Mstar, ffrac, yerr=ffrac_err, xerr=Mstar_err, fmt='o',
             markersize=12, color='red')
plt.errorbar(Leroy_mstar, Leroy_ffrac, yerr=Leroy_ffrac_err, fmt='.', 
             label='Leroy+2018')
for i, txt in enumerate(txts):
    ax.annotate(txt, (Mstar[i], ffrac[i]), 
                (xtext[i], ytext[i]), fontsize=12)
plt.ylabel('Free Fraction', fontsize=30)
plt.xlabel(r'$M_*$ (M$_{\odot})$', fontsize=30)
plt.tick_params(labelsize=20)
plt.tight_layout()
plt.legend(fontsize=20)
plt.savefig('pictures/freefree_fraction.png')

### plot the stellar mass and gas mass. 
Mstar = SC_band7['Mstar']; Mstar_err = SC_band7['Mstar_err']
Mgas = SC_band7['Mgas_40K']; Mgas_err = SC_band7['Mgas_40K_err']
# Mgas = SC_band7['Mgas_CO_cube']; Mgas_err = SC_band7['Mgas_CO_err_cube']

eff = Mstar/(Mstar+Mgas)
eff_err = eff*np.sqrt((Mstar_err/Mstar)**2+
                (Mgas_err/Mgas)**2)
xuplims = np.full(np.shape(Mstar), fill_value=False)
uplims = np.full(np.shape(eff), fill_value=False)
xuplims[6] = True
uplims[6] = True

# plot the Mgas versus Mstar
txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((10**0.01*Mstar))
ytext = np.array((10**0.01*Mgas))
fig = plt.figure(figsize=(10,8))
ax = plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
plt.errorbar(Mstar, Mgas, 
             yerr=Mgas_err, xerr=Mstar_err,
             fmt='o', markersize=12, color='red')
plt.plot([0, ax.get_ylim()[1]], [0, ax.get_ylim()[1]], color='black', 
         linestyle='--')
for i, txt in enumerate(txts):
    ax.annotate(txt, (Mstar[i], Mgas[i]), 
                (xtext[i], ytext[i]), fontsize=12)
plt.xlabel(r'$M_*$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_*$ (M$_{gas})$', fontsize=30)
plt.tick_params(labelsize=20)
plt.savefig('pictures/gas_star.png')
plt.tight_layout()





### plot the CO mass vs dust traced gas mass
mass_SC = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster')
mass_SC_p5 = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster, 0.5')

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', '12','13']
xtext1 = np.array((10**0.015*mass_SC['Mgas_CO_mom0']))
ytext1 = np.array((10**0.005*mass_SC['Mgas_Tco']))
ytext1[6] = ytext1[6] / 10**0.02

xtext2 = np.array((10**0.015*mass_SC_p5['Mgas_CO_mom0']))
ytext2 = np.array((10**0.005*mass_SC_p5['Mgas_Tco']))

fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
# ax.set_xlim(2e6, 2*10**7)
# ax.set_ylim(2e6, 2*10**7)
plt.errorbar(mass_SC['Mgas_CO_mom0'], mass_SC['Mgas_Tco'], 
              xerr=mass_SC['Mgas_CO_mom0_err'], 
              yerr=mass_SC['Mgas_Tco_err'], 
              fmt='o', markersize=12, label='large aperture')
plt.errorbar(mass_SC_p5['Mgas_CO_mom0'], mass_SC_p5['Mgas_Tco'],
              xerr=mass_SC_p5['Mgas_CO_mom0_err'], 
              yerr=mass_SC_p5['Mgas_Tco_err'], 
              fmt='o', markersize=12, label='small aperture')

plt.legend(loc='lower right', fontsize=20)
plt.plot([0, ax.get_ylim()[1]], [0, ax.get_ylim()[1]], color='black', linestyle='--')
for i, txt in enumerate(txts):
    ax.annotate(txt, (mass_SC['Mgas_CO_mom0'][i], mass_SC['Mgas_Tco'][i]), 
                (xtext1[i], ytext1[i]), fontsize=12)
    ax.annotate(txt, (mass_SC_p5['Mgas_CO_mom0'][i], mass_SC_p5['Mgas_Tco'][i]), 
                (xtext2[i], ytext2[i]), fontsize=12)
plt.xlabel(r'$M_{gas, CO}$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{gas}$ (M$_{\odot})$', fontsize=30)
plt.tick_params(labelsize=20)
plt.savefig('pictures/CO_dust_comparison.pdf')
plt.tight_layout()
