import os
import sys
sys.path.insert(0, "lib/")
from utils import *
from functions import *

def main():
	param = sys.argv
	if len(param) >= 4:
		num_switches = int(param[1])
		num_links = int(param[2])
		numHosts = int(param[3])
	
		list_ecmp = {}
		list_ksp = {}
		file_name = "%slinks_%ssw" % (num_links, num_switches)
		
		print "---- Creating the network ----"
		print "Step 1: Generating the Random Regular Graph...",
		G = nx.random_regular_graph(num_links, num_switches)
		if(G):
			print "OK"
		else:
			print "Error"
		print "Step 2: Creating adjacency list file...",
		adj_list_file_name = "adjList_"+file_name
		nx.write_adjlist(G, adj_list_file_name)
		if(nx):
			print "OK"
		else:
			print "Error"
		print "Step 3: Reading adjacency list file...",
		G = nx.read_adjlist(adj_list_file_name)
		if(G):
			print "OK"
		else:
			print "Error"

		print ""
		print "---- Computing paths ----"
		print "Step 1: Computing ECMP paths...",
		list_ecmp = ecmp_paths(G, num_switches)
		print "Step 2: Saving ECMP paths file...",
		save_obj(list_ecmp, "ecmp_%s" % (file_name))
		print "Step 3: Computing K-shortest-paths...",
		list_ksp = k_shortest_paths(G, num_switches)
		print "Step 4: Saving K-shortest-paths file...",
		save_obj(list_ksp, "ksp_%s" % (file_name))
		
		print ""
		print "---- Making the graphic ----"
		derangement = derange(numHosts)
		print "Step 2: Getting all links...",
		all_links = G.edges()
		print "OK"
		num_paths = get_path_counts(list_ecmp, list_ksp, derangement, all_links)
		make_graphic(num_paths, file_name)
		print ""
		print "---- Transforming routes for Ripl/Riplpox use ----"
		print "Step 1: Transforming KSP...",
		transformed_ksp_routes = transform_paths_dpid("ksp_%s" % (file_name), num_switches, 8)
		print "Step 2: Saving KSP routes file...",
		save_routing_table(transformed_ksp_routes, "ksp_%s" % (file_name))

		print "Step 3: Transforming ECMP 8...",
		transformed_ecmp_routes = transform_paths_dpid("ecmp_%s" % (file_name), num_switches, 8)
		print "Step 4: Saving ECMP 8 routes file...",
		save_routing_table(transformed_ecmp_routes, "ecmp_%s" % (file_name))
		print ""
		print "FINISHED: Figure 9 is in figures/ folder"
	else:
		print "Error: incorrect parameters"
		print "After 'main' add the number of switches, the number of links and the number hosts"
		print "Example to use 10 switches with 4 links each and 5 hosts: python main.py 10 4 5"
if __name__ == "__main__":
	main()