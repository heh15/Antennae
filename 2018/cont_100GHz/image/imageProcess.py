imsmooth(imagename = 'ngc4038_band3_cont_12m_7m.pbcor', 
	 outfile='ngc4038_band3_cont_12m_7m_roundbeam.pbcor',
	 major='0.65arcsec',
	 minor='0.65arcsec', 
	 pa='0deg',
	 targetres=True)

exportfits(imagename='ngc4038_band3_cont_12m_7m.pbcor', fitsimage='ngc4038_band3_cont_12m_7m_pbcor.fits')
