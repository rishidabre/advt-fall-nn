#!/usr/bin/python

from sys import argv

if len(argv)!=2:
	print "usage: %s <filename>"%argv[0]
	quit()

classes=[]
with open(argv[1], 'r') as f_ori:
	with open(argv[1][:-4]+"_cut.txt","w") as f_new:
		for line in f_ori:
			arr=line.replace('\n','').replace('\r','').split(',')
			print arr
			col3=float(arr[2])
			if col3 < 0:
				col3 = 0
			f_new.write("%s,%s,%s\n"%(arr[0],arr[1],col3))
print "Done!"
