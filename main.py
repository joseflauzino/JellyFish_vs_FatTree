import os
import sys
from utils import *
from functions import *

def main():
	param = sys.argv
	if len(param) >= 4:
		num_switches = int(param[1])
		num_ports = int(param[2])
		num_servers = int(param[3])

		ecmp_paths = {}
		all_ksp = {}
		file_name = "plot_%ssw_%sports_%sservers" % (num_switches, num_ports, num_servers)
		
		print "---- Creating the network ----"
		print "Step 1: Generating the Random Regular Graph"
		G = nx.random_regular_graph(num_ports, num_switches)
		draw_graph(G)
		print "Step 2: Creating adjacency list file"
		nx.write_adjlist(G, file_name)
		print "Step 3: Reading adjacency list file"
		G = nx.read_adjlist(file_name)


		print ""
		print "---- Computing paths ----"
		print "Step 1: Computing ECMP paths"
		ecmp_paths = compute_ecmp_paths(G, num_switches)
		print "Step 2: Saving ECMP paths file"
		save_file(ecmp_paths, "ecmp_%s" % (file_name))
		print "Step 3: Computing K-shortest-paths"
		all_ksp = compute_k_shortest_paths(G, num_switches)
		print "Step 4: Saving K-shortest-paths file"
		save_file(all_ksp, "ksp_%s" % (file_name))
		
		print ""
		print "---- Making the graphic ----"
		print "Step 1: Random Derangement"
		derangement = random_derangement(num_servers)
		print "Step 2: Getting all links"
		all_links = G.edges()
		print "All links: %s" % all_links
		print "Step 3: Counting the paths"
		num_paths = get_path_counts(ecmp_paths, all_ksp, derangement, all_links)
		#print "Counts: %s" % num_paths
		print "Step 4: Mounting the plot"
		make_graphic(num_paths, file_name)
		
		# aqui comeca a usar o utils
		print ""
		print "---- Transforming routes for Ripl/Riplpox use ----"
		print "Step 1: Transforming KSP"
		transformed_ksp_routes = transform_paths_dpid("ksp_%s" % (file_name), num_servers, 8)
		print "Step 2: Saving KSP routes file"
		save_routing_table(transformed_ksp_routes, "ksp_%s" % (file_name))
		print "Step 3: Transforming ECMP 8"
		transformed_ecmp_routes = transform_paths_dpid("ecmp_%s" % (file_name), num_servers, 8)
		print "Step 4: Saving ECMP 8 routes file"
		save_routing_table(transformed_ecmp_routes, "ecmp_8_%s" % (file_name))

		print ""
		print "FINISHED: Figure 9 is in graphics/ folder"

	else:
		print "Error: incorrect parameters"
		print "After 'main' add the number of switches, the number of ports and the number servers"
		print "Example to use 10 switches with 4 ports each and 5 servers: python main.py 10 4 5"
	
if __name__ == "__main__":
	main()