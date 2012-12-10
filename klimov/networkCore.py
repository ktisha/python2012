import numpy as np
import scipy.io
import scipy.optimize
import time

class NeuronNetwork:
    
    def __init__(self, input_size, hidden_size, output_size, eps = 0.12):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.Theta1 = []
        self.Theta2 = []

   
    def predict(self, x, Theta = None):
        Theta1 = Theta2 = []

        if Theta != None:
            Theta1 = np.reshape(Theta[0 : (self.input_size+1) * self.hidden_size], [self.input_size + 1,self.hidden_size])
            Theta2 = np.reshape(Theta[(self.input_size+1) * self.hidden_size :], [self.hidden_size + 1, self.output_size])
        else:
            if self.Theta1 == [] or self.Theta2 == []:
                self.load_weights()
            Theta1 = self.Theta1
            Theta2 = self.Theta2
        

        m = x.shape[0]
        h1 = sigmoid(np.concatenate((np.ones([m, 1]), x), 1) * Theta1)
        h2 = sigmoid(np.concatenate((np.ones([m, 1]), h1), 1) * Theta2)
        
        return np.asarray(np.argmax(h2, 1))

    def gradiend_descend(self, Theta, args, iteration, eps, mu):
        J_prev = 0
        for i in xrange(iteration):
            print 'iteration: ' + str(i) + "  (" + str((i/float(iteration)*100)) + "%)" 
            dTheta = grad_function(Theta, args)
            J = cost_function(Theta, args)
            if abs(J_prev - J) < eps:
                break
            #if J - J_prev > 0:
            #    mu /= 3
            #    continue
            Theta -= mu * dTheta
            J_prev = J
        return Theta
            

    def train(self, x, y, iteration = 200, eps = 1e-8, gamma = 1.0, mu = 1.0, weigth_eps = 0.12, disp = True):
        self.Theta1 = np.random.uniform(-weigth_eps, weigth_eps, [self.hidden_size, self.input_size + 1]) # 0.12 is magic const from science paper
        self.Theta2 = np.random.uniform(-weigth_eps, weigth_eps, [self.output_size, self.hidden_size + 1])

        Theta = np.concatenate((np.mat(self.Theta1.flatten(1)), np.mat(self.Theta2.flatten(1))), 1)
        args = (x, y, gamma, self.input_size, self.hidden_size, self.output_size)
        
        #print 'starting train network'
        start = time.time()
        Theta = scipy.optimize.fmin_cg(cost_function, Theta, grad_function, args=[args], disp=True, maxiter=iteration)
        print "network.train: elapsed Time: %s sec." % (time.time() - start)

        self.Theta1 = np.reshape(Theta[0 : (self.input_size+1) * self.hidden_size], [self.input_size + 1,self.hidden_size])
        self.Theta2 = np.reshape(Theta[(self.input_size+1) * self.hidden_size :], [self.hidden_size + 1, self.output_size])
        
        pred = self.predict(x)
        
        print 'training accuracy = %f%%'% (100. * np.sum(y == pred) / float(y.shape[0]))
    
    
    def save_weights(self):
        data = {}
        data['Theta1'] = self.Theta1
        data['Theta2'] = self.Theta2
        scipy.io.savemat("weight.mat", data)

    def load_weights(self):
        data = scipy.io.loadmat("weight.mat")
        self.Theta1 = np.mat(data['Theta1'])
        self.Theta2 = np.mat(data['Theta2'])

def sigmoid(z):
    return 1./(1. + np.exp(-z))

def sigmoid_gradient(z):
    g = sigmoid(z)
    return np.multiply(g, 1 - g)

def cost_function(Theta, args):

    x = args[0]
    y = args[1]
    gamma = args[2]
    input_size = args[3]
    hidden_size = args[4]
    output_size = args[5]

    Theta1 = np.reshape(Theta[0 : (input_size+1) * hidden_size], [input_size + 1,hidden_size]).T
    Theta2 = np.reshape(Theta[(input_size+1) * hidden_size :], [hidden_size + 1, output_size]).T

    m = len(x)

    a1 = np.concatenate((np.ones([x.shape[0], 1]), x), 1)
    z2 = Theta1 * a1.T
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones([1, a2.shape[1]]), a2))
    a3 = sigmoid(Theta2 * a2)
    
    Y = np.zeros([y.shape[0], output_size])
    for i in xrange(y.shape[0]):
        Y[i, y[i]] = 1

    J = (np.sum(np.multiply(-Y.T, np.log(a3)) - np.multiply(1 - Y.T, np.log(1-a3))) / m +
                gamma * np.sum(np.power(Theta1[:][:, 1:], 2)) / (2*m) + 
                gamma * np.sum(np.power(Theta2[:][:, 1:], 2)) / (2*m))

    return J

def grad_function(Theta, args):

    x = args[0]
    y = args[1]
    gamma = args[2]
    input_size = args[3]
    hidden_size = args[4]
    output_size = args[5]
    Theta1 = np.reshape(Theta[0 : (input_size+1) * hidden_size], [input_size + 1,hidden_size]).T
    Theta2 = np.reshape(Theta[(input_size+1) * hidden_size :], [hidden_size + 1, output_size]).T

    result = np.zeros_like(Theta)

    m = len(x)

    a1 = np.concatenate((np.ones([x.shape[0], 1]), x), 1)
    z2 = Theta1 * a1.T
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones([1, a2.shape[1]]), a2))
    a3 = sigmoid(Theta2 * a2)
    Y = np.zeros([y.shape[0], output_size])
    for i in xrange(y.shape[0]):
        Y[i, y[i]] = 1
    
    delta3 = a3.T - Y
    z2 = np.concatenate((np.ones([1, z2.shape[1]]), z2))
    delta2 = np.multiply((delta3 * Theta2).T, 
                sigmoid_gradient(z2))

    T1 = (delta2[1:,:] * a1) / m
    T2 = (a2 * delta3).T / m
    
    T1[:][:,1:] += (gamma / m) * Theta1[:][:,1:]
    T2[:][:,1:] += (gamma / m) * Theta2[:][:,1:]
    T1 , T2 = np.ndarray.flatten(T1,1), np.ndarray.flatten(T2,1)
    
    result[0:(input_size+1)*hidden_size] = T1
    result[(input_size+1)*hidden_size:] = T2
    return result


if __name__ == "__main__":
    data = scipy.io.loadmat("xdata.mat")
    #print data.key
    #data = scipy.io.loadmat('ex4data1.mat')
    x = np.mat(data['X'])
    data = scipy.io.loadmat("ydata.mat")
    y = np.mat(data['y'])
    y[np.nonzero(y == 10)] = 0
    network = NeuronNetwork(x.shape[1], 30, 10)
    network.train(x,y, gamma = 1, iteration = 50)
    network.save_weights()
