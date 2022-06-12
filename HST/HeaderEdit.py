from astropy.io import fits

def header_add_Jy(fitsfile, outputfits, item=1):
    
    hdul = fits.open(fitsfile)
    hdr = hdul[item].header
    data = hdul[item].data
    hdul.close()
    hdr['BUNIT'] = 'Jy'
    hdu = fits.PrimaryHDU(data, hdr)
    hdu.writeto(outputfits, overwrite=True)

    return



# fitsfile = 'ib5u91050_drz.fits'
# outputfits = 'Antennae_HST_Pbeta.fits'
# fitsfile = 'ib5u20090_drz.fits'
# outputfits = 'Antennae_HST_I.fits' 

fitsfile = 'Antennae_Pbeta_contsub.fits'
outputfits = 'Antennae_HST_Pbeta_contsub_header.fits'
header_add_Jy(fitsfile, outputfits, item=0)

# hdul = fits.open(fitsfile)
# hdr = hdul[1].header
# data = hdul[1].data
# hdul.close()
# 
# hdr['BUNIT'] = 'Jy'
# 
# # write the data into new fits file
# hdu = fits.PrimaryHDU(data, hdr)
# hdu.writeto(outputfits, overwrite=True) 
