from networkCore import NeuronNetwork
from PIL import Image
from scipy.ndimage import measurements, find_objects
from scipy.io import loadmat
import numpy as np
import sys
import profile
from scanImage import scan_image

def findOptimalParams(net_params = [400, 25, 10]):
    num_test_image = 6
    test_images = ['test%d.jpg'%(i+1) for i in range(num_test_image)]
    ideal = np.mat('[1 2 3 4 5 6 7 8 9 0]')
    
    network = NeuronNetwork(net_params[0], net_params[1], net_params[2])
    gamma_mass = [i*0.3 for i in range(15)]
    data = loadmat('xdata.mat')
    x = np.mat(data['X'])
    data = loadmat('ydata.mat')
    y = np.mat(data['y'])
    y[np.nonzero(y == 10)] = 0

    error = 0
    best_error = num_test_image*10
    best_gamma = best_iter = -1

    for maxiter in [10, 100, 150, 200]:
        for gamma in gamma_mass:
            #theta = network.train(x, y, gamma = gamma, iteration = maxiter)
            network.load_weights()
            print 'gamma - %f iter - %f'%(gamma, maxiter)
            error = 0
            for image in test_images:
                                
                pred = np.mat(scan_image(image)).T
                error += np.sum(pred != ideal)
            if error < best_error:
                best_gamma, best_iter = gamma, maxiter
            print 'error = %d' %error

    return best_gamma, best_iter


if __name__ == "__main__":
    #findOptimalParams([400, 25, 10])
    data = loadmat('ex4data1.mat')
    x = np.mat(data['X'])
    y = np.mat(data['y'])
    y[np.nonzero(y == 10)] = 0
    network = NeuronNetwork(400,25,10)
    profile.run('network.train(x,y,gamma=1,iteration=5)')
    #findOptimalParams([400, 30, 10])
    #findOptimalParams([400, 45, 10])
    #print scan_image('test1.jpg')
    #print scan_image('test2.jpg')
    #print scan_image('test3.jpg')
    #print scan_image('test4.jpg')
    #print scan_image('test5.jpg')
    #print scan_image('test6.jpg')

