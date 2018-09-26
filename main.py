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
		
		G = nx.random_regular_graph(num_links, num_switches)
		adj_list_file_name = "adjList_"+file_name
		nx.write_adjlist(G, adj_list_file_name)
		G = nx.read_adjlist(adj_list_file_name)
		
		list_ecmp = ecmp_paths(G, num_switches)
		save_obj(list_ecmp, "ecmp_%s" % (file_name))
		
		list_ksp = k_shortest_paths(G, num_switches)
		save_obj(list_ksp, "ksp_%s" % (file_name))
		
		derangement = derange(numHosts)
		all_links = G.edges()
		num_paths = get_path_counts(list_ecmp, list_ksp, derangement, all_links)
		
		make_graphic(num_paths, file_name)
		
		transformed_ksp_routes = transform_paths_dpid("ksp_%s" % (file_name), num_switches, 8)
		save_routing_table(transformed_ksp_routes, "ksp_%s" % (file_name))

		transformed_ecmp_routes = transform_paths_dpid("ecmp_%s" % (file_name), num_switches, 8)
		save_routing_table(transformed_ecmp_routes, "ecmp_8_%s" % (file_name))
		print "FINISHED: Figure 9 is in figures/ folder"
	else:
		print "Error: incorrect parameters"
		print "After 'main' add the number of switches, the number of links and the number hosts"
		print "Example to use 10 switches with 4 links each and 5 hosts: python main.py 10 4 5"
if __name__ == "__main__":
	main()

