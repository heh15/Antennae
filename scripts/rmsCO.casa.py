###########################################################
# directories

Dir = '/home/heh15/research/Antennae/'
scriptDir = Dir + 'scripts/'
regionDir = Dir + 'regions/'
imageDir = Dir + 'mollyFinn/'

imagefile = imageDir + 'Ant_B6high_Combined_12CO2_1.cube.image.fits'
regionfile = regionDir + 'rmsMeasure_co21.crtf'

###########################################################
# main program

rms = imstat(imagename=imagefile, region=regionfile)['rms'][0]

