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
# basic settings

ratio = 2.0

bands = ['band 3', 'band 6', 'band3_2016', 'band3_2016_p5', 'band7_2016', 'band7_2016_p5',
        'band3_2016_p5_p9', 'band3_p9_multiple']
continuum = dict.fromkeys(bands)

# band 3 image parameters for 2018 data
continuum['band 3'] = {}
continuum['band 3']['imagename'] = imagefile_band3
continuum['band 3']['region'] = sourcefile_band3
continuum['band 3']['outfile'] = regionDir + 'source_band3_imfit.crtf'
continuum['band 3']['pbimage'] = imageDir_band3 + 'ngc4038_band3_cont_12m_7m.pb'

# band 6 image parameters for 2018 data. 
continuum['band 6'] = {}
continuum['band 6']['imagename'] = imagefile_band6
continuum['band 6']['region'] = sourcefile_band6
continuum['band 6']['outfile'] = regionDir + 'source_band3_imfit.crtf'
continuum['band 6']['pbimage'] = imageDir_band6 + 'ngc4038_band6_cont_12m_7m.pb'

# parameters for 2016 data in band 3. 
continuum['band3_2016'] = {}
continuum['band3_2016']['imagename'] = imagefile_band3_2016
continuum['band3_2016']['region'] = sourcefile_band3_2016
continuum['band3_2016']['outfile'] = regionDir + 'source_band3_2016_imfit.crtf'
continuum['band3_2016']['pbimage'] = imageDir_band3_2016 + 'ngc40389overlap_band3_uvrange_robust_2.pb'

# parameters for 2016 data in band 3 but with higher resolution
sys.path.append('configs')
import copy

from imfit_params_band3_2016_p5 import params
continuum['band3_2016_p5'] = copy.deepcopy(params)

# parameters for 2015 data in band 7. 
from imfit_params_band7_2016 import params
continuum['band7_2016'] = copy.deepcopy(params)

# parameters for 2016 data in band 7 with robust=0.5
from imfit_params_band7_2016_p5 import params
continuum['band7_2016_p5'] = copy.deepcopy(params)


# parameters for 2016 data in band 3, robust 0.5, smoothed to 0.9 arcsec
from imfit_params_band3_2016_p5_p9 import params
continuum['band3_2016_p5_p9'] = copy.deepcopy(params)

# Fit the source thant broken into multiple sources in Band3 2016 image 
# with resolution of 0.9 arcsec. 

from imfit_params_multiple import params
continuum['band3_p9_multiple'] = copy.deepcopy(params)

###########################################################
# function

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

###########################################################
# main program 

# Set the default value of the ratio. 
for band in bands:
    continuum[band]['ratio'] = ratio
    if band == 'band3_p9_multiple':
        continuum[band]['ratio'] = 1.0

bands = ['band 3', 'band3_2016', 'band3_2016_p5', 'band7_2016', 'band7_2016_p5',
        'band3_2016_p5_p9', 'band3_p9_multiple']

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
        fittedRegion = beam_get(continuum[band]['imagename'], region, 
                                ratio=continuum[band]['ratio'])
        fittedRegions.append(fittedRegion)

    # Export the regions into a file. 
    with open (continuum[band]['outfile'], 'w') as outfile:
        outfile.write('#CRTFv0 CASA Region Text Format version 0\n')
        for line in fittedRegions:
            outfile.write(line+', color=red\n')



