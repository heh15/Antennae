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
