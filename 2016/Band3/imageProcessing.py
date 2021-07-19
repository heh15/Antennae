# Primary beam correction for robust 0.5 band 3 image
impbcor(imagename='ngc40389overlap_band3_uvrange_robust_p5.image', pbimage='ngc40389overlap_band3_uvrange_robust_p5.pb', outfile='ngc40389overlap_band3_uvrange_robust_p5.pbcor')

# exportfits image for band 3 robust 2.0 pbcor image
exportfits(imagename='ngc40389overlap_band3_uvrange_robust_2_smooth.pbcor', fitsimage='ngc40389overlap_band3_uvrange_robust_2_smooth_pbcor.fits')

# exportfits image for band 7 robust 2.0 pbcor image
exportfits(imagename='ngc40389overlap_band7_range_robust_2_smooth.pbcor', fitsimage='ngc40389overlap_band7_range_robust_2_smooth_pbcor.fits')

# exportfits image for band 3 pb
exportfits(imagename='ngc40389overlap_band3_uvrange_robust_2.pb', fitsimage='ngc40389overlap_band3_uvrange_robust_2_pb.fits')

# exportfits image for band 7 pb
exportfits(imagename='ngc40389overlap_band7_range_robust_2.pb', fitsimage='ngc40389overlap_band7_range_robust_2_pb.fits')

# primary beam correction for robust 0.5 band 7 image
impbcor(imagename='ngc40389overlap_band7_range_robust_p5.image', pbimage='ngc40389overlap_band7_range_robust_p5.pb', 
        outfile = 'ngc40389overlap_band7_range_robust_p5.pbcor')

# smooth the band 3 image to the beam size of 0.95 arcsec
imsmooth(imagename='ngc40389overlap_band3_uvrange_robust_p5.image', 
         outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_095.image',
         major='0.095arcsec',
         minor='0.095arcsec',
         pa='0deg',
         targetres=True,
         overwrite=True)
impbcor(imagename='ngc40389overlap_band3_uvrange_robust_p5_smooth_095.image', pbimage='ngc40389overlap_band3_uvrange_robust_p5.pb',
        outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_095.pbcor', overwrite=True)

# smooth the image to the beam size of 0.9 arcsec
imsmooth(imagename='ngc40389overlap_band3_uvrange_robust_p5.image',
         outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_090.image',
         major='0.090arcsec',
         minor='0.090arcsec',
         pa='0deg',
         targetres=True,
         overwrite=True)
impbcor(imagename='ngc40389overlap_band3_uvrange_robust_p5_smooth_090.image', pbimage='ngc40389overlap_band3_uvrange_robust_p5.pb',
        outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_090.pbcor', overwrite=True)

# export the smoothed image with beam size of 0.09 arcsec to fits file
exportfits(imagename='ngc40389overlap_band3_uvrange_robust_p5_smooth_090.pbcor', 
           fitsimage='ngc40389overlap_band3_uvrange_robust_p5_smooth_090_pbcor.fits', overwrite=True)

# export Band 3 smoothed image robust 0.5, 0.11 arcsec to fits file
exportfits(imagename='ngc40389overlap_band3_uvrange_robust_p5_smooth.pbcor',
           fitsimage='ngc40389overlap_band3_uvrange_robust_p5_smooth_pbcor.fits', overwrite=True)

# export the Band 7 robust 0.5 smoothed image to fits file
exportfits(imagename='ngc40389overlap_band7_range_robust_p5_smooth.pbcor', 
           fitsimage='ngc40389overlap_band7_range_robust_p5_smooth_pbcor.fits', overwrite=True)

# smooth the band 3 robust p5 image to the beam size of 0.134 arcsec 
imsmooth(imagename='ngc40389overlap_band3_uvrange_robust_p5.image',
         outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_134.image',
         major='0.134arcsec',
         minor='0.134arcsec',
         pa='0deg',
         targetres=True,
         overwrite=True)
impbcor(imagename='ngc40389overlap_band3_uvrange_robust_p5_smooth_134.image', pbimage='ngc40389overlap_band3_uvrange_robust_p5.pb',
        outfile='ngc40389overlap_band3_uvrange_robust_p5_smooth_134.pbcor', overwrite=True)

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


# exportfits flat image for band 3 robust 2 image
exportfits(imagename='ngc40389overlap_band3_uvrange_robust_2_smooth.image/', fitsimage='ngc40389overlap_band3_uvrange_robust_2_smooth.fits')

# exportfits flat image for band 7 robust 2 image
exportfits(imagename='ngc40389overlap_band7_range_robust_2_smooth.image', fitsimage='ngc40389overlap_band7_range_robust_2_smooth.fits')
