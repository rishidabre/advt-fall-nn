#!/usr/bin/python

from sys import argv

if len(argv)!=2:
	print "usage: %s <filename>"%argv[0]
	quit()

shows=[]
networks=[]
with open(argv[1], 'r') as f_ori:
	with open(argv[1][:-4]+"_enc.txt","w") as f_new:
		fs = open('show_map.txt','w')
		fn = open('network_map.txt','w')
		for line in f_ori:
			arr=line.replace('\n','').replace('\r','').split(',')
			show=arr[0]
			network=arr[1]
			if show not in shows:
				shows.append(show)
				fs.write("%s	%s\n"%(shows.index(show),show))
			sid=shows.index(show)
			if network not in networks:
				networks.append(network)
				fn.write("%s	%s\n"%(networks.index(network),network))
			nid=networks.index(network)
			f_new.write("%s,%s,%s\n"%(sid,nid,arr[4]))
print "Done!"
