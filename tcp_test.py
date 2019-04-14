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

# Script call tcp_test.py name_of_adjust_file number_switches number_ports number_parellel_flows output_file
def main():
	nSwitches = sys.argv[2]
	nPorts = sys.argv[3]
	nFlows = sys.argv[4]
	adjlist_file = sys.argv[1]

	jelly_topo = JellyfishTopo(nSwitches, nPorts, adjlist_file)
	randomHosts = jelly_topo.hosts()
	random.shuffle(randomHosts)
	clients = randomHosts[0::2]
	servers = randomHosts[1::2]
	pairs_list = zip(clients, servers)
	output_file = sys.argv[5]
	for pair in pairs_list:
		print pair[1] + " iperf -s &"
		print pair[0] + " iperf -c %s -P " + nFlows + " -t 60 >> " + "results/" + output_file + " &" %(pair[1])
	
if __name__ == '__main__':
	main()
