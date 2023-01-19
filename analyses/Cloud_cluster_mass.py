import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


###########################################################
# basic settings

picturetype = 'poster'
FigureParams = {}
FigureParams['poster'] = {}
FigureParams['poster']['figsize'] = (6,6)
FigureParams['poster']['legendsize'] = 20

###########################################################
# main program

# impor the data from anennae measurement

mass_SC = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster, 0.5')
mass_GMC = pd.read_excel('tables/mass.xlsx', sheet_name='GMC')

SC_Mstar = mass_SC['Mstar']; SC_MstarErr = mass_SC['Mstar_err']
SC_Mgas = mass_SC['Mgas_Tco']; SC_Mgaserr = mass_SC['Mgas_Tco_err']
SC_Mtot = SC_Mstar + SC_Mgas 
SC_Mtoterr = mass_SC['Mstar_err'] + mass_SC['Mgas_Tco_err']

GMC_M = mass_GMC['Mgas_Tco']; GMC_Merr = mass_GMC['Mgas_Tco_err'] 

remove = [3,4,9]
uplims = np.full(np.shape(SC_Mstar), fill_value=False)
uplims[6] = True
SC_Mstar[remove] = np.nan

# import the data for Milky Way
MW_YMC = pd.read_excel('MW_YMC.xlsx')

# filter out GMC with offset distance greater than 0.3 kpc
MW_YMC['GMC, mass'][MW_YMC['GMC, offset (kpc)'] > 0.3] = np.nan

MW_YMC_group = MW_YMC.groupby('GMC, mass')
idx = MW_YMC_group['log(Mass)'].idxmax(axis=1)
MW_YMC_max = MW_YMC.loc[idx].reset_index()

MW_SCmass = 10**MW_YMC_max['log(Mass)']
MW_SCmass_err = 2.303 * MW_SCmass * MW_YMC_max['mass_err']
MW_GMCmass = MW_YMC_max['GMC, mass']
MW_GMCmass_err = MW_YMC_max['mass_err_plus']
MW_offset = MW_YMC_max['GMC, offset (kpc)']

idx_off_300 = np.where(MW_offset > 0.2)[0]
idx_off_200 = np.where((MW_offset > 0.1) & (MW_offset <= 0.2))[0]
idx_off_100 = np.where(MW_offset < 0.1)[0]

# import the data for NGC 253
NGC253_YMC = pd.read_excel('NGC253_YMC_GMC.xlsx')
NGC253_YMC['Mtot'] = 10**NGC253_YMC['M_star'] + 10**NGC253_YMC['M_gas']

NGC253_YMC_group = NGC253_YMC.groupby('GMC_mass')
idx = NGC253_YMC_group['M_star'].idxmax(axis=1)
NGC253_YMC_max = NGC253_YMC.loc[idx]
NGC253_SCmass = 10**NGC253_YMC_max['M_star']
NGC253_SCmass_err = NGC253_SCmass * NGC253_YMC_max['Mstar_relerr']

idx1 = NGC253_YMC_group['Mtot'].idxmax(axis=1)
NGC253_YMC_max1 = NGC253_YMC.loc[idx1]
NGC253_SCMtot = NGC253_YMC_max1['Mtot']

NGC253_GMCmass = NGC253_YMC_max['GMC_mass']
ratio = NGC253_YMC_max['GMC_mass_relerr']
upper_err = NGC253_GMCmass*(ratio-1)
lower_err = NGC253_GMCmass*(1-1/ratio)
NGC253_GMCmass_err = [lower_err, upper_err]


#############################
# Mstar vs MGMC
fig = plt.figure(figsize=FigureParams['poster']['figsize'])
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(GMC_M, SC_Mstar, xerr=GMC_Merr, yerr=SC_MstarErr, uplims=uplims, 
             linestyle='', marker='o', color='tab:orange',
             label='Antennae')
plt.errorbar(MW_GMCmass[idx_off_300], MW_SCmass[idx_off_300], 
             xerr=MW_GMCmass_err[idx_off_300], yerr=MW_SCmass_err[idx_off_300],
             linestyle='', marker='o', color='tab:blue', markersize=2.5,
             label='Milky Way (>200 pc)')
plt.errorbar(MW_GMCmass[idx_off_200], MW_SCmass[idx_off_200], 
             xerr=MW_GMCmass_err[idx_off_200], yerr=MW_SCmass_err[idx_off_200],
             linestyle='', marker='o', color='tab:blue',markersize=5, 
             label='Milky Way (>100 pc)')
plt.errorbar(MW_GMCmass[idx_off_100], MW_SCmass[idx_off_100], 
             xerr=MW_GMCmass_err[idx_off_100], yerr=MW_SCmass_err[idx_off_100],
             linestyle='', marker='o', color='tab:blue', markersize=10,
             label='Milky Way (<100 pc)')
plt.errorbar(NGC253_GMCmass, NGC253_SCmass, yerr=NGC253_SCmass_err, 
             xerr = NGC253_GMCmass_err, 
             linestyle='', marker='o', color='tab:purple', label='NGC 253')

plt.ylim(top=1e7)
lower=max(ax.set_xlim()[0], ax.set_ylim()[0])
upper=min(ax.set_xlim()[1], ax.set_ylim()[1])
ax.plot([lower, 10*upper],[lower/10,upper],ls='--', color='black')
ax.annotate('10%', (10**6.0, 10**5.0), 
                (10**5.5, 10**5.0), fontsize=20)
ax.plot([lower, 100*upper],[lower/100,upper],ls='--', color='black')
ax.annotate('1%', (10**7.0, 10**5.0), 
                (10**6.7, 10**5.0), fontsize=20)
# ax.plot([lower, 50*upper],[lower/50,upper],ls='--', color='black')

Mx = 10**np.linspace(4, 8.5, 5)
My = 10**(-0.12)* Mx**0.78
ax.plot(Mx, My, ls='-', label='feedback on', color='green')

Mx = 10**np.linspace(4, 8.5, 5)
My = 10**(-0.68)* Mx**0.92
ax.plot(Mx, My, ls='-', label='feedback off', color='red')

# add annotation
txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((GMC_M*1.1))
ytext = np.array((SC_Mstar*1.1))
ytext[5] = 0.8 * ytext[5]
for i, txt in enumerate(txts):
    ax.annotate(txt, (GMC_M[i], SC_Mstar[i]), 
                (xtext[i], ytext[i]), fontsize=20)

# add label
plt.xlabel(r'$M_{\mathrm{GMC}}$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{\star, YMC}$ (M$_{\odot})$', fontsize=30)
plt.tick_params(labelsize=20, direction='in')
plt.legend(fontsize=12, framealpha=0.5, loc='upper left')
fig.tight_layout()
# save figure
# plt.savefig('pictures/MGMC_MSCstar.pdf', bbox_inches='tight')
plt.savefig('pictures/MGMC_MSCstar.png', bbox_inches='tight', dpi=300)


#############################
# Mtot vs MGMC
fig = plt.figure(figsize=FigureParams['poster']['figsize'])
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(GMC_M, SC_Mtot, xerr=GMC_Merr, yerr=SC_Mtoterr, 
             linestyle='', marker='o', color='tab:orange',
             label='Antennae')
# plt.errorbar(MW_GMCmass, MW_SCmass, xerr=MW_GMCmass_err, yerr=MW_SCmass_err,
#              linestyle='', marker='o', color='tab:blue',
#              label='Milky Way')
plt.errorbar(MW_GMCmass[idx_off_300], MW_SCmass[idx_off_300], 
             xerr=MW_GMCmass_err[idx_off_300], yerr=MW_SCmass_err[idx_off_300],
             linestyle='', marker='o', color='tab:blue', markersize=2.5,
             label='Milky Way (>200 pc)')
plt.errorbar(MW_GMCmass[idx_off_200], MW_SCmass[idx_off_200], 
             xerr=MW_GMCmass_err[idx_off_200], yerr=MW_SCmass_err[idx_off_200],
             linestyle='', marker='o', color='tab:blue',markersize=5, 
             label='Milky Way (>100 pc)')
plt.errorbar(MW_GMCmass[idx_off_100], MW_SCmass[idx_off_100], 
             xerr=MW_GMCmass_err[idx_off_100], yerr=MW_SCmass_err[idx_off_100],
             linestyle='', marker='o', color='tab:blue', markersize=10,
             label='Milky Way (<100 pc)')

plt.errorbar(NGC253_GMCmass, NGC253_SCMtot, yerr=NGC253_SCmass_err, 
             xerr = NGC253_GMCmass_err, 
             linestyle='', marker='o', color='tab:purple', label='NGC 253')

plt.ylim(top=1e7)
lower=max(ax.set_xlim()[0], ax.set_ylim()[0])
upper=min(ax.set_xlim()[1], ax.set_ylim()[1])
ax.plot([lower, 10*upper],[lower/10,upper],ls='--', color='black')
ax.annotate('10%', (10**6.0, 10**5.0), 
                (10**5.5, 10**5.0), fontsize=20)
ax.plot([lower, 100*upper],[lower/100,upper],ls='--', color='black')
ax.annotate('1%', (10**7.0, 10**5.0), 
                (10**6.7, 10**5.0), fontsize=20)
# ax.plot([lower, 50*upper],[lower/50,upper],ls='--', color='black')

Mx = 10**np.linspace(4, 8.5, 5)
My = 10**(-0.12)* Mx**0.78
ax.plot(Mx, My, ls='-', label='feedback on', color='green')

Mx = 10**np.linspace(4, 8.5, 5)
My = 10**(-0.68)* Mx**0.92
ax.plot(Mx, My, ls='-', label='feedback off', color='red')

# add annotation
txts = ['1', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', 
        '11', '12','13']
xtext = np.array((GMC_M*1.1))
ytext = np.array((SC_Mtot*1.1))
ytext[5] = 0.8 * ytext[5]
ytext[7] = 0.8 * ytext[7]
for i, txt in enumerate(txts):
    ax.annotate(txt, (GMC_M[i], SC_Mtot[i]), 
                (xtext[i], ytext[i]), fontsize=20)

# add label
plt.xlabel(r'$M_{\mathrm{GMC}}$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{tot, YMC}$ (M$_{\odot})$', fontsize=30)
plt.tick_params(labelsize=20, direction='in')
plt.legend(fontsize=12, framealpha=0.5, loc='upper left')
fig.tight_layout()
# save figure
plt.savefig('pictures/MGMC_MSCtot.pdf', bbox_inches='tight')