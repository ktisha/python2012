from networkCore import NeuronNetwork
from PIL import Image
from scipy.ndimage import measurements, find_objects
from scipy.io import loadmat
import numpy as np
import sys
import profile

def scan_image(filename, ):
    image = np.array(Image.open(filename).convert('L')).T
    image = 255 - image  ## Inverting image, just like in a train set
    mask = [[1,1,1],
        [1,1,1],
        [1,1,1]]
    labels, numb_of_components = measurements.label(1*(image > 128), structure=mask)
    slices =  find_objects(labels)
    network = NeuronNetwork(400, 25, 10)
    network.load_weights()
    result = []

    for i in range(numb_of_components):
          digit = image[slices[i]]
          size = digit.shape
          square_size = max(size)
          canvas = np.zeros([square_size]*2)
          ind1 = ((square_size - size[0]) / 2, (square_size - size[1]) / 2)
          ind2 = ((square_size + size[0]) / 2, (square_size + size[1]) / 2)
          canvas[ind1[0]:ind2[0]][:,ind1[1]:ind2[1]] = digit
          #Image.fromarray(canvas.T).show()
          digit = np.mat(Image.fromarray(canvas).resize((20,20))).T
          result.append(network.predict(digit.flatten(1))[0])
          #s = raw_input()
    return result  ## FIXME !!!

