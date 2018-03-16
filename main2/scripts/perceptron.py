#!/usr/bin/python

from sys import argv

wins_param = "[-winsorize]"
winsorize = False

if len(argv)>2:
    print "Usage: %s %s"%(argv[0], wins_param)
    quit()
elif len(argv) == 2:
    if argv[1]!=wins_param[1:-1]:
        print "Usage: %s %s"%(argv[0], wins_param)
        quit()
    else:
        winsorize = True

from random import choice
from numpy import array, dot, random, loadtxt
from pylab import plot, ylim, show
from math import fabs
from scipy import stats

#unit_step = lambda x: 0 if x<0 else 1
unit_step = lambda x: 2 if fabs(x)>fabs(2-x) else 1
exp_value = lambda x: 2 if x>2 else 1

training_data=loadtxt('lenses.data', dtype='int')

if winsorize:
    print "Before winsorizing: "
    print training_data
    t = []
    for d in training_data:
        t.append(stats.mstats.winsorize(d, limits=0.5))
    training_data = array(t)
    print "After winsorizing: "
    print training_data

w = random.rand(5)
#w = [1,1,1,1,1]
errors = []
eta = 0.01
n = 100

for i in xrange(n):
    data = choice(training_data)
#    x = data[1:5]
    y = []
    for i in data[1:5]:
        y.append(i)
    y.append(1) #Bias weight
    x = array(y)
    expected = data[5]
    result = dot(w, x)
    error = exp_value(expected) - unit_step(result)
    errors.append(error)
    w += eta * error * x

total = len(training_data)
accuracy = total

for x in training_data:
    y = []
    for i in x[1:5]:
        y.append(i)
    y.append(1)
    result = dot(y, w)
    fin_val = unit_step(result)
    if fin_val != exp_value(x[5]):
        accuracy -= 1
    print("{}: {} -> {}".format(x[1:5], result, fin_val))

print "Accuracy: {}%".format(((float(accuracy))/total)*100)
ylim([-2,2])
plot(errors)
show()
