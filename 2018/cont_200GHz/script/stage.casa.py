'''
June 9th, 2020
by Hao He
purpose: to image the continuum using auth-multithresh. 

June. 14th, 2020. 
1) Try the modified extract_continuum function from phangsPipline, excluded lines includes
co10, cn10high, cn10low and hc3n110. haven't included c17o.
2) For averaging the channels, use the conservative empirical value of 125 MHz for band 3 
data. The average channel number is 32. 

'''

import copy
import os
import time

############################################################
# directory

Dir = '/home/heh15/research/Antennae/2018/cont_200GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'

############################################################
# function

def count(stop, start):
    dure=stop-start
    m,s=divmod(dure,60)
    h,m=divmod(m,60)
    print("%d:%02d:%02d" %(h, m, s))

    return

############################################################
# basic parameters. 

do_individual = False
do_concat = True

keywords = {}
keywords['galaxy'] = 'ngc4038'
keywords['band'] = 'band6'
keywords['datatype'] = 'cont'

arrays = ['12mext', '12mcomp', '7m']

parameters = dict.fromkeys(arrays)
for key in arrays:
    parameters[key] = copy.deepcopy(default)

# outputvis files
outputvises = [calDir + 'ngc4038_band6_cont_12mext.ms',
               calDir + 'ngc4038_band6_cont_12mcomp.ms', 
               calDir + 'ngc4038_band6_cont_7m.ms']

### import the parameters from the config files. 
sys.path.append('configs/')

# personal edit for 12m compact array parameters. 
from stage_params_12mcomp import * 
parameters['12mcomp'] = copy.deepcopy(par_stage)

# personal edit for 12m extended array parameters. 
from stage_params_12mext import *
parameters['12mext'] = copy.deepcopy(par_stage)

# personal edit for 7m array
from stage_params_7m import *
parameters['7m'] = copy.deepcopy(par_stage)

############################################################
# main program 

start = time.time()

if do_individual == True:
    outputvises = []
    for key in arrays:
        # split the calibrated data and place it into the folder, try 12m compact and 7m first. 
        vis = parameters[key]['vis']
        outputvis = parameters[key]['outputvis']
        outputvises.append(outputvis)
        field = parameters[key]['field']
        lines_to_flag = parameters[key]['lines_to_flag']
        PPhao.extract_continuum(in_file=vis, 
                                out_file=outputvis,
                                lines_to_flag=lines_to_flag,
                                gal = parameters[key]['field'], 
                                spw = parameters[key]['spw'], 
                                vsys=parameters[key]['vsys'], 
                                vwidth=parameters[key]['vwidth'],
                                do_statwt=parameters[key]['do_statwt'], 
                                do_collapse=parameters[key]['do_collapse'],
                                collapse_width=parameters[key]['collapse_width'])

if do_concat == True:
    galaxy = keywords['galaxy']
    band = keywords['band']
    cont = keywords['datatype'] 
    arrays_str = '_'.join(arrays)
    concatvis = calDir+galaxy+'_'+band+'_'+cont+'_'+arrays_str+'_sci.ms'
    concat(vis=outputvises, concatvis=concatvis) 

stop = time.time()
count(stop, start)
