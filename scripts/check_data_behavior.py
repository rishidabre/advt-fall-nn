#!/usr/bin/python

from sys import argv
from collections import defaultdict

if len(argv)!=2:
	print "usage: %s <filename>"%argv[0]
	quit()

special_names={}
with open('../data/special_names.txt','r') as f:
	for line in f:
		arr=line.replace('\n','').replace('\r','').split('\t')
		special_names[arr[1]]=arr[0]

clubbed_data=defaultdict(list)
with open(argv[1], 'r') as f_ori:
	for line in f_ori:
		arr=line.replace('\n','').replace('\r','').split(',')
		offset=0
		for k,v in special_names.iteritems():
			if k in line:
				show=k
				offset=int(v)
				break
		if offset==0:
			show=arr[0]
		network=arr[1+offset]
		f=float(arr[4+offset])
		aud=int(arr[2+offset])
		if aud<500000:
			continue
		if f<0.0:
			f=0.0
		clubbed = show+network
		if clubbed not in clubbed_data.keys():
			clubbed_data[clubbed].append(f)
for k,v in clubbed_data.iteritems():
	if len(v)>1:
		print k,v
print "Done!"
