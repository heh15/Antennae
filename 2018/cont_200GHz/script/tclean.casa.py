import copy
from collections import OrderedDict

############################################################
# directory

Dir = '/home/heh15/research/Antennae/2018/cont_200GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'
regionDir = Dir + 'regions/'


############################################################
# basic parameters. 

'''
To add a parameter to tclean for specific dataset, 
first add the default value of the parameter to the default dictionary.
Then add the private value to the parameter dictionary. 
In future, there should be a complete list of tclean parameters. 
'''

arrays = ['12mcomp', '7m', '12mcomp_7m', '12m_7m', '12mext']
do_dirty = False
parallel = False

parameters = dict.fromkeys(arrays)
statistic = dict.fromkeys(arrays)

for key in arrays:
    parameters[key] = {}
    statistic[key] = {}

### import parameters
sys.path.append('configs')

# import the parameters from 12m compact array. 
from tclean_params_12mcomp import *
parameters['12mcomp'] = copy.deepcopy(par_tclean)  

# import parameters from 12m extended array
from tclean_params_12mext import *
parameters['12mext'] = copy.deepcopy(par_tclean)

# import parameters for 7m array
from tclean_params_7m import *
parameters['7m'] = copy.deepcopy(par_tclean)

# import parameters for 12m_7m array
from tclean_params_12m_7m import *
parameters['12m_7m'] = copy.deepcopy(par_tclean)

############################################################
# main program 

start=time.time()

# test
arrays = ['12m_7m']

for key in arrays:
    # first dirty clean the cube 
    delmod(vis = parameters[key]['vis'])
    tclean(vis = parameters[key]['vis'],
           imagename = parameters[key]['imagename'], 
           phasecenter = parameters[key]['phasecenter'], 
           specmode = parameters[key]['specmode'],
           spw = parameters[key]['spw'], 
           outframe = parameters[key]['outframe'],
           cell = parameters[key]['cell'],
           imsize = parameters[key]['imsize'], 
           weighting = parameters[key]['weighting'], 
           robust = parameters[key]['robust'],
           deconvolver = parameters[key]['deconvolver'], 
           gridder = parameters[key]['gridder'], 
           niter = 0, 
           cyclefactor = parameters[key]['cyclefactor'], 
           pblimit = parameters[key]['pblimit'], 
           interactive = parameters[key]['interactive'],
	   parallel = parallel)
        
    # measure the rms and record the value.
    imagename = parameters[key]['imagename']+'.image'
    statistic[key]['rms'] = imstat(imagename = imagename, region = regionDir+'rmsMeasure.crtf')['rms'][0]
    parameters[key]['threshold'] = parameters[key]['threshold_ratio']*statistic[key]['rms']
#   parameters[key]['threshold'] = 6.7e-5 # rms for 12mext_spw29.
    
    if do_dirty == True: 
	continue

    delmod(vis = parameters[key]['vis'])

    # second cleaning using auto-multithresh. 
    tclean(vis = parameters[key]['vis'],
           imagename = parameters[key]['imagename'], 
           phasecenter = parameters[key]['phasecenter'], 
           specmode = parameters[key]['specmode'],
           spw = parameters[key]['spw'], 
           outframe = parameters[key]['outframe'],
           cell = parameters[key]['cell'],
           imsize = parameters[key]['imsize'], 
           weighting = parameters[key]['weighting'], 
           robust = parameters[key]['robust'],
           deconvolver = parameters[key]['deconvolver'], 
           gridder = parameters[key]['gridder'], 
           niter = parameters[key]['niter'], 
           threshold = parameters[key]['threshold'], 
           cyclefactor = parameters[key]['cyclefactor'], 
           pblimit = parameters[key]['pblimit'], 
           interactive = parameters[key]['interactive'], 
           usemask = parameters[key]['usemask'],
           mask = parameters[key]['mask'],
           sidelobethreshold = parameters[key]['sidelobethreshold'], 
           noisethreshold = parameters[key]['noisethreshold'], 
           lownoisethreshold = parameters[key]['lownoisethreshold'], 
           minbeamfrac = parameters[key]['minbeamfrac'], 
           negativethreshold = parameters[key]['negativethreshold'],
	   parallel = parallel)

    impbcor(imagename= parameters[key]['imagename']+'.image', pbimage = parameters[key]['imagename']+'.pb',
            outfile = parameters[key]['imagename']+'.pbcor', overwrite=True)

stop=time.time()
dure=stop-start
m,s=divmod(dure,60)
h,m=divmod(m,60)
print("%d:%02d:%02d" %(h, m, s))


