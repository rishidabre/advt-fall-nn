#!/usr/bin/python

from sys import argv
from collections import defaultdict

if len(argv)!=2:
	print "Usage: %s <filename>"%argv[0]
	quit()

fname=argv[1]

rows={}
show_count={}
with open(fname, 'r') as f:
	for line in f:
		arr=line.replace('\n','').replace('\r','').split('\t')
		t=int(arr[3].replace(',',''))
		a=int(arr[4].replace(',',''))
		f=(t-a)/float(a)
		ad=arr[0]
		show=arr[1]
		if not rows.get(ad):
			rows[ad]=defaultdict(list)
		rows[ad][show].append(f)
		x=show_count.get(show)
		if not x:
			show_count[show]=0
		show_count[show] += 1

shows=defaultdict(list)
common_shows=[]
for k,v in rows.iteritems():
	for k2 in v:
		shows[k].append(k2)
	common_shows.extend(shows[k])
	#for k1,k2 in v.iteritems():
	#	print k,k1,len(k2)

for s in common_shows:
	for k,v in rows.iteritems():
		if s not in v:
			common_shows.remove(s)

print common_shows

for s,c in show_count.items():
	if s in common_shows:
		print s,c
	else:
		del show_count[s]

print "Max Count Show: ",
y=max(show_count,key=lambda x: show_count[x])
print y,show_count[y]
