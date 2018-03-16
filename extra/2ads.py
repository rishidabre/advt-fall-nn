#!/usr/bin/python

from pylab import xlabel,ylabel,title,legend,plot,show
from pickle import load,dump

with open('a','r') as f:
	c=load(f)

with open('b','r') as f:
	d=load(f)

#for i in xrange(len(d)-len(c)):
#	c.append(0)

ylabel("Fall-off [(total audience - ad copy audience)/total audience]")
xlabel("Ad occurrence [not pod number]")
title("Fall-off for 2 different advertisements alongside same show")
plot(c, label='Ad 1 (Amazon) > C & J Gaines: Hearth & Hand Coming Soon')#, 'b')
plot(d, label='Ad 2 (Apple) > Sublime Edition Phone/Sprint')#, 'r')
legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
show()
