import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import math

###########################################################
# basic parameters
G = 6.67e-11

###########################################################
# basic settings

galaxies = ['NGC253', 'M82', 'MilkyWay', 'NGC4945']
literature_cluster = dict.fromkeys(galaxies)
quantities = ['Mstar', 'Mstar_err', 'Rh', 'Rh_err']

for galaxy in galaxies:
    literature_cluster[galaxy] = pd.DataFrame(columns=quantities)

###########################################################
# function
def read_ascii(filename, columns, colnumber, startrow=0):
    Table3 = pd.DataFrame()
    dictionary = dict.fromkeys(columns)
    for i in range(len(columns)):
        dictionary[columns[i]] = {'value': [], 'colnumber': colnumber[i]}
    with open (filename, 'r') as infile:
        text = infile.readlines()
        text = text[startrow:]
        line = text[0]
        for line in text:
            for key in dictionary.keys():
                lower = dictionary[key]['colnumber'][0]
                upper = dictionary[key]['colnumber'][-1]
                dictionary[key]['value'].append(line[lower:upper])

    coordsName = ['RAh', 'RAm', 'RAs','Ded', 'Dem', 'Des']
    for key in coordsName:
        dictionary[key]['value'] = np.float_(dictionary[key]['value'])

    return dictionary


###########################################################
# main program

# import NGC 253 (stellar mass)
filename = 'tables/NGC253_ascii.txt'
NGC253 = pd.read_csv(filename, skiprows=6, header=None, skipfooter=2, sep='\t',
                    index_col=0)
FWHMs = NGC253[4]
sizes = []
sizes_err = []
for FWHM in FWHMs:
        D = float(FWHM.split(' ')[0])
        D_err = float(FWHM.split(' ')[2])
        sizes.append(D)
        sizes_err.append(D_err)
Leroy_mstar = 10**np.array([4.3, 4.3, 4.1, 5.0, 5.4, 5.3, 4.5, 4.8, 5.5, 5.3,
                            5.6, 6.0, 4.8, 5.5])

literature_cluster['NGC253']['Rh'] = np.array(sizes) / 2
literature_cluster['NGC253']['Rh_err'] = np.array(sizes_err) / 2
literature_cluster['NGC253']['Mstar'] = Leroy_mstar
literature_cluster['NGC253']['Reference'] = 'Leory+2018'


# import M 82 (Virial mass) McCrady+2007 
filename = 'tables/M82_ascii.txt'
M82 = pd.read_csv(filename, sep='\t', skiprows=0, header=None)
Masses = M82[4]
Masses[2] = '0 +- 0'
Masses[8] = '0 +- 0'
Masses[9] = '0 +- 0'
Masses[18] = '0 +- 0'
masses = []
masses_err = []
for Mass in Masses:
    mass = float(Mass.split(' ')[0])*1e5
    mass_err = float(Mass.split(' ')[2])*1e5
    masses.append(mass)
    masses_err.append(mass_err)
masses = np.array(masses)
masses_err = np.array(masses_err)

# From McCrady + 2003
filename = 'tables/M82_rhp.txt'
M82_rad = pd.read_csv(filename, sep='\t', header = None)
rads = M82_rad[6]
radiuses = []
radiuses_err = []

for rad in rads:
    radius = float(rad.split(' ')[0]) * 4.85 * 4.15 / 1000
    radius_err = float(rad.split(' ')[2]) * 4.85 * 4.15 /1000
    radiuses.append(radius)
    radiuses_err.append(radius_err)


literature_cluster['M82']['Rh'] = radiuses
literature_cluster['M82']['Rh_err'] = radiuses_err
literature_cluster['M82']['Mstar'] = masses
literature_cluster['M82']['Mstar_err'] = masses_err
literature_cluster['M82']['Reference'] = 'McCrady+2007'

# import Milky Way (Krumholz+2018)
# stellar mass 
filename = 'tables/Milky_cluster.xlsx'
MilkyWay = pd.read_excel(filename)

masses = MilkyWay['Mass']
masses_err = MilkyWay['Mass err']
radiuses = MilkyWay['Radius']
radiuses_err = MilkyWay['Radius err']

literature_cluster['MilkyWay']['Rh'] = radiuses
literature_cluster['MilkyWay']['Rh_err'] = radiuses_err
literature_cluster['MilkyWay']['Mstar'] = 10**masses
literature_cluster['MilkyWay']['Mstar_err'] = 10**(masses+masses_err) - \
                                            10**masses
literature_cluster['MilkyWay']['Reference'] = 'Krumholz+2019'

# import the NGC 4945 (Emig+2020)
# mass is stellar mass. 
filename = 'tables/NGC4945_ascii.txt'
NGC4945 = pd.read_csv(filename, sep='\t', skiprows=6, skipfooter=3, 
                      header=None, index_col=0)
sizes = NGC4945[1]
FWHMs = []
FWHMs_err = []
for size in sizes:
    FWHM = float(size.split(' ')[0])
    FWHM_err = float(size.split(' ')[2])
    FWHMs.append(FWHM)
    FWHMs_err.append(FWHM_err)

Mstar = 10**NGC4945[5]

literature_cluster['NGC4945']['Rh'] = np.array(FWHMs) / 2
literature_cluster['NGC4945']['Rh_err'] = np.array(FWHMs_err) / 2
literature_cluster['NGC4945']['Mstar'] = Mstar

literature_cluster['NGC4945']['Reference'] = 'Emig+2020'

# import the measurement for antennae cluster.
filename = 'tables/mass.xlsx'
mass_source = pd.read_excel(filename, sheet_name='star cluster, 0.5')
antennae_mass = mass_source['Mstar']
antennae_mass_err = mass_source['Mstar_err']

filename = 'tables/source_size2.xlsx'
radius_source = pd.read_excel(filename, sheet_name='robustp5')
antennae_radius = radius_source['physical'] / 2.0
antennae_radius_err = radius_source['physical_err'] / 2.0

txts = ['1a', '1b', '2', '3', '4','5', '6', '7', '8', '9', '10', '11', 
        '12','13']

# delete source with improved measurements. 
# resolved = [1, 2, 4, 5, 9] # source 9 resolved but undetected in high resolution.
# resolved = [9]
# antennae_mass[resolved] = np.nan

# delete source 4 since it might be time variable
time_variables = [3, 4]
antennae_mass[time_variables] = np.nan
antennae_mass[9] = np.nan # not enough S/N 

xuplims = np.full(np.shape(antennae_mass), fill_value=False)
xuplims[6] = True



xtext = np.array((10**0.01*antennae_mass))
ytext = np.array((10**0.01*antennae_radius))
resolution = 4.85 * 22 * 0.09 / 2.0
resolution_band7 = 4.85 * 22 * 0.11 / 2.0

# import the updated measurements for sources that broken into multiple 
# sources. 
filename = 'tables/mass.xlsx'
mass_source = pd.read_excel(filename, sheet_name='star cluster, add')
antennae_mass_add = mass_source['Mstar']
antennae_mass_add_err = mass_source['Mstar_err']

# deconvolved radius
filename = 'tables/source_size.xlsx'
radius_source = pd.read_excel(filename, sheet_name='robustp5_add')
antennae_radius_add = radius_source['physical'] / 2.0

# remove source 9a and 9b
antennae_radius_add[3] = np.nan
antennae_radius_add[4] = np.nan
antennae_radius_add[6] = np.nan
antennae_radius_add[7] = np.nan

txts_add = ['1b I', '1b II', '2a', '4a', '4b', '5a', '9a', '9b']
xtext_add = np.array((10**0.01*antennae_mass_add))
ytext_add = np.array((10**0.01*antennae_radius_add))

# fit the literature sample. 
whole_Mstar = []
whole_radius = []
for galaxy in galaxies:
    whole_Mstar = whole_Mstar + literature_cluster[galaxy]['Mstar'].to_list()
    whole_radius = whole_radius + literature_cluster[galaxy]['Rh'].to_list()

whole_Mstar = np.array(whole_Mstar)
whole_radius = np.array(whole_radius)

# select the star cluster with Mstar greater than 10^5 solor mass
whole_Mstar[np.where(whole_Mstar < 10**5)] = np.nan
mask = ~np.isnan(whole_Mstar) & ~np.isnan(whole_radius)

# fit the power law relation 
def func_powerlaw(x, c):
    return x**(1/3) * c

target_func = func_powerlaw
popt, pcov = curve_fit(target_func, whole_Mstar[mask], whole_radius[mask])

whole_Mstar_theory = 10**np.linspace(5, 7, 20)
whole_radius_theory = target_func(whole_Mstar_theory, *popt)
perr = np.sqrt(np.diag(pcov))

# import the virial radius. 
#r_vir = pd.read_excel('tables/source_size.xlsx', sheet_name='virial', 
#                      index_col=0)

fig = plt.figure(figsize=(6, 5))
ax = plt.subplot('111')
plt.xscale('log')
plt.yscale('log')
plt.errorbar(antennae_mass, antennae_radius, xerr=antennae_mass_err, 
             yerr=antennae_radius_err, xuplims=xuplims,
             marker = 'o', linestyle='', label = 'Antennae', color='tab:orange')
# plt.errorbar(antennae_mass_add, antennae_radius_add, xerr=antennae_mass_add_err, 
#              marker = 'o', linestyle='', color='#1f77b4')
# plt.scatter(antennae_mass, r_vir, marker='o', color='red')

for i, txt in enumerate(txts):
    plt.annotate(txt, (antennae_mass[i], antennae_radius[i]), 
                (xtext[i], ytext[i]), fontsize=20)
# for i, txt in enumerate(txts_add):
#     plt.annotate(txt, (antennae_mass_add[i], antennae_radius_add[i]), 
#                 (xtext_add[i], ytext_add[i]), fontsize=12)
colors = ['red', 'blue', 'green', 'black']
for i, galaxy in enumerate(galaxies):
    plt.errorbar(literature_cluster[galaxy]['Mstar'], 
                literature_cluster[galaxy]['Rh'],
                yerr = literature_cluster[galaxy]['Rh_err'], 
                xerr = literature_cluster[galaxy]['Mstar_err'],
                marker = '.', linestyle = '', 
                label = galaxy,
                color=colors[i])
plt.xlabel(r'$M_{\star} (M_{\odot})$', fontsize=30)
plt.ylabel('R$_{\mathrm{h}}$ (pc)', fontsize=30)
ax.tick_params(labelsize=20)
    
# draw the line for different feedback mechanism
plt.axline([10**4.2, 0.2], [10**5, 1], linestyle='dashed', color='purple')
plt.axline([10**4, 0.4], [10**6, 4], linestyle='dashed', color='firebrick')
plt.axline([10**5, 0.3], [10**6, 1], linestyle='dashed', color='red')

# label the line
plt.annotate('Direct Radiation', xy=(0.1, 0.1), xytext=(-0.1, 0.05), rotation=32,
             xycoords='axes fraction', annotation_clip=False, fontsize=14)
plt.annotate('Photon Ionization', xy=(0.1, 0.1), xytext=(0.1, 0), rotation=45,
             xycoords='axes fraction', annotation_clip=False, fontsize=14)
plt.annotate('IR', xy=(0.1, 0.1), xytext=(0.5, 0.1), rotation=38,
             xycoords='axes fraction', annotation_clip=False, fontsize=14)

# ax.axhline(resolution, linestyle='dashed')
ax.axhline(resolution_band7, linestyle='dotted',color='black')
# plt.plot(whole_Mstar_theory, whole_radius_theory , '--', 
#          label = str(round(popt[0],3))+' $\pm$ '+str(round(perr[0],3)))

# legend
plt.legend(fontsize=14, framealpha=0.5, loc='lower right')
plt.tight_layout()
plt.savefig('pictures/size_mass.pdf')

# import NGC 253 mass and size from Leory+2015 and Levy+2020 to see how 
# different resolutions change the measured size of the star cluster. 
print(antennae_radius)
