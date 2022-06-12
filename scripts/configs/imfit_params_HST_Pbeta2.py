Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + 'HST/'


params = {}
params['imagename'] = imageDir + 'Antennae_HST_Pbeta.fits'
params['region'] = regionDir + 'source_HST_Pbeta_init2.crtf'
params['outfile'] = regionDir + 'source_HST_Pbeta_imfit2.crtf'
params['pbimage'] = ''

statistic = {}
statistic['rms'] = None
statistic['pix/beam'] = None
