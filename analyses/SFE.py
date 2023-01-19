import pandas as pd
import matplotlib.pyplot as plt

mass_GMC = pd.read_excel('tables/mass.xlsx', sheet_name='GMC')
Mstar = mass_GMC['Mstar']
Mgas = mass_GMC['Mgas_20K']

SFE = Mstar / (Mstar+Mgas)

fig = plt.figure()
ax = plt.subplot(111)
plt.xscale('log')
plt.yscale('log')
plt.xlim([1e6, 1e8])
plt.scatter((Mstar+Mgas), SFE)