# encoding: utf-8
import generate_cmds_fat
import shlex
import subprocess
from subprocess import Popen, PIPE
from multiprocessing import Process
import sys
import os
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.net import Mininet
from ripl.ripl.dctopo import FatTreeTopo
import time

def main():
	param = sys.argv
	if len(param) >= 4:
		pods = int(param[1])
		adjListFile = 'graphFt'
		routeringmode = 'ecmp_8_' # ecmp_8_ or ksp_
		flowsNumber = 8
		num_hosts = (pods ** 3)/4
		hosts = [(str(i)) for i in range (1, num_hosts + 1)]
		generate_cmds_fat.InitTestFt(pods, routeringmode, flowsNumber)
		routingFile = routeringmode + adjListFile

if __name__ == "__main__":
	main()