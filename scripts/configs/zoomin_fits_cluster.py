from astropy import units as u
import time
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
from regions import read_ds9
from photutils import SkyEllipticalAperture
from photutils import EllipticalAperture
from photutils import SkyRectangularAperture
import matplotlib.colors as colors
from photutils import SkyCircularAperture
from matplotlib import rcParams
rcParams['mathtext.default']='regular'
from reproject import reproject_interp
import matplotlib.image as mpimg
import pandas as pd
from regions import read_ds9

region_labels = ['1a', '1b', '2', '3', '4', '5', '6', '7', '9']
features = ['aperture', 'position', 'size']
apers = dict.fromkeys(region_labels)
for key in apers.keys():
    apers[key] = dict.fromkeys(features)

# cluster 1a
ra = 180.478967 * u.degree 
dec = -18.884991 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['1a']['position'] = center
apers['1a']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['1a']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 1b
ra = 180.479127 * u.degree 
dec = -18.884894 * u.degree 
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['1b']['position'] = center
apers['1b']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['1b']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 2
ra = 180.477452 * u.degree
dec = -18.884204 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['2']['position'] = center
apers['2']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['2']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 3
ra = 180.473146 * u.degree
dec = -18.885896 * u.degree 
center = SkyCoord(ra=ra, dec=dec, frame='icrs')
apers['3']['position'] = center
apers['3']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['3']['aperture'] = SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 4
ra = 180.472975 * u.degree
dec = -18.886184 * u.degree 
center = SkyCoord(ra=ra, dec=dec, frame='icrs')
apers['4']['position'] = center
apers['4']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['4']['aperture'] = SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)


# cluster 5
ra = 180.480646 * u.degree
dec = -18.880358 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['5']['position'] = center
apers['5']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['5']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 6
ra = 180.480335 * u.degree
dec = -18.880124 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['6']['position'] = center
apers['6']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['6']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 7
ra = 180.481078 * u.degree
dec = -18.879346 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['7']['position'] = center
apers['7']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['7']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 9
ra = 180.478114 * u.degree
dec = -18.875377 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['9']['position'] = center
apers['9']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['9']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)
