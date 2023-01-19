import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

df = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster, 0.5')

# input the data for the stellar mass and gas mass
Mstar = df['Mstar']; Mstar_err = df['Mstar_err']
Mgas = df['Mgas_Tco']; Mgas_err = df['Mgas_Tco_err']
Mtot = Mstar + Mgas; Mtot_err = Mstar_err + Mgas_err

eff = Mstar/(Mstar+Mgas)
eff_err = eff*np.sqrt((Mstar_err/Mstar)**2+
                (Mtot_err/Mtot)**2)
xuplims = np.full(np.shape(Mstar), fill_value=False)
uplims = np.full(np.shape(eff), fill_value=False)
xuplims[6] = True
uplims[6] = True

# input them data for the Sigma_tot
df1 = pd.read_excel('tables/density.xlsx', sheet_name='star cluster, 0.5')
Sigma_tot = df1['Sigma_tot']; Sigma_tot_err = df1['Sigma_tot_err']

############################# 
# plot stellar fraction versus stellar mass

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', '12','13']
xtext = np.array((10**0.005*Mstar))
ytext = np.array((0.02+eff))
ytext[5] = ytext[5]-0.04
fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, 
                                                    symbol='%', 
                                                    is_latex=False))
ax.tick_params(labelsize = 20)

plt.errorbar(Mstar, eff, 
             yerr=eff_err, xerr=Mstar_err,
             xuplims=xuplims, uplims=uplims,
             fmt='o', markersize=12, color='tab:orange')
ax.axhline(1, color='black', linestyle='--')
ax.annotate('100%', [2e5, 1], [2e5,0.7], fontsize=20)
ax.axhline(0.5, color='black', linestyle='--')
ax.annotate('50%', [2e5, 0.5], [2e5,0.35], fontsize=20)
for i, txt in enumerate(txts):
    ax.annotate(txt, (Mstar[i], eff[i]), 
                (xtext[i], ytext[i]), fontsize=20)
plt.xlabel(r'$M_{\star}$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{\star}$/M$_{tot}$', fontsize=30)
# plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('pictures/efficiency.pdf')

#############################
## plot stellar fraction versus total mass
xtext = np.array((10**0.005*Mtot))
ytext = np.array((0.02+eff))
fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, 
                                                    symbol='%', 
                                                    is_latex=False))
plt.xlim([1e6,1e7])
ax.tick_params(labelsize = 20)

plt.errorbar(Mtot, eff, 
             yerr=eff_err, xerr=Mtot_err,
             uplims=uplims,
             fmt='o', markersize=12, color='tab:orange')
ax.axhline(1, color='black', linestyle='--')
# ax.annotate('100%', [4e6, 1], [4e6,0.7], fontsize=20)
ax.axhline(0.5, color='black', linestyle='--')
# ax.annotate('50%', [4e6, 0.5], [4e6,0.35], fontsize=20)
for i, txt in enumerate(txts):
    ax.annotate(txt, (Mtot[i], eff[i]), 
                (xtext[i], ytext[i]), fontsize=20)
plt.xlabel(r'$M_{tot}$ (M$_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{\star}$/M$_{tot}$', fontsize=30)
# plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('pictures/efficiency_Mtot.pdf')

#############################
# plot stellar fraction versus surface density
xtext = np.array((10**0.005*Sigma_tot))
ytext = np.array((0.02+eff))
xtext[1] = xtext[1] / 10**0.15

fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, 
                                                    symbol='%', 
                                                    is_latex=False))
ax.tick_params(labelsize = 20)
plt.xlim(1e3, 1e5)

# plot the data
plt.errorbar(Sigma_tot, eff, 
             yerr=eff_err, xerr=Sigma_tot_err,
             uplims=uplims,
             fmt='o', markersize=12, color='tab:orange')

# plot the theoretical values (Fall+2010)
Sigma_theory = 10**np.arange(3, 5.1, 0.1)
eff_theory_upp = Sigma_theory / (1.2*0.25*6310+Sigma_theory)
eff_theory_mid = Sigma_theory / (1.2*6310+Sigma_theory)
eff_theory_low = Sigma_theory / (1.2*4*6310+Sigma_theory)

plt.plot(Sigma_theory, eff_theory_upp, linestyle='--', 
         label=r'$f_{trap}$ / $\alpha_{crit}$ = 1/4')
plt.plot(Sigma_theory, eff_theory_mid, linestyle='--',
         label=r'$f_{trap}$ / $\alpha_{crit}$ = 1')
plt.plot(Sigma_theory, eff_theory_low, linestyle='--',
         label=r'$f_{trap}$ / $\alpha_{crit}$ = 4')
plt.legend(fontsize=15, loc='lower left', framealpha=0.5)

# annotate the data points
ax.axhline(1, color='black', linestyle='--')
# ax.annotate('100%', [2e3, 1], [2e3,0.8], fontsize=20)
ax.axhline(0.5, color='black', linestyle='--')
# ax.annotate('50%', [2e3, 0.5], [2e3,0.4], fontsize=20)
for i, txt in enumerate(txts):
    ax.annotate(txt, (Sigma_tot[i], eff[i]), 
                (xtext[i], ytext[i]), fontsize=20)
plt.xlabel(r'$\Sigma_{tot}$ (M$_{\odot}\ pc^{-2})$', fontsize=30)
plt.ylabel(r'$M_{\star}$/M$_{tot}$', fontsize=30)
plt.tight_layout()
plt.savefig('pictures/efficiency_Sigtot.pdf')