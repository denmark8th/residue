'''Calculate background noise (gs rms) of unlimited number of diff iamges
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

# Extract the digit from the file name:
def findNum(string):
    for char in string:
        if char.isdigit():
            return int(char)

# Convert RGB to grey scale
def rgb2grey(image):
    # rgb2grey formula
    def average(pixel):
        return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]

    grey = np.zeros((image.shape[0], image.shape[1]))  # init 2D numpy array

    for rownum in range(len(image)):
        for colnum in range(len(image[rownum])):
            grey[rownum][colnum] = average(image[rownum][colnum])

    return grey

# Read png file, and return grey scale image
def readImage(filename):
    image = misc.imread(filename)
    imageGrey = rgb2grey(image)
    imageGrey = imageGrey.astype(np.int16)

    return imageGrey

# Perform 2x2 convolution, and remove defective pixels
def convolve(diff):
    mask = np.array([[1,1],
                    [1,1]])
    cDiff = signal.convolve2d(diff, mask, mode = 'same', boundary = 'wrap')

    # remove defective pixels (2x2 < -20), return(noise) is a 1D array
    noise = cDiff[cDiff > -20]

    return noise

# Calculate rms of a np array
def rms(array):
    return sqrt(mean(square(array)))

if __name__ == '__main__':
    test = glob('*Test_Proc*')
    ref = glob('*Ref_Proc*')

    noiseAll = []
    for ti in test:
        for ri in ref:
            if ti.split('_')[1] == ri.split('_')[1]:
                diff = np.subtract(readImage(ti), readImage(ri))
                noise = convolve(diff)
                noiseAll.append(noise)

    rmsAll = list(map(lambda x: rms(x), noiseAll))
    print ('2x2 background noise rms =', rms(rmsAll), 'gs')





