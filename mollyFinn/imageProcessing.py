immoments(imagename='Ant_B7_Combined_12CO3_2_reduceVel.cube.fits', includepix=[3.2e-3, 100], chans='0~80', outfile='Antennae_12CO32.mom0')

immoments(imagename='Ant_B6high_Combined_12CO2_1.cube.image.fits', includepix=[1.2e-3, 100], chans='5~90', outfile='Antennae_12CO21.mom0')

# export to fits file
exportfits(imagename='Antennae_12CO21.mom0', fitsimage='Antennae_12CO21_mom0.fits')

# do primary beam correction for co 2-1
impbcor(imagename='Ant_B6high_Combined_12CO2_1.cube.image.fits', 
        pbimage='Ant_B6high_Combined_12CO2_1.cube.pb.fits', 
        outfile='Ant_B6high_Combined_12CO2_1.cube.pbcor')
exportfits(imagename='Ant_B6high_Combined_12CO2_1.cube.pbcor', 
            fitsimage='Ant_B6high_Combined_12CO2_1.cube.pbcor.fits', 
            overwrite=True)

# do moment 0 map for the co2-1 cube
immoments(imagename='Ant_B6high_Combined_12CO2_1.cube.pbcor', includepix=[1.2e-3, 100], chans='5~90', outfile='Antennae_12CO21_pbcor.mom0')


# collapse the primary beam cube
immoments(imagename='Ant_B6high_Combined_12CO2_1.cube.pb.fits', moments=8, outfile='Ant_B6high_Combined_12CO2_1.mom8.pb')

# do primary beam correction for co 3-2
impbcor(imagename='Ant_B7_Combined_12CO3_2_reduceVel.cube.fits', 
        pbimage='Ant_B7_Combined_12CO3_2_reduceVel.cube.pb.fits', 
        outfile='Ant_B7_Combined_12CO3_2_reduceVel.cube.pbcor')

# collapse the pb cube
immoments(imagename='Ant_B7_Combined_12CO3_2_reduceVel.cube.pb.fits', moments=8, outfile='Ant_B7_Combined_12CO3_2_reduceVel.mom8.pb')

# do primary beam correction for co 3-2 moment 0 maps
impbcor(imagename='Antennae_12CO32.mom0', 
        pbimage='Ant_B7_Combined_12CO3_2_reduceVel.mom8.pb', 
        outfile='Antennae_12CO32_pbcor.mom0')
