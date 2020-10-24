###########################################################
# directories

Dir = '/home/heh15/research/Antennae/2018/cont_100GHz/'
scriptDir = Dir + 'script/'
regionDir = Dir + '../regions/'
imageDir = Dir + 'image/'

sourcefile = regionDir + 'source_band3.crtf'
imagefile = imageDir + 'ngc4038_band3_cont_12m_7m.pbcor'

###########################################################
# basic parameters

ratio = 1.0

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

regions = []
with open(sourcefile, 'r') as infile:
    line = infile.readline()
    while line !='':
        line = infile.readline()
    	regions.append(line)
regions.remove('')

# fit different regions with 2D Gaussian function and decide 
# the aperture size to measure the flux. 
fittedRegions = []
for region in regions:       	
    fittedRegion = beam_get(imagefile, region, ratio=ratio)
    fittedRegions.append(fittedRegion)

# Export the regions into a file. 
fittedSourcefile = regionDir + 'source_band3_imfit.crtf'
with open (fittedSourcefile, 'w') as outfile:
    outfile.write('#CRTFv0 CASA Region Text Format version 0\n')
    for line in fittedRegions:
	outfile.write(line+'\n')



