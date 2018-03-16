#!/usr/bin/python

with open('../data/data_consolidated_enc_2.txt','r') as f1:
	with open('../data/test_data.txt','w') as f2:
		i=0
		for line in f1:
			if i%5==0:
				f2.write(line)
			i+=1
