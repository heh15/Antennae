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

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'

vis_12m_ext = '/home/brunettn/antennae/2018.1.00272.S/'\
	      'science_goal.uid___A001_X133d_X963/'\
		'group.uid___A001_X133d_X964/'\
		'member.uid___A001_X133d_X965/calibrated_nrao/'\
		'calibrated_final.ms' 

vis_12m_comp = '/home/brunettn/antennae/2018.1.00272.S/'\
               'science_goal.uid___A001_X133d_X963/'\
               'group.uid___A001_X133d_X964/'\
               'member.uid___A001_X133d_X967/calibrated_nrao/'\
               'calibrated_final.ms'
vis_7m = '/home/brunettn/antennae/2018.1.00272.S/'\
         'science_goal.uid___A001_X133d_X963/'\
         'group.uid___A001_X133d_X964/member.uid___A001_X133d_X969/'\
         'calibrated_nrao/calibrated_final.ms'

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

do_concat = False

keywords = {}
keywords['galaxy'] = 'ngc4038'
keywords['band'] = 'band3'
keywords['datatype'] = 'cont'
keywords['testversion'] = 'noflag_nobin'

# default setting for 12m compact array.
default={}
default['spw'] = '25, 27, 29, 31'
default['field'] = 'NGC4038'
# default['lines_to_flag'] = ['co10', 'cn10high', 'cn10low', 'hc3n1110']
default['lines_to_flag'] = [] # no lines to flage. 
default['vsys'] = 1550.0
default['vwidth'] = 685
default['do_statwt'] = False
default['do_collapse'] = False
default['collapse_width'] = [128, 64, 32, 32]

arrays = ['12mext', '12mcomp', '7m']

parameters = dict.fromkeys(arrays)
for key in arrays:
    parameters[key] = copy.deepcopy(default)

# personal edit for 12m extented array parameters. 
parameters['12mext']['vis'] = vis_12m_ext
# parameters['12mext']['spw'] = '25:790~806;882~1275;1497~1914,27:11~670;773~952,29:3~474,31:5~474' 

# personal edit for 12m compact array parameters. 
parameters['12mcomp']['vis'] = vis_12m_comp

# personal edit for 7m array parameters. 
parameters['7m']['vis'] = vis_7m
parameters['7m']['spw'] = '16, 18, 20, 22'

############################################################
# main program 

arrays = ['12mcomp']

start = time.time()

outputvises = []
for key in arrays:
    # split the calibrated data and place it into the folder, try 12m compact and 7m first. 
    galaxy = keywords['galaxy']
    band = keywords['band']
    cont = keywords['datatype']
    test = keywords['testversion']
    vis = parameters[key]['vis']
    outputvis = calDir+galaxy+'_'+band+'_'+cont+'_'+key+'_'+test+'_sci.ms'
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
    arrays_str = '_'.join(arrays)
    concatvis = calDir+galaxy+'_'+band+'_'+cont+'_'+arrays_str+'_sci.ms'
    concat(vis=outputvises, concatvis=concatvis) 

stop = time.time()
count(stop, start)
