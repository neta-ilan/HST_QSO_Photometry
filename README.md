# HST_QSO_Photometry

This repository contains a code for Apparture Photometry of data taken by the Wide Field Camera 3 located on Hubble Space Telescope. 

## Requirements

* `anaconda` with `python 3.7`
* `astropy`, `numpy`, `matplotlib` packages
* A basic understanding of FITS (Flexible Image Transport System) files and their structure

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

## Observational data

This code was used to analyze data obtained with HST WFC3 NIR F140W (Hubble Space Telescope, Wide Field Camera 3, Near InfraRed Channel, ~14000 Angstrom wavelength). 

The principal investigator of the proposel is Trakhtenbrot Benny (Tel Aviv University, Israel).



