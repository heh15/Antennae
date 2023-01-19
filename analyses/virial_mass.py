'''
Use total mass and measured velocity dispersion to derive the radius to reach
virial equilibrium. Then we can compare the virial radius with the deconvolved
radius to check if our measured size makes sense. 
'''
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import math


###########################################################
# basic settings

D = 22
k = 1.38e-23
G = 6.67e-11

picturetype = 'poster'

FigureParams = {}
FigureParams['poster'] = {}
FigureParams['poster']['figsize'] = (6,6)
FigureParams['poster']['legendsize'] = 18
FigureParams['poster']['labelsize'] = 40


###########################################################
# main program

# import the total mass
filename = 'tables/mass.xlsx'
df = pd.read_excel(filename, sheet_name='star cluster, 0.5')
Mstar = df['Mstar']
Mstar_err = df['Mstar_err']

# import gas
Mgas = df['Mgas_Tco']
Mgas_err = df['Mgas_Tco_err']
# Mgas = df['Mgas_130K']
# Mgas_err = df['Mgas_err']

# calculate total mass of the star cluster
Mtot = Mstar + Mgas
Mtot_err = np.sqrt(Mstar_err**2+Mgas_err**2)

# import the velocity dispersion
filename = 'dispersion.xlsx'
df1 = pd.read_excel(filename)
dispersion = df1['dispersion, 2.0']
dispersion_err = df1['error.1']

# Calculate the virial radius (Leroy+08, equation 8)
d_vir = Mtot / 892 / dispersion**2
r_vir = d_vir / 2
r_vir.name = 'Virial Radius'

# # export the virial radius to the excel. 
# path = 'tables/source_size.xlsx'
# book = load_workbook(path)

# with pd.ExcelWriter('tables/source_size.xlsx', engine='openpyxl') as writer: 
#     writer.book = book
#     r_vir.to_excel(writer, sheet_name = 'virial')


## Compare the virial mass and total mass for different star clusters. 
path = 'tables/source_size2.xlsx'
df = pd.read_excel(path, sheet_name='robustp5')
radius = df['physical'] / 2
radius_err = df['physical_err'] / 2

M_vir = 531 * (2*radius) * dispersion**2
M_vir_err = np.sqrt((2*dispersion_err/dispersion)**2+
                       (radius_err/radius)**2) * M_vir
txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', 
        '12','13']
xtext = np.array((10**0.01*Mtot))
ytext = np.array((10**0.01*M_vir))


## Add additional measurements

# import stellar mass 
path = 'tables/mass.xlsx'
df_add = pd.read_excel(path, sheet_name = 'star cluster, add')
Mstar_add = df_add['Mstar']
Mstar_err_add = df_add['Mstar_err']

# import gas mass 
path = 'tables/mass.xlsx'
df_add = pd.read_excel(path, sheet_name='star cluster, add')
Mgas_add = df_add['Mgas_Tco']
Mgas_err_add = df_add['Mgas_Tco_err']

Mtot_add = Mstar_add + Mgas_add
Mtot_err_add = np.sqrt(Mstar_err_add**2+Mgas_err_add**2)

# import radius 
path = 'tables/source_size.xlsx'
df_add = pd.read_excel(path, sheet_name='robustp5_add')
radius_add = df_add['physical'] / 2

# import velocity dispersion
filename = 'dispersion.xlsx'
df_add2 = pd.read_excel(filename, sheet_name='robustp5_add')
dispersion_add = df_add2['dispersion']
dispersion_err_add = df_add2['error']

Mvir_add = 531 * (2*radius_add) * dispersion_add**2
Mvir_err_add = 2 * (dispersion_err_add/dispersion_add) * Mvir_add
txts_add = ['1bI', '1bII', '2a', '4a', '4b', '5a', '9a', '9b']
xtext_add = np.array((10**0.01*Mtot_add))
ytext_add = np.array((10**0.01*Mvir_add))



# delete source with improved measurements. 
# resolved = [1, 2, 4, 5, 9] # source 9 resolved but undetected in high resolution.
# M_vir[resolved] = np.nan

fig = plt.figure(figsize=(5, 5))
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'$M_{tot}\ (M_{\odot})$', fontsize=30)
plt.ylabel(r'$M_{vir}\ (M_{\odot})$', fontsize=30)
ax.tick_params(labelsize=20)


plt.errorbar(Mtot, M_vir, xerr=Mtot_err, yerr=M_vir_err, marker = 'o', 
              linestyle = '', color='tab:orange')
for i in Mtot.index:
    plt.arrow(Mtot[i], M_vir[i], 0, -0.3*M_vir[i], length_includes_head=True, 
              head_width=0.1*Mtot[i], head_length=0.1*M_vir[i], color='tab:orange')
# plt.arrow(np.array(Mtot), np.array(M_vir), 0,0)
# plt.errorbar(Mvir_add, Mtot_add, xerr=Mvir_err_add, yerr=Mtot_err_add, 
#                marker='o', linestyle='')
ax.set_xlim(left=1e6)
# ax.set_ylim(top=9e6)
 
for i, txt in enumerate(txts):
    plt.annotate(txt, (Mtot[i], M_vir[i]), 
                (xtext[i], ytext[i]), fontsize=20)
# for i, txt in enumerate(txts_add):
#     plt.annotate(txt, (Mvir_add[i], Mtot_add[i]), 
#                 (xtext_add[i], ytext_add[i]), fontsize=20)

lower=max(ax.set_xlim()[0], ax.set_ylim()[0])
upper=min(ax.set_xlim()[1], ax.set_ylim()[1])
ax.plot([lower, upper],[lower,upper],ls='--', color='black')
ax.plot([lower/2, upper],[lower,upper*2],ls='--', color='black')
ax.annotate('Virialized', (1.5e6, 1.5e6), 
            (1.5e6, 1.2e6), fontsize=20, rotation=38.0)
ax.annotate('Bound', (1.2e6, 2.4e6), 
            (1.2e6, 2.1e6), fontsize=20, rotation=38.0)
fig.tight_layout()
plt.savefig('pictures/Mvir_Mtot.pdf')

### Compare the gas mass to the virial mass

## Add the updated virial mass for substructures.
df2 = pd.read_excel('tables/mass.xlsx', sheet_name='star cluster')
Mgas2 = df2['Mgas_Tco']; Mgas_err2 = df2['Mgas_Tco_err']

df2 = pd.read_excel('tables/source_size.xlsx', sheet_name='robust2')
radius2 = df2['physical']

Mvir2 = 531 * (2*radius2) * dispersion**2
Mvir_err2 = 2 * (dispersion_err/dispersion) * Mvir2

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', 
        '12','13']
xtext = np.array((10**0.01*Mvir2))
ytext = np.array((10**0.01*Mgas2))

# fig = plt.figure(figsize=(6, 6))
# ax = plt.subplot(111)
# plt.xscale('log')
# plt.yscale('log')
# plt.xlabel(r'$M_{vir}\ (M_{\odot})$', fontsize=30)
# plt.ylabel(r'$M_{gas}\ (M_{\odot})$', fontsize=30)
# plt.errorbar(Mvir2, Mgas2, xerr=Mvir_err2, yerr=Mgas_err2, marker = 'o', 
#               linestyle = '')
# for i, txt in enumerate(txts):
#     plt.annotate(txt, (Mvir2[i], Mgas2[i]), 
#                 (xtext[i], ytext[i]), fontsize=20)
# lower=max(ax.set_xlim()[0], ax.set_ylim()[0])
# upper=min(ax.set_xlim()[1], ax.set_ylim()[1])
# ax.plot([lower, upper],[lower,upper],ls='--', color='black')

### Add the pressure component

# variables, R - radius, dispersion - dispersion, Mtot
# See note of Leroy+2018


size = math.pi * (radius)**2

Sigma_tot = Mtot / size
Sigma_tot_err = Mtot_err / Mtot *Sigma_tot

## Calculate the ratio=
sizelinewidth_ratio = dispersion**2 / radius
sizelinewidth_ratio_err = (2*dispersion_err/dispersion) * sizelinewidth_ratio

# import the velocity dispersion

size_add = math.pi * (radius_add)**2
Sigma_add = Mtot_add / size_add
Sigma_err_add = Mtot_err_add / Mtot_add * Sigma_add

ratio_add = dispersion_add**2 / radius_add
ratio_err_add = (2*dispersion_err_add/dispersion_add) * ratio_add


Sigma_theory = 10**np.linspace(3, 5, 20)
pressures = 10**np.linspace(7, 9, 3)

# resolved = [1, 2, 4, 5, 9]
# Sigma_tot[resolved] = np.nan

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', 
        '12','13']
xtext = np.array((10**0.01*Sigma_tot))
ytext = np.array((10**0.01*sizelinewidth_ratio))

txts_add = ['1bI', '1bII', '2a', '4a', '4b', '5a', '9a', '9b']
xtext_add = np.array((10**0.01*Sigma_add))
ytext_add = np.array((10**0.01*ratio_add))

fig = plt.figure(figsize=(6,6))
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.errorbar(Sigma_tot, sizelinewidth_ratio, 
             xerr=Sigma_tot_err, yerr = sizelinewidth_ratio_err, 
             marker='o', linestyle='', color='tab:orange')
# plt.errorbar(Sigma_add, ratio_add, xerr = Sigma_err_add, yerr = ratio_err_add,
#               marker='o', linestyle='')
plt.xlabel('$\Sigma_{tot}$ M$_{\odot}$ pc$^{-2}$', fontsize=30)
plt.ylabel('$\sigma^2/R$ (km/s)$^2$/pc', fontsize=30)
ratio = 0.45 * (Sigma_theory/100)
plt.plot(Sigma_theory, ratio, linestyle='dashed')
for p in pressures: 
    ratio = 0.45 * (Sigma_theory/100) + 2.74e-4*p/Sigma_theory
    plt.plot(Sigma_theory, ratio, linestyle='dashed', 
              label="{:.2e}".format(p)+' K cm$^{-3}$')

# ax.set_xlim(right=5e4)
# ax.set_ylim(top=5e4)
    
for i, txt in enumerate(txts):
    plt.annotate(txt, (Sigma_tot[i], sizelinewidth_ratio[i]), 
                (xtext[i], ytext[i]), fontsize=20)
# for i, txt in enumerate(txts_add):
#     plt.annotate(txt, (Sigma_add[i], ratio_add[i]), 
#                 (xtext_add[i], ytext_add[i]), fontsize=15)
plt.legend(loc='lower right', fontsize=18)
fig.tight_layout()
plt.savefig('pictures/Mtot_bound_pressure.pdf', bbox_inches='tight')

### Calculate the turbulent pressure for those star clusters
# Sun+2020b
press_clusters = 3.3e4 * (Sigma_tot /100)* (dispersion/10)**2 * (radius/75)**(-1)

### print the value and uncertainty
print(np.log10(M_vir))
print(1/np.log(10)*M_vir_err/M_vir)
print(np.log10(Sigma_tot))
print(np.log10(press_clusters))