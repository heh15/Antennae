###########################################################
# directories

Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir_band3 = Dir + '2018/cont_100GHz/image/'
imageDir_band6 = Dir + '2018/cont_200GHz/image/'
imageDir_band3_2016 = Dir + '2016/Band3/'

sourcefile_band3 = regionDir + 'source_band3.crtf'
imagefile_band3 = imageDir_band3 + 'ngc4038_band3_cont_12m_7m.pbcor'

sourcefile_band6 = regionDir + 'source_band6.crtf'
imagefile_band6 = imageDir_band6 + 'ngc4038_band6_cont_12m_7m.pbcor' 

sourcefile_band3_2016 = regionDir + 'starcluster_band3_2016.crtf'
imagefile_band3_2016 = imageDir_band3_2016 + \
                       'ngc40389overlap_band3_uvrange_robust_2_smooth.pbcor'

imagefile_co = Dir + 'mollyFinn/antennae_CO21_firecracker_2sig.mom0'

###########################################################
# basic parameters


bands = ['band 3', 'band 6', 'band3_2016', 'band3_2016_p5', 'band7_2016', 'band7_2016_p5',
        'band3_2016_p5_p9']
continuum = dict.fromkeys(bands)
statistics = dict.fromkeys(bands)

for band in bands:
    statistics[band] = {}

# band 3 image parameters for 2018 data
continuum['band 3'] = {}
continuum['band 3']['imagename'] = imagefile_band3
continuum['band 3']['region'] = regionDir + 'source_band3_imfit.crtf'
continuum['band 3']['pbimage'] = imageDir_band3 + 'ngc4038_band3_cont_12m_7m.pb' 

statistics['band 3']['rms'] = 1.2e-5
statistics['band 3']['pix/beam'] = 40

# band 6 image parameters for 2018 data. 
continuum['band 6'] = {}
continuum['band 6']['imagename'] = imagefile_band6
continuum['band 6']['region'] = regionDir + 'source_band3_imfit.crtf'
continuum['band 6']['pbimage'] = imageDir_band6 + 'ngc4038_band6_cont_12m_7m.pb' 

statistics['band 6']['rms'] = 5.3e-5
statistics['band 6']['pix/beam'] = 77

# parameters for 2016 data in band 3. 
continuum['band3_2016'] = {}
continuum['band3_2016']['imagename'] = imagefile_band3_2016
continuum['band3_2016']['region'] = regionDir + 'source_band3_2016_imfit.crtf'
continuum['band3_2016']['pbimage'] = imageDir_band3_2016 + 'ngc40389overlap_band3_uvrange_robust_2.pb' 

statistics['band3_2016']['rms'] = 1.4e-5
statistics['band3_2016']['pix/beam'] = 90

# parameters for 2016 data in band 3 but with higher resolution
sys.path.append('configs')
import copy

from fluxMeasure_parames_band3_2016_p5 import params, statistic
continuum['band3_2016_p5'] = copy.deepcopy(params)
statistics['band3_2016_p5'] = copy.deepcopy(statistic)

# parameters for 2016 data in band 3, robust = 0.5, 0.09 arcsec beam.
from fluxMeasure_params_band3_2016_p5_p9 import params, statistic 
continuum['band3_2016_p5_p9'] = copy.deepcopy(params)
statistics['band3_2016_p5_p9'] = copy.deepcopy(statistic)

# parameters for 2016 data in band 7. 
from fluxMeasure_params_band7_2016 import params, statistic
continuum['band7_2016'] = copy.deepcopy(params)
statistics['band7_2016'] = copy.deepcopy(statistic)

# parameters for 2016 data in band 7 with robust=0.5
from fluxMeasure_params_band7_2016_p5 import params, statistic
continuum['band7_2016_p5'] = copy.deepcopy(params)
statistics['band7_2016_p5'] = copy.deepcopy(statistic)


###########################################################
# functions

def measure_flux(linedict, statdict, measure_cube=False,
                chans = '0', chan_num = 0, pbimage=''):
    with open (linedict['region'], 'r') as infile:
        fittedRegions = infile.readlines()
    
    fittedRegions.pop(0)
    fittedRegions = [line.strip('\n') for line in fittedRegions]

    # get the statistics for different regions.
    result = {} 
    result['flux'] = []
    result['flux uncertainty'] = []
    result['peak intensity'] = []
    result['pbcor'] = []

    for i in range(len(fittedRegions)):
        fittedRegion = fittedRegions[i]

        if measure_cube == True:
            stats_all = imstat(imagename=linedict['imagename'],
                                region=fittedRegion, chans=chans[i])
            rms = statdict['rms'] * np.sqrt(chan_num[i]/80.0)
        else:
            stats_all = imstat(imagename=linedict['imagename'],
                                region=fittedRegion)
            rms = statdict['rms']

        if (stats_all is None) or (len(stats_all['flux'])==0):
            print('region '+ fittedRegion + ' is outside the field of view')
            result['flux'].append(np.nan)
            result['peak intensity'].append(np.nan)
            result['flux uncertainty'].append(np.nan)
            result['pbcor'].append(np.nan)
            continue

        # the pb correction value for each aperture
        if pbimage == '':
            pbcor = 1
        else:
            pbcor = imstat(imagename=pbimage, 
                           region=fittedRegion)['mean'][0]

        flux = stats_all['flux'][0]
        peak = stats_all['max'][0]
        pix_num = stats_all['npts'][0]
        pix_pbeam = statdict['pix/beam']
        flux_uncertainty = rms/pbcor*sqrt(pix_num/pix_pbeam)
        result['flux'].append(round_sig(flux))
        result['peak intensity'].append(round_sig(peak))
        result['flux uncertainty'].append(round_sig(flux_uncertainty, sig=1))
        result['pbcor'].append(round_sig(pbcor, sig=2))   
     
    return result


from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def band3_2016_sort(lst):
    lst = lst[1:] + lst[0:1]
    lst = lst[:1] + lst[4:5] + lst[1:4:] + lst[5:]
    lst = lst[:3] + lst[5:7] + lst[3:5] + lst[7:]
    
    return lst


###########################################################
# main programs. 

bands = ['band 3', 'band 6', 'band3_2016', 'band3_2016_p5', 'band7_2016', 
         'band7_2016_p5', 'band3_2016_p5_p9']

for band in bands:
    result = measure_flux(continuum[band], statistics[band], 
                          pbimage=continuum[band]['pbimage'])
    statistics[band].update(result)
    statistics[band]['flux'] = [i * 1000 for i in statistics[band]['flux']]
    statistics[band]['flux uncertainty'] = [i * 1000 for i in 
                                           statistics[band]['flux uncertainty']]
    statistics[band]['peak intensity'] = [i * 1000 for i in 
                                         statistics[band]['peak intensity']]                                            

# add the measurement for band7 apertures. 
# update the region file. 

bands = ['band3_2016', 'band7_2016']
for band in bands:
    continuum[band]['region'] = regionDir + 'source_band7_2016_imfit.crtf'

bands = ['band3_2016_p5', 'band7_2016_p5', 'band3_2016_p5_p9']
for band in bands:
    continuum[band]['region'] = regionDir + 'source_band7_2016_imfit_p5.crtf'

# measure the flux
bands = ['band3_2016', 'band7_2016', 'band3_2016_p5', 'band7_2016_p5', 
        'band3_2016_p5_p9']
for band in bands: 
    result = measure_flux(continuum[band], statistics[band], 
                            pbimage=continuum[band]['pbimage'])
    statistics[band]['flux'].insert(6, result['flux'][0] * 1000)
    statistics[band]['peak intensity'].insert(6, 
                    result['peak intensity'][0] * 1000)
    statistics[band]['flux uncertainty'].insert(6, 
                    result['flux uncertainty'][0] * 1000)
    statistics[band]['pbcor'].insert(6, result['pbcor'][0])

# add the measurement for sources that broken apart
# update the regions file
bands = ['band3_2016_p5_p9']
for band in bands: 
    continuum[band]['region'] = regionDir + 'source_band3_multiple_imfit.crtf'

# measure the flux
for band in bands:
    result = measure_flux(continuum[band], statistics[band], 
                          pbimage=continuum[band]['pbimage'])
    for key in ['flux', 'peak intensity', 'flux uncertainty']:
        result[key] = (np.array(result[key])*1000).tolist()
    statistics[band]['flux'] = statistics[band]['flux'] + result['flux']
    statistics[band]['peak intensity'] += result['peak intensity']
    statistics[band]['flux uncertainty'] += result['flux uncertainty']
    statistics[band]['pbcor'] += result['pbcor']
