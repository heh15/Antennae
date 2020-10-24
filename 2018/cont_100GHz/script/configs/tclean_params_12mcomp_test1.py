testversions = 'noflag_nobin_fixmask'

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
imageDir = Dir + 'image/'
calDir = Dir + 'calibrated/'
regionDir = Dir + 'regions/'
maskDir = Dir + 'mask/'

par_tclean = {}

par_tclean['vis'] = calDir + 'ngc4038_band3_cont_12mcomp_noflag_nobin_sci.ms'
par_tclean['imagename'] = imageDir + 'ngc4038_band3_cont_12mcomp'+'_'+testversions
par_tclean['phasecenter'] = 'J2000 12h01m53.1912 -18d52m29.7759'
par_tclean['specmode'] = 'mfs'
par_tclean['imsize'] = [540, 588]
par_tclean['outframe'] = 'Bary' # default
par_tclean['cell'] = '0.32arcsec'
par_tclean['weighting'] = 'briggs' # default
par_tclean['robust'] = 0.0 # default
par_tclean['deconvolver'] = 'hogbom' # default
par_tclean['gridder'] = 'mosaic'
par_tclean['niter'] = 10000
par_tclean['cyclefactor'] = 1.0 # default
par_tclean['pblimit'] = 0.2 # default
par_tclean['interactive'] = False  # default
par_tclean['threshold'] = 0.0
par_tclean['threshold_ratio'] = 2.0 # S/N cut ratio. 

### spw to be used
par_tclean['spw'] = '0:854~1222;1540~1911,1:4~228;274~491;770~951,2:13~469,3:8~466' 

### mask to be used 
par_tclean['usemask'] = 'user'
par_tclean['mask'] = maskDir + 'member.uid___A001_X133d_X967.NGC4038_sci.spw25_27_29_31.cont.I.mask.fits'

# auto-multhresh par_tclean for 12m short base line continuum. 
par_tclean['sidelobethreshold'] = 2.0
par_tclean['noisethreshold'] = 4.25
par_tclean['lownoisethreshold'] = 1.5
par_tclean['minbeamfrac'] = 0.3
par_tclean['negativethreshold'] = 0.0
