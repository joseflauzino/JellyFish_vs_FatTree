import networkx as nx#instalei
import matplotlib as matplot #instalei
#matplot.use('Agg')
import matplotlib.pyplot as plot #instalei
import random
import pickle
from itertools import islice

def compute_ecmp_paths(G, num_switches):
	ecmp_paths = {}
	for a in range(num_switches):
	    for b in range(a+1, num_switches):
		shortest_paths = nx.all_shortest_paths(G, source=str(a), target=str(b))
		ecmp_paths[(str(a), str(b))] = [p for p in shortest_paths]
	return ecmp_paths

def compute_k_shortest_paths(G, num_switches, k=8):
	all_ksp = {}
	for a in range(num_switches):
	    for b in range(a+1, num_switches):
		ksp = list(islice(nx.shortest_simple_paths(G, source=str(a), target=str(b)), k))
		all_ksp[(str(a), str(b))] = ksp
	return all_ksp

def draw_graph(G):
	plot.subplot(111)
	nx.draw_networkx(G)
	plot.savefig("graphs_figures/graph.png")

def get_path_counts(ecmp_paths, all_ksp, traffic_matrix, all_links):
	counts = {}
	# initialize counts for all links
	for link in all_links:
	    a, b = link
	    print "a: %s" % a
	    print "b: %s" % b
	    counts[(str(a),str(b))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	    print "Counts: %s" % counts[a,b]
	    counts[(str(b),str(a))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	    print "Counts: %s" % counts[b,a]
	for start_host in range(len(traffic_matrix)):
		dest_host = traffic_matrix[start_host]
		start_node = start_host/3
		dest_node = dest_host/3
		if start_node == dest_node:
		    continue
		# swap them so that start_node < dest_node
		if start_node > dest_node:
			start_node, dest_node = dest_node, start_node
		paths = ecmp_paths[(str(start_node), str(dest_node))]
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
				counts[link]["8-ecmp"] += 1
			    counts[link]["64-ecmp"] += 1
			    prev_node = node

		ksp = all_ksp[(str(start_node), str(dest_node))]
		for path in ksp:
		    prev_node = None
		    for node in path:
			if not prev_node:
                            prev_node = node
                            continue
                        link = (str(prev_node), str(node))
			counts[link]["8-ksp"] += 1
			prev_node = node
	
	return counts


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
	'''
{
	('1', '0'): {'8-ksp': 0, '8-ecmp': 0, '64-ecmp': 0}, 
	('0', '2'): {'8-ksp': 2, '8-ecmp': 0, '64-ecmp': 0}, 
	('2', '1'): {'8-ksp': 2, '8-ecmp': 0, '64-ecmp': 0}, 
	('2', '0'): {'8-ksp': 0, '8-ecmp': 0, '64-ecmp': 0}, 
	('0', '1'): {'8-ksp': 2, '8-ecmp': 2, '64-ecmp': 2}, 
	('1', '2'): {'8-ksp': 0, '8-ecmp': 0, '64-ecmp': 0}}'''
	#print ksp_distinct_paths_counts
#	print ecmp_8_distinct_paths_counts
#	print ecmp_64_distinct_paths_counts
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
	plot.savefig("graphics/%s.png" % file_name)
	    
def save_file(data, name):
    with open('routes/'+ name + '.pkl', 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

def load_file(name ):
    with open('routes/' + name + '.pkl', 'rb') as file:
        return pickle.load(file)

# Code adapted from:
# https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
def random_derangement(n):
    while True:
        v = range(n)
        for j in range(n - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return tuple(v)