# HST_QSO_Photometry

This repository contains a code for Apparture Photometry of data taken by the Wide Field Camera 3 located on Hubble Space Telescope. 

## Requirements

* `anaconda` with `python 3.7`
* `astropy`, `numpy`, `matplotlib` packages
* A basic understanding of FITS (Flexible Image Transport System) files and their structure
* A basic undestanding of the Aperture Photomentry method

You can find a good explanation for both FITS files structure and Aperture Photometry, in "A Beginner's Guide to Working with Astronomical Data" by Markus Possel, chapter 10.1 "FITS files and python".

## Observational data

This code was used to analyze data obtained with HST WFC3 NIR F140W (Hubble Space Telescope, Wide Field Camera 3, Near InfraRed Channel, ~14000 Angstrom wavelength). 

The principal investigator of the proposel is Trakhtenbrot Benny (Tel Aviv University, Israel).
In this project, the photometric measurments were done on a sample of 6 Quasi-stellar objects (QSO), in high Redshifts.

## Scripts Functions Overview

This repository contains a few scripts:

1. Angular alignment. As a preperatory stage before stacking the images.
    * align_two_fits(path1, path2, plot=False):
        this func aligns the image in the fits file in path2 to match the fits file in path1, in terms of angular alignment.
        the fits files assumed struceture: 2 hdu's, the first containing nothing (in the data part), and the second containing the image data. 
        Both have important headers that we want to keep.
    
2. Stacking two images stored in two FITS files. 
    * stack(path1, path2, draw=False, draw_QSO=None):
        this func stacks 2 fits files, the draw option will plot the new image, 
        the draw_QSO option takes a tuple of RA and DEC in deg and plots the QSO's close area only.
        each original image has two hdus, one containing a header and the image data, and the other containing only a header with information.
        the new stacked file will contain all of these headers.
        notice- the draw_QSO feature uses WCS (World Coordinate System) taken from the header in order to match the given coordinates and
        their matching pixels.

3. Aperture Photometry. 
* photometry3(hdulist, centerX, centerY, small, medium, large):
    this func calculates counts->flux->mag[AB] and the matching error.
    it assumes that the "small" aperture is 3 pixels (radius) and
    therefore the enclosed flux percentage is: 0.838.
    notice- the enclosed flux precentage can be taken from the "WFPC3 Instrument Handbook"
    (http://www.stsci.edu/hst/instrumentation/wfc3), chapter 7, Table 7.6: WFC3/IR PSF Encircled Energy Fraction vs. Aperture Radius
    (arcsec).
* photometry5(hdulist, centerX, centerY, small, medium, large):
    same as the previous function, but this func assumes that the "small" aperture is 5 pixels and
    therefore the enclosed flux percentage is: 0.88125'''
* plot_circles(hdulist, centerX, centerY, small, medium, large):
    this func plots the image in z-scale with three aperture circles.
    this feature helps you to see what objects you are including in your measurment of the background.
* plot_circles_not_z_scale(hdulist, centerX, centerY, small, medium, large):
    this func plots only the 0.05 highest valued pixels with three aperture circles
    this is good for identifying the center of the PSF of the QSO.
   

For any questions regarding this repository, feel free to write me via mail: neta.ilan@tau.ac.il


