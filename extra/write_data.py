#!/usr/bin/python

from sys import argv
from collections import defaultdict

if len(argv)!=5:
	print "Usage: %s <filename> <newfilename> <--omit-ad=> <--show-name=showname>"%argv[0]
	quit()

fname=argv[1]
newfname=argv[2]

omitad=False
if argv[3] == "--omit-ad":
	omitad=True

selected_show=""
if "--show-name" in argv[4]:
	selected_show=argv[4].split('=')[1]

rows={}
with open(fname, 'r') as f:
	with open(newfname, 'w') as f_new:
		for line in f:
			arr=line.replace('\n','').replace('\r','').split('\t')
			t=int(arr[3].replace(',',''))
			a=int(arr[4].replace(',',''))
			f=(t-a)/float(a)
			ad=arr[0]
			if not rows.get(ad):
				rows[ad]=defaultdict(list)
			show=arr[1]
			if selected_show != "" and show != selected_show:
				continue
			rows[ad][show].append(f)
			c1=rows.keys().index(ad)
			c2=rows[ad].keys().index(show)
			c3=f
			if omitad:
				f_new.write("%s,%s\n"%(c2+1,0 if c3<0 else c3))
			elif selected_show != "":
				f_new.write("%s,%s\n"%(c1+1,0 if c3<0 else c3))
			else:
				f_new.write("%s,%s,%s\n"%(c1+1,c2+1,0 if c3<0 else c3))

for k,v in rows.iteritems():
	for k1,k2 in v.iteritems():
		print k,k1,len(k2)
