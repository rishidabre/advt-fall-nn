#!/usr/bin/python

from sys import argv

if len(argv)!=3:
	print "usage: %s <filename> <newfilename>"%argv[0]
	quit()

special_names={}
with open('../data/special_names.txt','r') as f:
	for line in f:
		arr=line.replace('\n','').replace('\r','').split('\t')
		special_names[arr[1]]=arr[0]

shows=[]
networks=[]
with open(argv[1], 'r') as f_ori:
	with open(argv[2],"w") as f_new:
		fs = open('show_map.txt','w')
		fn = open('network_map.txt','w')
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
			if show not in shows:
				shows.append(show)
				fs.write("%s	%s\n"%(shows.index(show),show))
			sid=shows.index(show)
			if network not in networks:
				networks.append(network)
				fn.write("%s	%s\n"%(networks.index(network),network))
			nid=networks.index(network)
			if f<0.0:
				f=0.0
			f_new.write("%s,%s,%s\n"%(sid,nid,f))
print "Done!"
