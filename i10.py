import numpy as np
import os
from PIL import Image


#
#
# Main i10 code
#
#

def qSpaceResolution(energy):
    """
    Calculates the reciprocal space resolution of each pixel on the CCD

    Parameters:
    ----------
    energy: energy of the x-rays measured in eV
    
    SD: Sample detector distance (fixed for i10)

    returns: Qp, reciprocal space pixel value (multiply by number of pixels)

    """
    wavelength = (6.63e-34 * 3e8)/(energy * 1.6e-19) * 1e9 # In inverse angstroms
    sampleDistance = 138e-3
    pixelSize = 13.5e-6
    theta_p = 0.5 * np.arctan((pixelSize)/sampleDistance)
    Qp = (4*np.pi*np.sin(theta_p))/wavelength # Braggs law
    return Qp


#=========== Tiff manipulation ==============

def readTiff(filename):
    """
    Reads a single tiff file into a np.array for a 2048x2048 detector
    
    Parameters:
    -----------
    filename: filename of the tiff you want to load (str)

    returns: image array to be plotted in matplotlib

    """
    im = np.zeros((2048, 2048))
    im += np.array(Image.open(filename))
    return im


def condenseTiff(self, filenum):
    """
    Reads all pimtetiff files from a -pimte-files folder and condenses them into a single image

    Parameters:
    -----------
    filenum: -pimte-files prefix number

    returns: image array to be plotted in matplotlib

    """
    im = np.zeros((2048,2048))
    for filename in os.listdir(self.fpath + str(filenum) + '-pimte-files'):
        print(self.fpath + str(filenum) + '-pimte-files/' + filename)
        im += np.array(Image.open(self.fpath + str(filenum) + '-pimte-files/' + filename))
    return im


def save_tiff(im, directory, filename):
    """
    Saves a tiff into a new directory for use in ImageJ
    Checks if the directory exists first and if it doesn't, create the new directory

    Parameters:
    ----------
    im: image array create using readTiff or condenseTiff
    directory: directory you want to save to, will create if it doesn't exist
    filename: name of the file you want to save
    
    """
    isFile = os.path.isdir(directory) # Checks whether the folder exists and if not makes one
    pic = os.path.exists(directory + filename + '.tiff')
    if isFile == False:
        os.mkdir(directory)
    else:
        pass
    if pic == False:
        tiff = Image.fromarray(im)
        tiff.save(directory + filename + '.tiff')
    else:
        pass


if __name__ == "__main__":
    print("The q-length of skyrmions in Cu2OSeO3 should be about 0.1 angstroms: %f" % (qSpaceResolution(931.8) * 237))