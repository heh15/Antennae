exportfits(imagename='ngc40389overlap_band7_range_robust_2.image', fitsimage='ngc40389overlap_band7_range_robust_2.fits')

exportfits(imagename='ngc40389overlap_band7_range_robust_2_smooth.image', fitsimage='ngc40389overlap_band7_range_robust_2_smooth.fits')

# exportfits image for band 7 robust 2.0 pbcor image
exportfits(imagename='ngc40389overlap_band7_range_robust_2_smooth.pbcor', fitsimage='ngc40389overlap_band7_range_robust_2_smooth_pbcor.fits')

# exportfits image for band 7 pb
exportfits(imagename='ngc40389overlap_band7_range_robust_2.pb', fitsimage='ngc40389overlap_band7_range_robust_2_pb.fits')

# primary beam correction for robust 0.5 band 7 image
impbcor(imagename='ngc40389overlap_band7_range_robust_p5.image', pbimage='ngc40389overlap_band7_range_robust_p5.pb', 
        outfile = 'ngc40389overlap_band7_range_robust_p5.pbcor')

# export the Band 7 robust 0.5 smoothed image to fits file
exportfits(imagename='ngc40389overlap_band7_range_robust_p5_smooth.pbcor', 
           fitsimage='ngc40389overlap_band7_range_robust_p5_smooth_pbcor.fits', overwrite=True)

# exportfits flat image for band 7 robust 2 image
exportfits(imagename='ngc40389overlap_band7_range_robust_2_smooth.image', fitsimage='ngc40389overlap_band7_range_robust_2_smooth.fits')

# smooth the band 7 robust p5 image to the beam size of 0.134 arcsec
imsmooth(imagename='ngc40389overlap_band7_range_robust_p5.image',
         outfile='ngc40389overlap_band7_range_robust_p5_smooth_134.image',
         major='0.134arcsec',
         minor='0.134arcsec',
         pa='0deg',
         targetres=True,
         overwrite=True)
impbcor(imagename='ngc40389overlap_band7_range_robust_p5_smooth_134.image', pbimage='ngc40389overlap_band7_range_robust_p5.pb',
        outfile = 'ngc40389overlap_band7_range_robust_p5_smooth_134.pbcor', overwrite=True)

# smooth the band 7 robust 2 image to the beam size of 0.201 arcsec
imsmooth(imagename='ngc40389overlap_band7_range_robust_2_smooth.image',
        outfile='ngc40389overlap_band7_range_robust_2_smooth_p201.image',
        major='0.201arcsec',
        minor='0.201arcsec',
        pa='0deg',
        targetres=True,
        overwrite=True)
impbcor(imagename='ngc40389overlap_band7_range_robust_2_smooth_p201.image',pbimage='ngc40389overlap_band7_range_robust_2.pb',
        outfile='ngc40389overlap_band7_range_robust_2_smooth_p201.pbcor',overwrite=True)

