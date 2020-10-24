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

###########################################################
# basic parameters

ratio = 2.0

bands = ['band 3', 'band 6', 'band3_2016', 'band3_2016_p5', 'band7_2016']
continuum = dict.fromkeys(bands)
statistics = dict.fromkeys(bands)

for band in bands:
    statistics[band] = {}

# band 3 image parameters for 2018 data
continuum['band 3'] = {}
continuum['band 3']['imagename'] = imagefile_band3
continuum['band 3']['region'] = sourcefile_band3
continuum['band 3']['outfile'] = regionDir + 'source_band3_imfit.crtf'
continuum['band 3']['pbimage'] = imageDir_band3 + 'ngc4038_band3_cont_12m_7m.pb' 

statistics['band 3']['rms'] = 1.2e-5
statistics['band 3']['pix/beam'] = 40

# band 6 image parameters for 2018 data. 
continuum['band 6'] = {}
continuum['band 6']['imagename'] = imagefile_band6
continuum['band 6']['region'] = sourcefile_band6
continuum['band 6']['outfile'] = regionDir + 'source_band6_imfit.crtf'
continuum['band 6']['pbimage'] = imageDir_band6 + 'ngc4038_band6_cont_12m_7m.pb' 

statistics['band 6']['rms'] = 5.3e-5
statistics['band 6']['pix/beam'] = 77

# parameters for 2016 data in band 3. 
continuum['band3_2016'] = {}
continuum['band3_2016']['imagename'] = imagefile_band3_2016
continuum['band3_2016']['region'] = sourcefile_band3_2016
continuum['band3_2016']['outfile'] = regionDir + 'source_band3_2016_imfit.crtf'
continuum['band3_2016']['pbimage'] = imageDir_band3_2016 + 'ngc40389overlap_band3_uvrange_robust_2.pb' 

statistics['band3_2016']['rms'] = 1.4e-5
statistics['band3_2016']['pix/beam'] = 90

# parameters for 2016 data in band 3 but with higher resolution
sys.path.append('configs')
import copy

from fluxMeasure_parames_band3_2016_p5 import params, statistic
continuum['band3_2016_p5'] = copy.deepcopy(params)
statistics['band3_2016_p5'] = copy.deepcopy(statistic)

# parameters for 2015 data in band 7. 
from fluxMeasure_params_band7_2016 import params, statistic
continuum['band7_2016'] = copy.deepcopy(params)
statistics['band7_2016'] = copy.deepcopy(statistic)

###########################################################
# functions

def beam_get(imagename, region_init, ratio=2.0):
    ''' 
    parameters
    imagename: The path to the CASA image file
    regions: The path to the CASA region file or the CASA 
    region string. 
    ratio: The ratio to be multiplied by the fitted ellipse to 
    get the final elliptical aperture shape. 
    ''' 
    beam=imfit(imagename=imagename,region=region_init)
    x_value=beam['results']['component0']['shape']\
             ['direction']['m0']['value']
    y_value=beam['results']['component0']['shape']\
             ['direction']['m1']['value']
    bmaj_value=beam['results']['component0']\
                ['shape']['majoraxis']['value']
    bmin_value=beam['results']['component0']['shape']\
                ['minoraxis']['value']
    pa_value=beam['results']['component0']['shape']\
              ['positionangle']['value']
    x=str(x_value)+'rad'
    y=str(y_value)+'rad'
    bmaj=str(bmaj_value/2.0*ratio)+'arcsec'
    bmin=str(bmin_value/2.0*ratio)+'arcsec'
    pa=str(pa_value)+'deg'
    region='ellipse[['+x+','+y+'],['+bmaj+','+bmin+'],'+pa+']'

    return region

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

bands = ['band 3', 'band3_2016', 'band3_2016_p5', 'band7_2016']

for band in bands:
    regions = []
    with open(continuum[band]['region'], 'r') as infile:
        line = infile.readline()
        while line !='':
            line = infile.readline()
            regions.append(line)
    regions.remove('')

    # fit different regions with 2D Gaussian function and decide 
    # the aperture size to measure the flux. 
    fittedRegions = []
    for region in regions:       	
        fittedRegion = beam_get(continuum[band]['imagename'], region, ratio=ratio)
        fittedRegions.append(fittedRegion)

    # Export the regions into a file. 
    with open (continuum[band]['outfile'], 'w') as outfile:
        outfile.write('#CRTFv0 CASA Region Text Format version 0\n')
        for line in fittedRegions:
            outfile.write(line+'\n')

for band in bands:
    if band == 'band7_2016':
        regionband = 'band3_2016'
    else: 
        regionband = band 
    with open (continuum[regionband]['outfile'], 'r') as infile:
        fittedRegions = infile.readlines()
    fittedRegions.pop(0)
    fittedRegions = [line.strip('\n') for line in fittedRegions]
    
    # get the statistics for different regions. 
    statistics[band]['flux'] = []
    statistics[band]['flux uncertainty'] = []
    statistics[band]['peak intensity'] = []
    for fittedRegion in fittedRegions:
        stats_all = imstat(imagename=continuum[band]['imagename'],
                                region=fittedRegion)
        if len(stats_all['flux']) == 0:
            print('region ' + fittedRegion + ' is not in the field')
            statistics[band]['flux'].append(np.nan)
            statistics[band]['peak intensity'].append(np.nan)
            statistics[band]['flux uncertainty'].append(np.nan)
            continue            
        flux = stats_all['flux'][0]
        peak = stats_all['max'][0]
        rms = statistics[band]['rms']
        pix_num = stats_all['npts'][0]
        pix_pbeam = statistics[band]['pix/beam']
        try:
            pbcor = imstat(imagename=continuum[band]['pbimage'], 
                        region=fittedRegion)['median'][0]
        except IndexError: 
            pbcor = np.nan
        flux_uncertainty = rms/pbcor*sqrt(pix_num/pix_pbeam)
        statistics[band]['flux'].append(round_sig(flux*1000))
        statistics[band]['peak intensity'].append(round_sig(peak*1000))
        statistics[band]['flux uncertainty'].append(round_sig(flux_uncertainty*1000, sig=1))

    statistics[band]['rms'] = statistics[band]['rms']*1000 

# change the order of measurement to compare with results read manually. 
bands = ['band3_2016', 'band3_2016_p5', 'band7_2016']
quantities = ['flux', 'flux uncertainty', 'peak intensity']
for band in bands:
    for quantity in quantities: 
        statistics[band][quantity] = band3_2016_sort(statistics[band][quantity])

# Add the measurement for region 6, which only has the band 7 detection
bands = ['band3_2016', 'band7_2016']
with open (continuum['band7_2016']['outfile']) as infile:
    infile.readline()
    fittedRegion = infile.readline()

for band in bands:
    stats_all = imstat(imagename=continuum[band]['imagename'], 
                       region = fittedRegion)
    flux = stats_all['flux'][0]
    peak = stats_all['max'][0]
    rms = statistics[band]['rms']
    pix_num = stats_all['npts'][0]
    pix_pbeam = statistics[band]['pix/beam']
    pbcor = imstat(imagename=continuum[band]['pbimage'],
                    region=fittedRegion)['median'][0]
    flux_uncertainty = rms/pbcor*sqrt(pix_num/pix_pbeam)
    statistics[band]['flux'].insert(6, round_sig(flux*1000))
    statistics[band]['peak intensity'].insert(6, round_sig(peak*1000))
    statistics[band]['flux uncertainty'].insert(6, round_sig(flux_uncertainty, sig=1))

