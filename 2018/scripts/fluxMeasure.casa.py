###########################################################
# directories

Dir = '/home/heh15/research/Antennae/2018/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir_band3 = Dir + 'cont_100GHz/image/'
imageDir_band6 = Dir + 'cont_200GHz/image/'

sourcefile_band3 = regionDir + 'source_band3.crtf'
imagefile_band3 = imageDir_band3 + 'ngc4038_band3_cont_12m_7m.pbcor'

sourcefile_band6 = regionDir + 'source_band6.crtf'
imagefile_band6 = imageDir_band6 + 'ngc4038_band6_cont_12m_7m.pbcor' 

###########################################################
# basic parameters

ratio = 1.0

bands = ['band 3', 'band 6']
continuum = dict.fromkeys(bands)

# band 3 image parameters
continuum['band 3'] = {}
continuum['band 3']['imagename'] = imagefile_band3
continuum['band 3']['region'] = sourcefile_band3
continuum['band 3']['outfile'] = regionDir + 'source_band3_imfit.crtf'

# band 6 image parameters
continuum['band 6'] = {}
continuum['band 6']['imagename'] = imagefile_band6
continuum['band 6']['region'] = sourcefile_band6
continuum['band 6']['outfile'] = regionDir + 'source_band6_imfit.crtf'

###########################################################
# functions

def beam_get(imagename, region_init, ratio=1.0):
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
    bmaj=str(bmaj_value*ratio)+'arcsec'
    bmin=str(bmin_value*ratio)+'arcsec'
    pa=str(pa_value)+'deg'
    region='ellipse[['+x+','+y+'],['+bmaj+','+bmin+'],'+pa+']'

    return region

###########################################################
# main programs. 

bands = ['band 3']

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


