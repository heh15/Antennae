import numpy as np
import pandas as pd
from openpyxl import load_workbook

###########################################################
# basic settings 

freq_co21 = 230

co2_1_ratio = 0.7

D_Mpc = 22
D = D_Mpc*1e6*3.1e16
beta = 1.5
z = 0.0055

###########################################################
# main program

SC_properties = pd.DataFrame()

### Calculate the gas mass based on CO fluxes
df_line = pd.read_excel('flux_measure.xlsx', sheet_name='line')
SC_band7 = pd.read_excel('tables/Derived.xlsx', sheet_name = 'star cluster', 
                         index_col=0)

# CO mass measured from cubes
SC_band7['Mgas_CO_cube'] = df_line['co21 pbcor cube'] / (4*co2_1_ratio) *\
    1.05e4*D_Mpc**2/(1+z)
SC_band7['Mgas_CO_err_cube'] = SC_band7['Mgas_CO_cube']*\
    df_line['uncertainty']/df_line['co21 pbcor cube']

# CO mass from the moment 0 maps
SC_band7['Mgas_CO_mom0'] = df_line['co21 pbcor mom0'] / (4*co2_1_ratio) *\
    1.05e4*D_Mpc**2/(1+z)
SC_band7['Mgas_CO_err_mom0'] = SC_band7['Mgas_CO_cube']*\
    df_line['uncertainty.1']/df_line['co21 pbcor mom0']
    
### export the CO mass to the table
path = 'tables/Derived.xlsx'
book = load_workbook(path)
sheet = book.get_sheet_by_name('star cluster')
book.remove_sheet(sheet)

with pd.ExcelWriter('tables/Derived.xlsx', engine='openpyxl') as writer: 
    writer.book = book
    SC_band7.to_excel(writer, sheet_name = 'star cluster')
    

### CO mass for additional apertures. 
df_line_add = pd.read_excel('flux_measure.xlsx', sheet_name='line_add')

# CO mass measured from cubes
SC_properties['Mgas_CO_cube'] = 2 * df_line_add['co21 flux cube'] / (4*co2_1_ratio) *\
    1.05e4*D_Mpc**2/(1+z)
SC_properties['Mgas_CO_err_cube'] = SC_properties['Mgas_CO_cube']*\
    df_line_add['uncertainty']/df_line_add['co21 flux cube']

# CO mass from the moment 0 maps
SC_properties['Mgas_CO_mom0'] = 2 * df_line_add['co21 flux mom0'] / (4*co2_1_ratio) *\
    1.05e4*D_Mpc**2/(1+z)
SC_properties['Mgas_CO_err_mom0'] = SC_properties['Mgas_CO_cube']*\
    df_line_add['uncertainty.1']/df_line_add['co21 flux mom0']


SC_properties.index = df_line_add['source']

with pd.ExcelWriter('tables/Mgas.xlsx') as writer:  
    SC_properties.to_excel(writer, sheet_name = 'robust0.5, 0.09')




