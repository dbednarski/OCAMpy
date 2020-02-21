#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Usage:

$ python raw2fits.py FILE01.raw FILE02.raw ...

Output: FILE01.fits FILE02.fits ...

With Overscan: 63888 pixels/frame (1x1); Clean: 57600 pixels/frame (1x1)

Authors: Daniel Moser, Daniel Bednarski
Last changes on 2020-02-19.

"""

import sys
import numpy as np
import struct
import warnings as warn
from astropy.io import fits


for tfile in sys.argv[1:]:

    # FAZER LOOP A CADA 57600*2 elementos (hex)
    f = open(tfile, 'rb').read()
#    fpx = 63888
    fpx = 57600
    deadpix = 2  # the first 2 px are "dead pix" (don't contain information).
    ixdr = 0
    nframe = int(len(f)/(2*(fpx+deadpix)))
    print("# Reading {} frames from {} file...".format(nframe,tfile))

    for i in range(0,nframe):
        ixdr += deadpix*2
        data = struct.unpack('<{}h'.format(fpx), f[ixdr:ixdr+fpx*2])
        ixdr += fpx*2

        # #
        mtx = np.array(data).reshape(240, 240)
        hdu = fits.PrimaryHDU(mtx.astype('int16'))

# ADICIONAR CAMPOS DO HEADER
#       hdu.header['exposure'] = 0.1
#       hdu.header['naxis1'] = 240
#       hdu.header['naxis2'] = 240
#       print(hdu.header)
        hdul = fits.HDUList([hdu])
        hdul.writeto(tfile.replace('.raw', '_{:03d}.fits'.format(i)))

    # this will check if the XDR is finished.
    if ixdr == len(f):
        print('# XDR {0} completely read!\n'.format(tfile))
    else:
        warn.warn( '# XDR {0} not completely read!\n# length difference is '
            '{1}\n'.format(tfile, (len(f)-ixdr)/2 ) )


