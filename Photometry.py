#Step 3- Aperture Photometry

#imports
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import photutils
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from matplotlib.colors import LogNorm
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import ZScaleInterval
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS, Galactic, FK4, FK5
from astropy.coordinates import Angle, Latitude, Longitude
from astropy import wcs
from astropy.wcs import WCS
import sys
import math
###########################################################################

def photometry3(hdulist, centerX, centerY, small, medium, large):
    ''' this func calculates counts->flux->mag[AB] and the matching error
    for the calculation. it assumes that the "small" aperture is 3 pixels (radius) and
    therefore the enclosed flux percentage is: 0.838'''
    
    imdata=hdulist[0].data
    radius=small
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])
    C1 = np.sum(photCollector) #small circle counts with noise
    A1 = len(photCollector)
    radius=medium
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])         
    C2 = np.sum(photCollector)
    A2 = len(photCollector)
    radius=large
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])   
    C3 = np.sum(photCollector)
    A3 = len(photCollector)
    bi=(C3-C2)/(A3-A2) #background_noise_avg_per_pixel
    B=A1*((C3-C2)/(A3-A2)) #background_small_circle
    counts=C1-B
    
    #tranforming counts to flux
    F_JANSKY=9.5291135*math.pow(10,-8)
    PHOTFNU=pow(10,-23)*F_JANSKY
    FluxAB=(counts*PHOTFNU)/0.838
    
    #tranforming flux to magnitude
    magAB=-(2.5)*math.log10(FluxAB)-48.6
    
    #now for the error
    error_in_counts=math.sqrt(C1+2*B)
    #0.838 is the encircled flux percentage for a 3 pixels circle
    Flux_error=(error_in_counts*PHOTFNU)/0.838
    mag_error=-(2.5/math.log(10))*(Flux_error/FluxAB)
    return magAB, mag_error

def photometry5(hdulist, centerX, centerY, small, medium, large):
    ''' this func calculates counts->flux->mag[AB] and the matching error
    for the calculation this func assumes that the "small" aperture is 5 pixels and
    therefore the enclosed flux percentage is: 0.88125'''
    imdata=hdulist[0].data
    radius=small
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])
    C1 = np.sum(photCollector) #small circle counts with noise
    A1 = len(photCollector)
    radius=medium
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])         
    C2 = np.sum(photCollector)
    A2 = len(photCollector)
    radius=large
    photCollector=np.array([])
    for ii in range(centerX-radius, centerX+radius):
        for jj in range(centerY-radius,centerY+radius):
            distance = np.sqrt((ii-centerX)**2 + (jj-centerY)**2 )
            if distance < radius:
                photCollector= np.append(photCollector, imdata[jj][ii])   
    C3 = np.sum(photCollector)
    A3 = len(photCollector)
    bi=(C3-C2)/(A3-A2) #background_noise_avg_per_pixel
    B=A1*((C3-C2)/(A3-A2)) #background_small_circle
    counts=C1-B
    F_JANSKY=9.5291135*math.pow(10,-8)
    PHOTFNU=pow(10,-23)*F_JANSKY
    FluxAB=(counts*PHOTFNU)/0.88125
    magAB=-(2.5)*math.log10(FluxAB)-48.6
    #now for the error
    error_in_counts=math.sqrt(C1+2*B)
    #0.838 is the encircled flux percentage for a 3 pixels circle
    #0.88125 for 5 pixels
    Flux_error=(error_in_counts*PHOTFNU)/0.88125
    mag_error=-(2.5/math.log(10))*(Flux_error/FluxAB)
    return magAB, mag_error

def plot_circles(hdulist, centerX, centerY, small, medium, large):
    ''' this func plots the image in z-scale with three aperture circles'''
    imdata=hdulist[0].data
    interval = ZScaleInterval()
    zmin, zmax=interval.get_limits(imdata)
    plt.xlim(centerX-80,centerX+80)
    plt.ylim(centerY-75,centerY+75)
    plt.axes().set_aspect('equal')
    plt.imshow(imdata,cmap='gray',clim=(zmin,zmax))
    plt.colorbar()
    plt.xlabel(hdulist[1].header['TARGNAME'])
    thisCircle = plt.Circle((centerX, centerY), small,
    color='r',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    thisCircle = plt.Circle((centerX, centerY), medium,
    color='g',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    thisCircle = plt.Circle((centerX, centerY), large,
    color='b',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    #you can choose to save the figure by uncommenting the next line
    #plt.savefig(hdulist[1].header['TARGNAME']+hdulist[1].header['FILENAME']+".png", bbox_inches='tight')

def plot_circles_not_z_scale(hdulist, centerX, centerY, small, medium, large):
    ''' this func plots only the 0.05 highest valued pixels with three aperture circles
    this is good for identifying the center of the PSF of the QSO'''
    imdata=hdulist[0].data
    plt.xlim(centerX-80,centerX+80)
    plt.ylim(centerY-75,centerY+75)
    plt.axes().set_aspect('equal')
    plt.imshow(imdata,cmap='gray',clim=(0.95,0.9999))
    plt.colorbar()
    plt.xlabel(hdulist[1].header['TARGNAME'])
    thisCircle = plt.Circle((centerX, centerY), small,
    color='r',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    thisCircle = plt.Circle((centerX, centerY), medium,
    color='g',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    thisCircle = plt.Circle((centerX, centerY), large,
    color='b',fill=False,lw=2)
    plt.gca().add_artist(thisCircle)
    #you can choose to save the figure by uncommenting the next line
    #plt.savefig(hdulist[1].header['TARGNAME']+hdulist[1].header['FILENAME']+".png", bbox_inches='tight')
