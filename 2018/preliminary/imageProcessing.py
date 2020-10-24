immath(imagename = ['member.uid___A001_X133d_X965.s10_0.NGC4038_sci.spw29.mfs.I.iter1.image.pbcor.fits', 'member.uid___A001_X133d_X965.s10_0.NGC4038_sci.spw29.mfs.I.iter1.pb.fits'], 
	expr = 'IM0/IM1', 
	outfile = 'member.uid___A001_X133d_X965.s10_0.NGC4038_sci.spw29.mfs.I.iter1.image')

# make the moment 2 maps of the CO 2-1 image
immoments(imagename = 'member.uid___A001_X133d_X96f.NGC4038_sci.spw25.cube.I.pbcor.fits', moments=2, includepix=[4*3.7e-3, 100], chans='150~350', outfile='ngc4038_4039_CO21_pbcor.mom2')
imregrid(imagename = 'member.uid___A001_X133d_X96f.NGC4038_sci.spw25.cube.I.pb.fits', template = 'ngc4038_4039_CO21_pbcor.mom2/', output='ngc4038_4039_CO21.pb') 
immoments(imagename = 'member.uid___A001_X133d_X96f.NGC4038_sci.spw25.cube.I.pbcor.fits', moments=2, includepix=[4*3.7e-3, 100], mask = 'member.uid___A001_X133d_X965.s10_0.NGC4038_sci.spw29.mfs.I.iter1.pb.fits>0.5', stretch=True, chans='150~350', outfile='ngc4038_4039_CO21_pbcor1.mom2')

# make the moment 0 maps of the 12CO 2-1 image. 
immoments(imagename = 'member.uid___A001_X133d_X96f.NGC4038_sci.spw25.cube.I.pbcor.fits', moments=0, includepix=[2*3.7e-3, 100], chans='150~350', outfile='ngc4038_4039_CO21_pbcor.mom0')
