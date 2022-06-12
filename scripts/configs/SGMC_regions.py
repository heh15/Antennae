from astropy import units as u
from photutils import SkyRectangularAperture
from photutils import SkyEllipticalAperture
from astropy.coordinates import SkyCoord
from photutils import SkyCircularAperture

SGMC_labels = ['1','2','3','4/5']
apers = dict.fromkeys(SGMC_labels)
parameters = ['apertures', 'txt_coords']
for key in apers.keys():
    apers[key] = dict.fromkeys(parameters)

ra = 15*(12*u.degree+1*u.arcmin+55.5*u.arcsec)
dec = -(18*u.degree+52*u.arcmin+47*u.arcsec)
D_pc = 1400
position = SkyCoord(ra = ra, dec = dec, frame='icrs')
radius_arcsec = D_pc / 4.85 / 19 / 2
apers['1']['apertures'] = SkyCircularAperture(position, r=radius_arcsec*u.arcsec)
apers['1']['txt_coords'] = SkyCoord(ra=position.ra+7*u.arcsec, dec=position.dec)

ra = 15*(12*u.degree+1*u.arcmin+54.9*u.arcsec)
dec = -(18*u.degree+52*u.arcmin+52*u.arcsec)
D_pc = 1100
position = SkyCoord(ra = ra, dec = dec, frame='icrs')
radius_arcsec = D_pc / 4.85 / 19 / 2
apers['2']['apertures'] = SkyCircularAperture(position, r=radius_arcsec*u.arcsec)
apers['2']['txt_coords'] = SkyCoord(ra=position.ra-0*u.arcsec, dec=position.dec)

ra = 15*(12*u.degree+1*u.arcmin+54.7*u.arcsec)
dec = -(18*u.degree+53*u.arcmin+2*u.arcsec)
D_pc = 1300
position = SkyCoord(ra = ra, dec = dec, frame='icrs')
radius_arcsec = D_pc / 4.85 / 19 / 2
apers['3']['apertures'] = SkyCircularAperture(position, r=radius_arcsec*u.arcsec)
apers['3']['txt_coords'] = SkyCoord(ra=position.ra-5*u.arcsec, dec=position.dec)

ra = 15*(12*u.degree+1*u.arcmin+54.9*u.arcsec)
dec = -(18*u.degree+53*u.arcmin+2*u.arcsec)
D_pc = 1000
position = SkyCoord(ra = ra, dec = dec, frame='icrs')
radius_arcsec = D_pc / 4.85 / 19 / 2
apers['4/5']['apertures'] = SkyCircularAperture(position, r=radius_arcsec*u.arcsec)
apers['4/5']['txt_coords'] = SkyCoord(ra=position.ra+5*u.arcsec, dec=position.dec)
