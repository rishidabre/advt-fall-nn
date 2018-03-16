#!/usr/bin/python

import numpy as np
from numpy.random import randn
from pylab import plot,ylim,show,legend,xlabel,ylabel,title
from sys import argv

if len(argv)!=3:
        print "Usage: %s <train_file> <test_file>"%argv[0]
        quit()

# Input filename
fname = argv[1]
fname2 = argv[2]

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
#                       [1],
#                       [1],
#                       [0]])
y = np.array(outputs)

np.random.seed(1)

N, D_in, H, D_out = len(inputs), len(inputs[0]), 3, 1
#x, y = randn(N, D_in), randn(N, D_out)
w1, w2 = randn(D_in, H), randn(H, D_out)

for t in range(20000):
	h = 1 / (1 + np.exp(-X.dot(w1)))
	y_pred = h.dot(w2)
	loss = np.square(y_pred - y).sum()
	print(t, loss)

	grad_y_pred = 2.0 * (y_pred - y)
	grad_w2 = h.T.dot(grad_y_pred)
	grad_h = grad_y_pred.dot(w2.T)
	grad_w1 = X.T.dot(grad_h * h * (1 - h))

	w1 -= 1e-4 * grad_w1
	w2 -= 1e-4 * grad_w2

print w1, w2

###########################################
###	Logic to read test data set	###
###########################################

dataset = []
with open(fname2,'r') as f:
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
#                       [1],
#                       [1],
#                       [0]])
y = np.array(outputs)

np.random.seed(1)

N, D_in, H, D_out = len(inputs), len(inputs[0]), 3, 1

h = 1 / (1 + np.exp(-X.dot(w1)))
y_pred = h.dot(w2)
loss = np.square(y_pred - y).sum()

errors = outputs - y_pred
print errors

xlabel("Instances")
ylabel("Error")
title("Errors (Expected - Actual)")
plot(errors),show()
xlabel("Instances")
ylabel("Output")
title("Output (Expected and Actual)")
plot(outputs, label='Expected')#, 'b')
plot(y_pred, label='Actual')#, 'r')
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
show()
