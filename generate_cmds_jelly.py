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
from ripl.ripl.dctopo import JellyfishTopo

def main():
	param = sys.argv
	if len(param) >= 4:
		num_switches = int(param[1])
		num_ports = int(param[2])
		num_flows = int(param[3])
		adjlist_file = param[4]
		out_file = param[5]

		jelly_topo = JellyfishTopo(num_switches, num_ports, adjlist_file,out_file)
		randomHosts = jelly_topo.hosts()
		random.shuffle(randomHosts)
		clients = randomHosts[0::2]
		servers = randomHosts[1::2]
		pairs_list = zip(clients, servers)
		
		for pair in pairs_list:
			print pair[1] + " iperf -s &"
			#print pair[0] + " iperf -c %s -P %s -t 15 >> outputs/jelly/%s_%sflows.txt &" %(pair[1], num_flows, out_file, num_flows) 
			if pair == pairs_list[len(pairs_list) - 1]:
				print pair[0] + " iperf -c %s -P %s -t 15 -b 10M >> outputs/jelly/%s_%sflows.txt" %(pair[1], num_flows, out_file, num_flows) 
			else:
				print pair[0] + " iperf -c %s -P %s -t 15 -b 10M >> outputs/jelly/%s_%sflows.txt &" %(pair[1], num_flows, out_file, num_flows) 
	else:
		print "Error: incorrect parameters"
		print "After 'generate_cmds.py' add the number of switches, the number of ports and adjacency list file name."
		print "Example to use 10 switches with 4 ports each and the adjacency list file named 'adjList_10sw_3links_5hosts': python generate_cmds.py 10 4 adjList_10sw_3links_5hosts"
	
if __name__ == '__main__':
	main()