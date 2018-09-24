import random, pickle, math
import networkx as nx, matplotlib.pyplot as plot
from itertools import islice
from itertools import permutations

def draw_graph(G):
	plot.subplot(111)
	nx.draw_networkx(G, node_size=10, node_color='b',with_labels=False)
	plot.savefig("graphs_figures/graph.png")

def ecmp_paths(G, num_switches):
	list_ecmp = {}
	for i in range(num_switches):
	    for j in range(i+1, num_switches):
		shortest_paths = nx.all_shortest_paths(G, source=str(i), target=str(j))
		list_ecmp[(str(i), str(j))] = [x for x in shortest_paths]
	return list_ecmp

def k_shortest_paths(G, num_switches):
	k=8
	list_ksp = {}
	for i in range(num_switches):
	    for j in range(i+1, num_switches):
		ksp = list(islice(nx.shortest_simple_paths(G, source=str(i), target=str(j)), k))
		list_ksp[(str(i), str(j))] = ksp
	return list_ksp

def get_path_counts(list_ecmp, list_ksp, traffic_matrix, all_links):
	n = {}
	for link in all_links:
	    i, j = link
	    n[(str(i),str(j))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	    n[(str(j),str(i))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	for start_host in range(len(traffic_matrix)):
		dest_host = traffic_matrix[start_host]
		start_node = start_host/3
		dest_node = dest_host/3
		if start_node == dest_node:
		    continue

		if start_node > dest_node:
			start_node, dest_node = dest_node, start_node
		paths = list_ecmp[(str(start_node), str(dest_node))]
		if len(paths) > 64:
		    paths = paths[:64]
		for i in range(len(paths)):
			path = paths[i]
			prev_node = None
			for node in path:
			    if not prev_node:
				prev_node = node
				continue
			    link = (str(prev_node), str(node))
			    if i < 8:
				n[link]["8-ecmp"] += 1
			    n[link]["64-ecmp"] += 1
			    prev_node = node

		ksp = list_ksp[(str(start_node), str(dest_node))]
		for path in ksp:
		    prev_node = None
		    for node in path:
			if not prev_node:
                            prev_node = node
                            continue
                        link = (str(prev_node), str(node))
			n[link]["8-ksp"] += 1
			prev_node = node
	return n

def make_graphic(num_paths, file_name):
	ksp_distinct_paths_counts = []
	ecmp_8_distinct_paths_counts = []
	ecmp_64_distinct_paths_counts = []
	

	for _, value in sorted(num_paths.iteritems(), key=lambda (k,v): (v["8-ksp"],k)):
	    ksp_distinct_paths_counts.append(value["8-ksp"])
	for _, value in sorted(num_paths.iteritems(), key=lambda (k,v): (v["8-ecmp"],k)):
	    ecmp_8_distinct_paths_counts.append(value["8-ecmp"])
	for _, value in sorted(num_paths.iteritems(), key=lambda (k,v): (v["64-ecmp"],k)):
	    ecmp_64_distinct_paths_counts.append(value["64-ecmp"])

	x = range(len(ksp_distinct_paths_counts))
	fig = plot.figure()
	
	axes = fig.add_subplot(111)
	axes.step(x, ksp_distinct_paths_counts, linewidth=5, solid_capstyle='round', color='b', label="8 Shortest Paths")
	axes.step(x, ecmp_64_distinct_paths_counts, linewidth=2, linestyle=':', color='r', label="64-way ECMP")
	axes.step(x, ecmp_8_distinct_paths_counts, color='g', label="8-way ECMP")
	axes.set_xlabel("Rank of Link")
	axes.grid(True, linestyle=':')
	axes.set_ylabel("# Distinct Paths Link is on")

	plot.legend(loc="upper left")
	plot.savefig("graphics/plot_%s.png" % file_name)
	    
def save_file(data, name):
    with open('routes/routes_'+ name + '.pkl', 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

def derange(n):
	s = range(n)
	d=s[:]
	while any([a==b for a,b in zip(d,s)]):random.shuffle(d)
	return d