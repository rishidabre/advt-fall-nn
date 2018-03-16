#!/usr/bin/python

import numpy as np
from pylab import plot, ylim, show

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

inputs = []
outputs = []
with open('../data/test_data.txt','r') as f:
	for line in f:
		arr = line.replace('\n','').replace('\r','').split(',')
		inputs.append([float(int(arr[0])),int(arr[1])])
		outputs.append(float(arr[2]))

# input dataset
#X = np.array([  [0,0,1],
#                [0,1,1],
#                [1,0,1],
#                [1,1,1] ])
X = np.array(inputs)
    
# output dataset            
#y = np.array([[0,0,1,1]]).T
y = np.array([outputs]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((2,1)) - 1
print syn0

for iter in xrange(10000):

    # forward propagation
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))

    # how much did we miss?
    l1_error = y - l1

    # multiply how much we missed by the 
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * nonlin(l1,True)

    # update weights
    delta = np.dot(l0.T,l1_delta)
    print delta
    syn0 += delta
#print "Output After Training:"
#print l1

errors = []
for i in range(len(outputs)):
	error = outputs[i] - l1[i]
	errors.append(error)
	if error>2:
		print "Inputs: %s,%s - Expected: %s - Actual: %s"%(inputs[i][0],inputs[i][1],outputs[i],l1[i])
ylim([-2,2]),plot(errors, 'r',l1, 'b'),show()
