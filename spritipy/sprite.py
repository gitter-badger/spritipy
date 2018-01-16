# TODO: make a docstring
# Christian Dansereau 2016 Copyright
import os
import numpy as np
import nibabel as nib
from PIL import Image
from nilearn.image import resample_img
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


def _load_volume(img_path):
    img = nib.load(img_path)
    vol = img.get_data()

    # check if its a nii file
    ext = _get_ext(img_path)
    if ext == ".nii":
        vol = np.swapaxes(vol, 0, 2)
    return vol


def _get_spec(vol):
    nx, ny, nz = vol.shape
    nrows = int(np.ceil(np.sqrt(nz)))
    ncolumns = int(np.ceil(nz / (1. * nrows)))
    return nrows, ncolumns, nx, ny, nz


def _get_ext(img_path):
    # Get the extension of the image file, allowing for
    # both .img.gz and .img variants
    # TODO: allow for filenames with '.' (some.dumb.file.name.nii.gz)
    extension = os.path.basename(img_path).split('.')[1]

    return extension


def montage(vol):
    nrows, ncolumns, nx, ny, nz = _get_spec(vol)

    mosaic = np.zeros((nrows * nx, ncolumns * ny))
    indx, indy = np.where(np.ones((nrows, ncolumns)))

    for ii in range(vol.shape[2]):
        # we need to flip the image in the x axis
        mosaic[(indx[ii] * nx):((indx[ii] + 1) * nx),
        (indy[ii] * ny):((indy[ii] + 1) * ny)] = vol[::-1, :, ii]

    return mosaic


def make_sprite(img_path, vmax=None, vmin=None, colmap=plt.cm.Greys):
    # TODO: set colormap ranges independently of alpha masking
    # TODO: check dimensions and sampling, possibly correct
    """
    This method generates a brainsprite ready sprite image from a 3D brain image
    file. Save the output of this method to a file for brainsprite to access.

    :param img_path: <str> file path of the image file to turn into a sprite
    :param vmax: <float> values greater than vmax in the raw image are masked
        from the sprite. (default: None)
    :param vmin: <float> values smaller than vmin in the raw image are masked
        from the sprite. (default: None)
    :param colmap: <matplotlib colormap> colormap for mapping the raw values
        to colors in the sprite. (default: pyplot Greys colormap)
    :return: sprite: <PIL Image> image object. This can be saved using the
        "save" method": sprite.save('/some/path.png')
    """
    vol = _load_volume(img_path)
    # Get thresholds
    if vmax is None:
        vmax = np.max(vol)
    if vmin is None:
        vmin = np.min(vol)

    # Create mosaic
    mosaic = montage(vol)
    # And mask it
    mask_array = (mosaic < vmax) * (mosaic > vmin)
    mask = Image.fromarray(np.uint8(mask_array) * 255).convert("L")
    # Normalize the mosaic
    mosaic = mosaic / np.max(np.abs(mosaic))
    # Make the sprite
    sprite = Image.fromarray(np.uint8(colmap(mosaic) * 255))
    sprite.putalpha(mask)

    return sprite
