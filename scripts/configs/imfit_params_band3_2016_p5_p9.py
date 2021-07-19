Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + '2016/Band3/'


params = {}
params['imagename'] = imageDir + 'ngc40389overlap_band3_uvrange_robust_p5_smooth_090.pbcor'
params['region'] = regionDir + 'source_band3_2016_init_contour.crtf'
params['outfile'] = regionDir + 'source_band3_2016_p5_imfit_smooth_p9.crtf'
params['pbimage'] = imageDir + 'ngc40389overlap_band3_uvrange_robust_p5.pb'

statistic = {}
statistic['rms'] = 1.5e-5
statistic['pix/beam'] = 1.1331*0.09*0.09/0.015**2
