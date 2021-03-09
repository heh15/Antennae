import copy

###########################################################
# directories

Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imagefile_co = Dir + 'mollyFinn/Antennae_12CO21_pbcor.mom0'
imagefile_co_cube = Dir + 'mollyFinn/Ant_B6high_Combined_12CO2_1.cube.pbcor'
sourcefile_band3_2016 = regionDir + 'source_band3_2016_imfit.crtf'

###########################################################
# basic settings

bands = ['co_cube', 'co_mom0']
linedata = {}
statistics = {}
# measure the co flux
for key in bands:
    linedata[key] = {}
    statistics[key] = {}

# parameters for CO cube
linedata['co_cube']['imagename'] = imagefile_co_cube
linedata['co_cube']['region'] = sourcefile_band3_2016
linedata['co_cube']['measure_cube'] = True 

statistics['co_cube']['rms'] = 6e-4 * np.sqrt(80)
statistics['co_cube']['pix/beam'] = 63
statistics['co_cube']['chans'] = ['33~48', '38~47', '29~39', '0', '0', '14~30', '41~46', '0']
statistics['co_cube']['chan_num'] = [15, 9, 10, 0, 0, 16, 5, 0]

# parameters for CO moment 0 
linedata['co_mom0'] = copy.deepcopy(linedata['co_cube'])
linedata['co_mom0']['imagename'] = imagefile_co
linedata['co_mom0']['measure_cube'] = False

statistics['co_mom0'] = copy.deepcopy(statistics['co_cube'])
statistics['co_mom0']['chans'] = '0'
statistics['co_mom0']['chan_num'] = 0


# measurement from additional apertures. 
chans_add = ['37~48', '37~48','30~39', '0', '0', '18~31', '0', '0']
chan_num_add = [11, 11, 9, 0, 0, 13, 0, 0]

###########################################################
# functions

from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def band3_2016_sort(lst):
    lst = lst[1:] + lst[0:1]
    lst = lst[:1] + lst[4:5] + lst[1:4:] + lst[5:]
    lst = lst[:3] + lst[5:7] + lst[3:5] + lst[7:]
    
    return lst

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

###########################################################
# main program


for band in bands:
    chans = statistics[band]['chans']
    chan_num = statistics[band]['chan_num']
    measure_cube = linedata[band]['measure_cube']
    result = measure_flux(linedata[band], statistics[band], 
                          measure_cube=measure_cube,
                          chans=chans, chan_num=chan_num)
    statistics[band].update(result)

# Add the measurement for region 6, which only has the band 7 detection
bands = ['co_cube', 'co_mom0']
regionfile = regionDir + 'source_band7_2016_imfit.crtf'
for band in bands:
    linedata[band]['region'] = regionfile
statistics['co_cube']['chans'] = ['8~28']
statistics['co_cube']['chan_num'] = [20]

for band in bands:
    chans = statistics[band]['chans']
    chan_num = statistics[band]['chan_num']
    measure_cube = linedata[band]['measure_cube']
    result = measure_flux(linedata[band], statistics[band],
                          measure_cube=measure_cube,
                          chans=chans, chan_num=chan_num)
    statistics[band]['flux'].insert(6, result['flux'][0])
    statistics[band]['peak intensity'].insert(6, result['peak intensity'][0])
    statistics[band]['flux uncertainty'].insert(6, 
                                         result['flux uncertainty'][0])

# Add the measurement for sources that broken into multiple regions. 
bands = ['co_cube', 'co_mom0']
regionfile = regionDir + 'source_band3_multiple_imfit.crtf'
for band in bands:
    linedata[band]['region'] = regionfile
statistics['co_cube']['chans'] = chans_add
statistics['co_cube']['chan_num'] = chan_num_add

for band in bands:
    chans = statistics[band]['chans']
    chan_num = statistics[band]['chan_num']
    measure_cube = linedata[band]['measure_cube']
    result = measure_flux(linedata[band], statistics[band],
                          measure_cube=measure_cube,
                          chans=chans, chan_num=chan_num)
    statistics[band]['flux'] += result['flux']
    statistics[band]['peak intensity'] += result['peak intensity']
    statistics[band]['flux uncertainty'] += result['flux uncertainty'] 
