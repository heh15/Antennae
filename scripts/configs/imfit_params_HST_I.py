Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + 'HST/'


params = {}
params['imagename'] = imageDir + 'Antennae_HST_I.fits'
params['region'] = regionDir + 'source_HST_I_init.crtf'
params['outfile'] = regionDir + 'source_HST_I_imfit.crtf'
params['pbimage'] = ''

statistic = {}
statistic['rms'] = None
statistic['pix/beam'] = None
