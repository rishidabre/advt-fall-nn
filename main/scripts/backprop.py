#!/usr/bin/python

# Backprop on the Ionosphere Dataset
from random import seed
from random import randrange
from random import random
from csv import reader
from math import exp
from collections import defaultdict
from numpy import arange
from pylab import plot, ylim, show
from time import time
from pickle import dump

# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup

# Find the min and max values for each column
def dataset_minmax(dataset):
	print dataset
	minmax = list()
	stats = [[min(column), max(column)] for column in zip(*dataset)]
	return stats

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
	for row in dataset:
		for i in range(len(row)-1):
			try:
				row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
			except ZeroDivisionError:
				row[i] = (row[i] - minmax[i][0]) / 0.0001

# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0

# Calculate and return errors
def get_errors(actual, predicted):
	errors = []
        for i in range(len(actual)):
                errors.append(actual[i] - predicted[i])
        return errors

# Load the cost matrix from file
def load_cost_matrix():
	cost_matrix=[]
	with open('cost_matrix.csv', 'r') as f:
		for line in f:
			cost_matrix.append(line.replace('\n','').split(','))
        for i in range(len(cost_matrix[0])):
                str_column_to_float(cost_matrix, i)
	return cost_matrix

# Calculate the total misclassification cost
def calculate_misclassification_cost(confusion):
	cost_matrix=load_cost_matrix()
	misclass_cost=defaultdict(dict)
	total_cost=0
	for i in xrange(len(cost_matrix)):
		for j in xrange(len(cost_matrix[i])):
			misclass_cost[i][j]=round(confusion[i][j]*cost_matrix[i][j],2)
			total_cost+=misclass_cost[i][j]
	#print misclass_cost
	return total_cost

# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
	folds = cross_validation_split(dataset, n_folds)
	all_errors = list()
	i=1
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		#accuracy = accuracy_metric(actual, predicted)
		errors = get_errors(actual, predicted)
		all_errors.append(errors)
		print "Completed fold %s of %s."%(i, n_folds)
		i+=1
	return all_errors

# Calculate neuron activation for an input
def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation

# Transfer neuron activation
def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))

# Forward propagate input to a network output
def forward_propagate(network, row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = transfer(activation)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs

# Calculate the derivative of an neuron output
def transfer_derivative(output):
	return output * (1.0 - output)

# Plot errors
def plot_errors(errors):
	#ylim([-2,2])
	plot(errors)
	show()

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
#	cost_matrix=load_cost_matrix()
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		#plot_errors(errors)
		#print errors
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update network weights with error
def update_weights(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] += l_rate * neuron['delta']

# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
	for epoch in range(n_epoch):
		i=0
		for row in train:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(n_outputs)]
			#expected[row[-1]] = 1
			expected[i] = 1
			i+=1
			backward_propagate_error(network, expected)
			update_weights(network, row, l_rate)

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
	network = list()
	hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
	network.append(hidden_layer)
	output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	return network

# Make a prediction with a network
def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))

# Backpropagation Algorithm With Stochastic Gradient Descent
def back_propagation(train, test, l_rate, n_epoch, n_hidden):
	n_inputs = len(train[0]) - 1
	n_outputs = len(set([row[-1] for row in train]))
	network = initialize_network(n_inputs, n_hidden, n_outputs)
	train_network(network, train, l_rate, n_epoch, n_outputs)
	predictions = list()
	for row in test:
		prediction = predict(network, row)
		predictions.append(prediction)
	return(predictions)

#print load_cost_matrix()
#quit()

t = time()*1000
# Cover different learning rates
for l_rate in [0.1]:#arange(0.1, 1.1, 0.1):
        # Cover different epochs
        for n_epoch in [50]:#, 100, 500]:
                print "Running Backprop for Learning Rate %s and Epochs %s"%(l_rate, n_epoch)
		# Test Backprop on Ionosphere dataset
		seed(1)
		# load and prepare data
		filename = '../data/test_data_2.txt'
		dataset = load_csv(filename)
		for i in range(len(dataset[0])-1):
			#str_column_to_float(dataset, i)
			str_column_to_int(dataset, i)
#		# convert class column to integers
#		str_column_to_int(dataset, len(dataset[0])-1)
		# Convert class column to float
		str_column_to_float(dataset, len(dataset[0])-1)
		# normalize input variables
		minmax = dataset_minmax(dataset)
		normalize_dataset(dataset, minmax)
		# evaluate algorithm
		n_folds = 2
		#l_rate = 0.3
		#n_epoch = 500
		n_hidden = 10
		all_errors = evaluate_algorithm(dataset, back_propagation, n_folds, l_rate, n_epoch, n_hidden)
		#print('Errors: %s' % scores)
		#mean_acc = (sum(scores)/float(len(scores)))
		#print('Mean Accuracy: %.3f%%' % mean_acc)
		i=1
		for errors in all_errors:
			f=open("errors%s"%i, 'w')
			dump(errors, f)
			f.close()
			i=i+1
			plot_errors(errors)
print "Finished running in %s second(s)."%(time()*1000-t)
