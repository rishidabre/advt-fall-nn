#!/usr/bin/python

from sys import argv

if len(argv)!=2:
	print "usage: %s <filename>"%argv[0]
	quit()

classes=[]
with open(argv[1], 'r') as f_ori:
	with open(argv[1][:-4]+"_enc.txt","w") as f_new:
		fmap = open(argv[1][:-4]+"_map.txt",'w')
		for line in f_ori:
			arr=line.replace('\n','').replace('\r','').split(',')
			print arr
			clas=arr[4]
			if clas not in classes:
				classes.append(clas)
				fmap.write("%s	%s\n"%(classes.index(clas)+1,clas))
			cid=classes.index(clas)+1
			f_new.write("%s,%s,%s,%s,%s\n"%(arr[0],arr[1],arr[2],arr[3],cid))
print "Done!"
