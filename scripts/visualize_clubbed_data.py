#!/usr/bin/python

import numpy as np
from numpy.random import randn
from pylab import plot,ylim,show,legend,xlabel,ylabel,title
from sys import argv

if len(argv)!=2:
	print "Usage: %s <filename>"%(argv[0])
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

dataset = []
with open(fname,'r') as f:
        for line in f:
                arr = line.replace('\n','').replace('\r','').split(',')
                op = float(arr[1])
                if op>10:
                        continue
                dataset.append([int(arr[0]),op])

minmax = dataset_minmax(dataset)
normalize_dataset(dataset, minmax)

inputs = []
outputs = []

for row in dataset:
        inputs.append(row[0:-1])
        outputs.append(row[1:])

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

cols = X.T

xlabel("Instances")
ylabel("Inputs and Outputs")
title("Data Visualization")
plot(inputs, label='Clubbed inputs')
plot(outputs, label='Fall-off')#, 'r')
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
show()
