Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + '2016/Band3/'


params = {}
params['imagename'] = imageDir + 'ngc40389overlap_band3_uvrange_robust_2_smooth_p201.pbcor/'
params['region'] = regionDir + 'source_band3_2016_init_p201.crtf'
params['outfile'] = regionDir + 'source_band3_2016_imfit_p201.crtf'
params['pbimage'] = imageDir + 'ngc40389overlap_band3_uvrange_robust_p5.pb'

statistic = {}
statistic['rms'] = 2.3e-5
statistic['pix/beam'] = 1.1331*0.201*0.201/0.015**2
