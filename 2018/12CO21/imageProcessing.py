# rebin the moment 8 maps
imrebin(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_2sig_pbcor_K.fits', 
        factor=[5,5], 
        outfile='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_2sig_pbcor_K_rebin.mom8',
        overwrite=True)
exportfits(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_2sig_pbcor_K_rebin.mom8', 
          fitsimage='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_2sig_pbcor_K_rebin.fits',
          overwrite=True)

# rebin the moment 8 maps with 5 sigma cutoff. 
imrebin(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K.fits',
        factor=[5,5],
        outfile='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K_rebin.mom8',
        overwrite=True)
exportfits(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K_rebin.mom8',
          fitsimage='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom8_5sig_pbcor_K_rebin.fits',
          overwrite=True)


# rebin the moment 0 maps
imrebin(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K.fits', 
        factor=[5,5], 
        outfile='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K_rebin.mom0',
        overwrite=True)
exportfits(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K_rebin.mom0', 
           fitsimage='ngc_4038_4039_12m_ext+12m_com+7m_co21_mom0_2sig_pbcor_K_rebin.fits',
           overwrite=True)

# make moment 0 map for flat cube
immoments(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_flat_round_k.fits', 
          moments=0, includepix=[2*0.26, 1000], chans='100~295', 
          outfile='ngc_4038_4039_12m_ext+12m_com+7m_co21_flat_round_k.mom0')
exportfits(imagename='ngc_4038_4039_12m_ext+12m_com+7m_co21_flat_round_k.mom0', 
          fitsimage='ngc_4038_4039_12m_ext+12m_com+7m_co21_flat_round_k_mom0.fits')
