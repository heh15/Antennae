testversions = ''

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'
regionDir = Dir + 'regions/'

par_tclean = {}

par_tclean['vis'] = calDir+'ngc4038_band3_cont_7m.ms'
par_tclean['imagename'] = imageDir + 'ngc4038_band3_cont_7m'+testversions
par_tclean['phasecenter'] = 'J2000 12h01m53.1912 -18d52m29.7759'
par_tclean['specmode'] = 'mfs'
par_tclean['imsize'] = [150, 160]
par_tclean['outframe'] = 'Bary' # default
par_tclean['cell'] = '1.5arcsec'
par_tclean['weighting'] = 'briggs' # default
par_tclean['robust'] = 0.5
par_tclean['deconvolver'] = 'hogbom' # default
par_tclean['gridder'] = 'mosaic'
par_tclean['niter'] = 10000
par_tclean['cyclefactor'] = 1.0 # default
par_tclean['pblimit'] = 0.2 # default
par_tclean['interactive'] = False  # default
par_tclean['threshold'] = 0.0
par_tclean['threshold_ratio'] = 2.0 # S/N cut ratio. 
par_tclean['usemask'] = 'auto-multithresh'

par_tclean['mask'] = ''

# spws used for tclean. 
par_tclean['spw'] = ''

# auto-multhresh par_tclean for 12m short base line continuum. 
par_tclean['sidelobethreshold'] = 1.25
par_tclean['noisethreshold'] = 5.0
par_tclean['lownoisethreshold'] = 2.0
par_tclean['minbeamfrac'] = 0.1
par_tclean['negativethreshold'] = 0.0

