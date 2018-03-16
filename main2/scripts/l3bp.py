#!/usr/bin/python

import numpy as np
from pylab import plot,ylim,show,legend,xlabel,ylabel,title
from sys import argv

if len(argv)!=2:
	print "Usage: %s <filename>"%argv[0]
	quit()

# Input filename
fname = argv[1]

# Find the min and max values for each column
def dataset_minmax(dataset):
        minmax = list()
        stats = [[min(column), max(column)] for column in zip(*dataset)]
        return stats

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
        for row in dataset:
                for i in range(len(row)-1):
                        try:
                                row[i] = (row[i] - minmax[i][0]) / float((minmax[i][1] - minmax[i][0]))
                        except ZeroDivisionError:
                                row[i] = (row[i] - minmax[i][0]) / 0.0001

def nonlin(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))

dataset = []
with open(fname,'r') as f:
        for line in f:
                arr = line.replace('\n','').replace('\r','').split(',')
		op = float(arr[2])
		if op>10:
			continue
		dataset.append([int(arr[0]),int(arr[1]),op])

minmax = dataset_minmax(dataset)
normalize_dataset(dataset, minmax)

inputs = []
outputs = []

for row in dataset:
	inputs.append(row[0:-1])
	outputs.append(row[2:])

#X = np.array([[0,0,1],
#            [0,1,1],
#            [1,0,1],
#            [1,1,1]])
X = np.array(inputs)               
#y = np.array([[0],
#			[1],
#			[1],
#			[0]])
y = np.array(outputs)

np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = np.random.random((2,5)) - 1
syn1 = np.random.random((5,1)) - 1

mses = []
for j in xrange(10000):

    # Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

    # how much did we miss the target value?
    l2_error = y - l2
    
    if (j% 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error)))
        
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

#    mse = 0
#    for i in range(len(outputs)):
#        error = outputs[i] - l2[i]
#        if error>2:
#            print "Inputs: %s,%s - Expected: %s - Actual: %s"%(inputs[i][0],inputs[i][1],outputs[i],l2[i])
#        else:
#            mse += (error**2)
#    mses.append(mse)

#xlabel("Iterations")
#ylabel("Mean Squared Error (MSE)")
#title("Mean Squared Error Propagation")
#plot(mses),show()

errors = []
for i in range(len(outputs)):
        error = outputs[i] - l2[i]
        if error>2:
                print "Inputs: %s,%s - Expected: %s - Actual: %s"%(inputs[i][0],inputs[i][1],outputs[i],l2[i])
	else:
        	errors.append(error)

xlabel("Instances")
ylabel("Error")
title("Errors (Expected - Actual)")
plot(errors),show()
xlabel("Instances")
ylabel("Output")
title("Output (Expected and Actual)")
plot(outputs, label='Expected')#, 'b')
plot(l2, label='Actual')#, 'r')
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
show()
