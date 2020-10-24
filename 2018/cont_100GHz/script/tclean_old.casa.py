import copy
from collections import OrderedDict

############################################################
# directory

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'
regionDir = Dir + 'regions/'


vis_12m_comp = calDir + 'ngc4038_band3_cont_12mcomp_noflag_nobin_sci.ms'
vis_7m = calDir + 'ngc4038_band3_cont_7m_sci.ms'
vis_12m_ext_comp_7m = calDir + 'ngc4038_band3_cont_12mext_12mcomp_7m_sci.ms' 
vis_12m_ext = calDir + 'ngc4038_band3_cont_12mext_noflag_nobin_sci.ms'


#test 
vis_12m_ext = '/home/brunettn/antennae/2018.1.00272.S/'\
              'science_goal.uid___A001_X133d_X963/'\
                'group.uid___A001_X133d_X964/'\
                'member.uid___A001_X133d_X965/calibrated_nrao/'\
                'calibrated_final.ms'


############################################################
# format setting 

############################################################
# basic parameters. 

'''
To add a parameter to tclean for specific dataset, 
first add the default value of the parameter to the default dictionary.
Then add the private value to the parameter dictionary. 
In future, there should be a complete list of tclean parameters. 
'''
dirty_only = False
parallel = False

keywords = OrderedDict()
keywords['galaxy'] = 'ngc4038'
keywords['band'] = 'band3'
keywords['datatype'] = 'cont'
keywords['testversions'] = 'robust2_noflag_nobin'

default={}
default['spw'] = '0, 1, 2, 3' 
default['phasecenter'] = 'J2000 12h01m53.1912 -18d52m29.7759'
default['specmode'] = 'mfs'
default['imsize'] = [540, 588]
default['outframe'] = 'Bary' # default
default['cell'] = '0.32arcsec'
default['weighting'] = 'briggs' # default
default['robust'] = 0.0 # default
default['deconvolver'] = 'hogbom' # default
default['gridder'] = 'mosaic'
default['niter'] = 10000
default['cyclefactor'] = 1.0 # default
default['pblimit'] = 0.2 # default
default['interactive'] = False  # default
default['threshold'] = 0.0 
default['threshold_ratio'] = 2.0 # S/N cut ratio. 
default['usemask'] = 'auto-multithresh'

# auto-multhresh default for 12m short base line continuum. 
default['sidelobethreshold'] = 2.0
default['noisethreshold'] = 4.25
default['lownoisethreshold'] = 1.5
default['minbeamfrac'] = 0.3 
default['negativethreshold'] = 0.0

arrays = ['12mcomp', '7m', '12mcomp_7m', '12m_7m', '12m_ext']

parameters = dict.fromkeys(arrays)
statistic = dict.fromkeys(arrays)

for key in arrays:
    parameters[key] = copy.deepcopy(default)
    statistic[key] = {}


# personal edit for 12m compact array parameters. 
# beamsize, 2.601, 1.769, 86.838

parameters['12mcomp']['vis'] = vis_12m_comp

galaxy = keywords['galaxy']
band = keywords['band']
cont = keywords['datatype']

imagename = imageDir
for key in keywords:
    imagename = imagename + keywords[key] + '_'
imagename = imagename+ '12mcomp'
parameters['12mcomp']['imagename'] = imagename 
parameters['12mcomp']['spw'] = '0:854~1222;1540~1911,1:4~228;274~491;770~951,2:13~469,3:8~466'
parameters['12mcomp']['robust'] = 2.0


# personal edit for 7m array parameters. 
parameters['7m']['vis'] = vis_7m

parameters['7m']['sidelobethreshold'] = 1.25
parameters['7m']['noisethreshold'] = 5.0
parameters['7m']['lownoisethreshold'] = 2.0
parameters['7m']['minbeamfrac'] = 0.1


# personal edit for 12m extended array

parameters['12m_ext']['vis'] = vis_12m_ext

imagename = imageDir
for key in keywords:
    imagename = imagename + keywords[key] + '_'
imagename = imagename+ '12m_ext'
parameters['12m_ext']['imagename'] = imagename

parameters['12m_ext']['sidelobethreshold'] = 3.0
parameters['12m_ext']['noisethreshold'] = 5.0
parameters['12m_ext']['lownoisethreshold'] = 1.5
parameters['12m_ext']['minbeamfrac'] = 0.3

parameters['12m_ext']['cell'] = '0.084arcsec'
parameters['12m_ext']['imsize'] = [2048, 2240]

# parameters['12m_ext']['spw'] = '0:790~806;882~1275;1497~1914,1:11~670;773~952,2:3~474,3:5~474'
parameters['12m_ext']['spw'] = '2:3~474'
parameters['12m_ext']['spw'] = '29:3~474'

# personal edit for 12m+7m array parameters
parameters['12m_7m']['vis'] = vis_12m_ext_comp_7m

imagename = imageDir
for key in keywords:
    imagename = imagename + keywords[key] + '_'
imagename = imagename+ '12m_7m'
parameters['12m_7m']['imagename'] = imagename

parameters['12m_7m']['spw'] = '0~11'

parameters['12m_7m']['sidelobethreshold'] = 3.0
parameters['12m_7m']['noisethreshold'] = 5.0
parameters['12m_7m']['lownoisethreshold'] = 1.5
parameters['12m_7m']['minbeamfrac'] = 0.3

parameters['12m_7m']['cell'] = '0.084arcsec'
parameters['12m_7m']['imsize'] = [2048, 2240]

############################################################
# main program 

start=time.time()

# test
arrays = ['12mcomp']

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
    
    if dirty_only == True: 
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


