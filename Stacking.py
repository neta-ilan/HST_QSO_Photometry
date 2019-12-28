#Step 2- Stacking
#In our fits files, the units of the image are electron/second, 
#so when stacking we do not want to symply add the values of the pixels, 
#but to add them and divide in 2, in order to obtain the right units.

#imports
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy.visualization import ZScaleInterval
from astropy.wcs import WCS


def stack(path1, path2, draw=False, draw_QSO=None):
    ''' this func stacks 2 fits files, draw will plot the new image, 
    draw QSO takes a tuple of RA and DEC in deg and plots the QSO's close area only.
    each image has another hdu, containing a header with information, we want to keep all of the headers 
    in the new stacked file'''
    
    hdu1 = fits.open(path1, mode='update')[0] //notice the image's data is in the first hdu
    hdu2 = fits.open(path2, mode='update')[0]
    second_header1= fits.open(path1, mode='update')[1].header
    second_header2= fits.open(path2, mode='update')[1].header
    image1=hdu1.data
    image2=hdu2.data
    image_concat=[image1, image2]
    final_image = np.sum(image_concat, axis=0)
    x,y=image1.shape
    for i in range (x):
        for j in range(y):
            final_image[i][j]=(final_image[i][j])/2 
            
    #giving a new name to the stacked file
    outfile = path1+'_stacked_'+'.fits'
    fits.writeto(outfile, final_image, hdu2.header, overwrite=True)
    new_file=fits.open(path1+'_stacked_'+'.fits', mode='update')

    #adding the other headers to the new file
    #we are using the information in the header to name the new hdu element.
    new_hdu=fits.ImageHDU(data=None, header=second_header1, name=second_header1['ROOTNAME']) 
    new_hdu2=fits.ImageHDU(data=None, header=second_header2, name=second_header2['ROOTNAME'])
    new_file.append(new_hdu)
    new_file.append(new_hdu2)
    
    #editting the SCI header, so that whoever uses it knows it is not original 
    #and knows the names of the original ones that were stacked to make this image
    val1='stacked_of: '+second_header1['ROOTNAME']+' and: '+second_header2['ROOTNAME']
    new_file[0].header['ROOTNAME']=val1
    new_file[0].header['EXPNAME']=val1
    new_file.close()
    #don't forget to close the new file, or it wont be created
    
    #the stacked image is done, now moving on to plotting it in Z-scale (optional)
    
    if draw==True:
        interval = ZScaleInterval()
        zmin, zmax=interval.get_limits(final_image)
        plt.imshow(final_image, cmap='gray', vmin=zmin, vmax=zmax)
        plt.colorbar()
        
    #if the image is wide field, you might want to see only your object and make sure the stacking is good
    #you will need to supply the function with a tuple, containing the RA and DEC of your object.
    
    if draw_QSO!=None:
        #the first part is undestanding the pixels mathing the coordinates
        RA=float(draw_QSO[0])
        DEC=float(draw_QSO[1])
        w=WCS(hdu1.header)
        px, py = w.all_world2pix([RA],[DEC], 1)
        x=px[0]
        y=py[0]
        #the pixels must be integer values
        centerX=int(round(x)) 
        centerY=int(round(y))
        #plotting the close area to your object
        interval = ZScaleInterval()
        zmin, zmax=interval.get_limits(final_image)
        plt.xlim(centerX-80,centerX+80)
        plt.ylim(centerY-75,centerY+75)
        plt.axes().set_aspect('equal')
        plt.imshow(final_image,cmap='gray',clim=(zmin,zmax))
        plt.colorbar()
       
