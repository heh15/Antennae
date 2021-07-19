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

region_labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
features = ['aperture', 'position', 'size']
apers = dict.fromkeys(region_labels)
for key in apers.keys():
    apers[key] = dict.fromkeys(features)

# cluster 1 
ra = 180.479004 * u.degree 
dec = -18.884962 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['1']['position'] = center
apers['1']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['1']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

# cluster 2
ra = 180.477452 * u.degree
dec = -18.884204 * u.degree
center = SkyCoord(ra = ra, dec = dec, frame='icrs')
apers['2']['position'] = center
apers['2']['size'] = u.Quantity(((0.015, 0.015)), u.arcmin)
apers['2']['aperture'] =  SkyRectangularAperture(center, 0.015*u.arcmin, 0.015*u.arcmin)

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
