import os, sys
from functions import *

def main():
	param = sys.argv
	if len(param) >= 4:
		num_switches = int(param[1])
		num_links = int(param[2])
		num_servers = int(param[3])

		list_ecmp = {}
		list_ksp = {}
		file_name = "%ssw_%slinks_%shosts" % (num_switches, num_links, num_servers)
		
		print "---- Creating the network ----"
		G = nx.random_regular_graph(num_links, num_switches)
		draw_graph(G,file_name)
		adj_list_file_name = "adj_list/adjList_"+file_name
		nx.write_adjlist(G, adj_list_file_name)
		G = nx.read_adjlist(adj_list_file_name)

		print "---- Computing paths ----"
		list_ecmp = ecmp_paths(G, num_switches)
		save_file(list_ecmp, "ecmp_%s" % (file_name))
		list_ksp = k_shortest_paths(G, num_switches)
		save_file(list_ksp, "ksp_%s" % (file_name))
		
		print "---- Making the graphic ----"
		derangement = derange(num_servers)
		print "derangement: %s" % (derangement,)
		
		#teste_derangements = derangements(num_servers)
		#print "my derangement: %s" % (teste_derangements,)

		all_links = G.edges()
		num_paths = get_path_counts(list_ecmp, list_ksp, derangement, all_links)
		make_graphic(num_paths, file_name)
		

		print ""
		print "FINISHED: Figure 9 is in graphics/ folder"

	else:
		print "Error: incorrect parameters"
		print "After 'main' add the number of switches, the number of ports and the number servers"
		print "Example to use 10 switches with 4 ports each and 5 servers: python main.py 10 4 5"
	
if __name__ == "__main__":
	main()