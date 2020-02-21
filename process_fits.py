#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    This script substracts the median bias from the images and
    combine a median image for each wavelength.

    Usage: python process_fits.py path_to_raw_files

    
    Required input filenames:
    
    bias: median bias is computed using all bias*.fits files.
          CAUTION: just keep inside the folder the correct bias
          files to be combined.
          
    images: this script supposes each image name being as
            "img_"+wavelength+"_*.fits", where "wavelenght" is the
            value that distinguishes each wavelenght (300nm, 350nm, etc).
            For each distinct "wavelength" value is computed a median image,
            regardless of the "*" content right before the .fits extension.

    The output processed files are named "avg_"+prefix+".fits".


    Author: Daniel Bednarski
    Date: 2020-02-19.
"""

import sys
import numpy as np
import struct
import warnings as warn
from astropy.io import fits
import glob
import matplotlib.pyplot as plt



def medianImage(input_files, bias=[]):
    '''
        input_files: List of filenames
        bias: bias DATA.
    '''

    # 'data' below is going to be shapped as (10, 240, 240) np.array
    if len(bias) == 0:
        data = np.array([fits.open(f)[0].data for f in input_files])
    else:
        data = np.array([fits.open(f)[0].data-bias for f in input_files])
    
    print("Combined files:")
    print(input_files)
    print(data.shape)
    
    # return 'data' median over index 0 (i.e., over 10 images)
    return np.median(data, axis=0)




folder=sys.argv[1]


list_all_images = np.sort(glob.glob("{}/img*.fits".format(folder)))
list_bias = np.sort(glob.glob("{}/bias*.fits".format(folder)))

print("*** Processing bias...")
bias_data = medianImage(list_bias)
#print(bias_data)
#plt.imshow(bias_data, cmap='gray')
#plt.show()

prefix = ""
list_img = np.array([])
#list_all_images = np.append(list_all_images, [])
for i,img in enumerate(list_all_images):
    print(img.split('/')[-1].split('_')[-2])
 
    # The second condition is just to proccess the last image serie
    if prefix != img.split('/')[-1].split('_')[-2] or i == len(list_all_images)-1:
#        print("^^^ mudou")
        if i == len(list_all_images)-1:
            prefix = img.split('/')[-1].split('_')[-2]
            list_img = np.append(list_img,[img])
        elif len(list_img) == 1:
            prefix = img.split('/')[-1].split('_')[-2]

        if len(list_img) != 0:
            print("*** Processing {} serie...".format(prefix))
            img_data = medianImage(list_img, bias_data)

            # SALVING the processed fits
            hdu = fits.PrimaryHDU(img_data.astype('int16'))
            hdulist = fits.HDUList([hdu])
            hdulist.writeto('avg_{}.fits'.format(prefix))
        else:
            print("*** WARNING: not processed image serie for {}.".format(img))
        
        # Get new values
        list_img = np.array([img])
        prefix = img.split('/')[-1].split('_')[-2]
                
    else:
        list_img = np.append(list_img,[img])
        
        

