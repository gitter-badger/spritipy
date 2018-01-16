# Christian Dansereau 2016 Copyright
import os
import numpy as np
import nibabel as nib
from PIL import Image
from nilearn.image import resample_img
import matplotlib.pyplot as plt


def _loadVolume(source_file):
    img = nib.load(source_file)
    vol = img.get_data()

    # check if its a nii file
    ext = _getExt(source_file)
    if ext == ".nii":
        vol = np.swapaxes(vol, 0, 2)
    return vol


def _getspec(vol):
    nx, ny, nz = vol.shape
    nrows = int(np.ceil(np.sqrt(nz)))
    ncolumns = int(np.ceil(nz / (1. * nrows)))
    return nrows, ncolumns, nx, ny, nz


def _getExt(source_file):
    # Getting the extension
    if os.path.splitext(source_file)[1] == '.gz':
        extension = os.path.splitext(os.path.splitext(source_file)[0])[1]
    else:
        extension = os.path.splitext(source_file)[1]

    return extension


def _montage(vol):
    nrows, ncolumns, nx, ny, nz = _getspec(vol)

    mosaic = np.zeros((nrows * nx, ncolumns * ny))
    indx, indy = np.where(np.ones((nrows, ncolumns)))

    for ii in range(vol.shape[2]):
        # we need to flip the image in the x axis
        mosaic[(indx[ii] * nx):((indx[ii] + 1) * nx), (indy[ii] * ny):((indy[ii] + 1) * ny)] = vol[::-1, :, ii]

    return mosaic


def _saveMosaic(mosaic, output_path, overlay=False, overlay_threshold=0.1):
    if overlay:
        mosaic[mosaic < overlay_threshold] = 0
        im = Image.fromarray(np.uint8(plt.cm.hot(mosaic) * 255))
        mask = Image.fromarray(np.uint8(mosaic > 0) * 255).convert("L")
        im.putalpha(mask)
    else:
        im = Image.fromarray(mosaic).convert('RGB')
    # if im.mode != 'RGBA':
    #    im = im.convert('RGBA')
    im.save(output_path)
