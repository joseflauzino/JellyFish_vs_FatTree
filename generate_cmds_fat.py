import os
import sys
import pdb
import random
import pickle
from itertools import islice
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.node import OVSController
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.util import quietRun
import random
from subprocess import Popen, PIPE
from time import sleep, time
from ripl.ripl.dctopo import FatTreeTopo

def main():
	param = sys.argv
	if len(param) >= 3:
		pods = int(param[1])
		flows = int(param[2])
		route_proto = param[3]

		fat_topo = FatTreeTopo(pods)
		randomHosts = fat_topo.hosts()
	 	random.shuffle(randomHosts)
	 	clients = randomHosts[0::2]
	 	servers = randomHosts[1::2]
	 	pairs_list = zip(clients, servers)

		for pair in pairs_list:
			print pair[1] + " iperf -s &"
			#print pair[0] + " iperf -c %s -P %s -t 15 >> outputs/fat/%s_fat_%spods_%sflows.txt &" % (pair[1], flows, route_proto, pods, flows)
			
			if pair == pairs_list[len(pairs_list) - 1]:
				print pair[0] + " iperf -c %s -P %s -t 15 -b 10M >> outputs/fat/%s_fat_%spods_%sflows.txt" % (pair[1], flows, route_proto, pods, flows)
			else:
				print pair[0] + " iperf -c %s -P %s -t 15 -b 10M >> outputs/fat/%s_fat_%spods_%sflows.txt &" % (pair[1], flows, route_proto, pods, flows) 
	else:
		print "Error: incorrect parameters"
		print "After 'generate_cmds_fat.py' add the number of pods, the number of ports and adjacency list file name."
		print "Example to use 4 pods with 4 ports each and the adjacency list file named 'adjList_10sw_3links_5hosts': python generate_cmds.py 10 4 adjList_10sw_3links_5hosts"

if __name__ == '__main__':
	main()