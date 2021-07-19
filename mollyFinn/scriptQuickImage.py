# making some CO 2-1 images for star cluster regions
# from Molly Finn's cube

# March 22, 2019

# making a quick mom0 maps 
# for purposes of submitting proposal in Cycle 7

# set channel ranges from looking at cube and integrated spectrum
# rms measured in end channels of *CLEANED PBCOR* cube
# cubes will be in main subdirectory

# estimate 0.6 mJy/beam

cube = 'Ant_B6high_Combined_12CO2_1.cube.image.fits'

immoments(imagename=cube,chans='27~54',
  includepix=[0.0012,100],outfile='antennae_CO21_firecracker_2sig.mom0')

immoments(imagename=cube,chans='35~48',
  includepix=[0.0012,100],outfile='antennae_CO21_southeast_2sig.mom0')

immoments(imagename=cube,chans='39~48',
  includepix=[0.0012,100],outfile='antennae_CO21_north_2sig.mom0')

immoments(imagename=cube,chans='17~30',
  includepix=[0.0012,100],outfile='antennae_CO21_northSE_2sig.mom0')

immoments(imagename=cube,chans='8~22',
  includepix=[0.0012,100],outfile='antennae_CO21_northSW_2sig.mom0')


# mom0 rms is 0.0006 * sqrt(10-15) * 5 km/s = 0.0095 - 0.0116 Jy/beam km/s
#  .0006 * sqrt (28) * 5 = 0.0159 Jy/beam km/s for firecracker



