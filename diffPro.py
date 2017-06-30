'''Calculate background noise (gs rms) of unlimited number of diff images
input: strings (test and ref image pairs)
output: float (rms)
'''

from scipy import misc
from scipy import signal
import numpy as np
from numpy import mean, sqrt, square
from glob import glob

# When print, print the full content of np array, not the truncated one
np.set_printoptions(threshold=np.inf)

# Read png file, and return grey scale image
def readImage(png):
    image = misc.imread(png)
    image = image.astype(np.int16)
    return image

# Perform 2x2 convolution, and remove defective pixels
def convolve(diff):
    mask = np.array([[1,1],
                    [1,1]])
    cDiff = signal.convolve2d(diff, mask, mode = 'same', boundary = 'wrap')

    # remove defective pixels, return(noise) is a 1D array
    # noise = cDiff[abs(cDiff) < 20]

    return cDiff

# Calculate rms of a np array
def rms(array):
    return sqrt(mean(square(array)))

if __name__ == '__main__':
    images = glob('*png')
    noise_2x2 = []
    noise_1x1 = []
    for png in images:
        diff = readImage(png)
        cDiff = convolve(diff)
        noise_2x2.append(cDiff)

        noise_1x1.append(diff)

    rmsAll_2by2 = list(map(lambda x: rms(x), noise_2x2))
    rmsAll_1by1 = list(map(lambda x: rms(x), noise_1x1))
    print ('2x2 background noise rms =', rms(rmsAll_2by2), 'gs')
    print('1x1 background noise rms =', rms(rmsAll_1by1), 'gs')





