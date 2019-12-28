# Step 1- Angular Alignment
#We had two visits on each target, and needed to stack the images, before stacking, an alignment most be performed.

#the imports needed
import matplotlib.pyplot as plt
from astropy.io import fits
from reproject import reproject_interp
from astropy.wcs import WCS

#the function receives two paths of the form: R"C:\Users\Name\Location\file.fits"

def align_two_fits(path1, path2, plot=False):
    ''' this func aligns the image in the fits file in path2 to match the fits file in path1, in terms of angular alignment.
    the fits files are built like this: 2 hdu's, the first containing nothing and the second containing the image data. 
    Both have important headers that we want to keep'''
    
    hdu1 = fits.open(path1, mode='update')[1]
    hdu2 = fits.open(path2, mode='update')[1]
    second_header1= fits.open(path1, mode='update')[0].header
    second_header2= fits.open(path2, mode='update')[0].header
    
    #using reproject, we take the WCS info of the first image, and change the second one according to it.
    array, footprint = reproject_interp(hdu2, hdu1.header)
    
    #plotting, optional
    if plot:
        ax1 = plt.subplot(1,2,1, projection=WCS(hdu1.header))
        ax1.imshow(array, origin='lower', vmin=-2.e-4, vmax=5.e-4)
        ax1.coords.grid(color='white')
        ax1.coords['ra'].set_axislabel('Right Ascension')
        ax1.coords['dec'].set_axislabel('Declination')
        ax1.set_title('Reprojected 2nd image')
        ax2 = plt.subplot(1,2,2, projection=WCS(hdu1.header))
        ax2.imshow(footprint, origin='lower', vmin=0, vmax=1.5)
        ax2.coords.grid(color='white')
        ax1.coords['ra'].set_axislabel('Right Ascension')
        ax1.coords['dec'].set_axislabel('Declination')
        ax2.coords['dec'].set_axislabel_position('r')
        ax2.coords['dec'].set_ticklabel_position('r')
        ax2.set_title('1st image footprint')
        
    #writing two new fits files, notice that the new names are the original ones with the word "_aligned_" added.
    #notice we need to write both of them, even though only one was changed, 
    #in order to maintain the same format of hdu and headers, so that we can later stack them,
    
    fits.writeto(path2+'_aligned_'+'.fits', array, hdu2.header, overwrite=True)
    fits.writeto(path1+'_aligned_'+'.fits', hdu1.data, hdu1.header, overwrite=True)

    #adding the additional headers        
    curr1 = fits.open(path1+'_aligned_'+'.fits', mode='update')
    new_hdu=fits.ImageHDU(data=None, header=second_header1)
    curr1.append(new_hdu)
    curr1.close()
   
    curr2 = fits.open(path2+'_aligned_'+'.fits', mode='update')
    new_hdu=fits.ImageHDU(data=None, header=second_header2)
    curr2.append(new_hdu)
    curr2.close()
    
    #don't forget to close the new files, otherwise they are not created.
    
    #notice the hdu's order was changed, in the original files, 
    #the image's data was located in the second hdu element (indexed as 1),
    #in the new files, the image's data is loccated in the first hdu (idexed as 0).
