imsmooth(imagename = 'ngc4038_band3_cont_12m_7m.pbcor', 
	 outfile='ngc4038_band3_cont_12m_7m_roundbeam.pbcor',
	 major='0.65arcsec',
	 minor='0.65arcsec', 
	 pa='0deg',
	 targetres=True)

exportfits(imagename='ngc4038_band3_cont_12m_7m.pbcor', fitsimage='ngc4038_band3_cont_12m_7m_pbcor.fits')

imsmooth(imagename='ngc4038_band3_cont_12m_7m.image', 
         outfile='ngc4038_badn3_cont_12m_7m_smooth_phangs.image', 
         major='0.74arcsec', 
         minor='0.55arcsec',
         pa='-81deg', 
         targetres=True)

# exportfits the flat image
exportfits(imagename='ngc4038_band3_cont_12m_7m.image', fitsimage='ngc4038_band3_cont_12m_7m.fits')
