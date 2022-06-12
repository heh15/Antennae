Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + '2016/Band7/'


params = {}
params['imagename'] = imageDir + 'ngc40389overlap_band7_range_robust_p5_smooth.pbcor'
params['region'] = regionDir + 'source_band3_2016_init_contour.crtf'
params['outfile'] = regionDir + 'source_band7_2016_imfit_p5_band3Ap.crtf'
params['pbimage'] = imageDir + 'ngc40389overlap_band7_range_robust_2.pb'

statistic = {}
statistic['rms'] = 4.1e-5
statistic['pix/beam'] = 1.1331*0.11*0.11/0.015**2

