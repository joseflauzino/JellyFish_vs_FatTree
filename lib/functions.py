import networkx as nx
import matplotlib as mpl
import random
mpl.use('Agg')
import matplotlib.pyplot as plot
import pickle
from itertools import islice

def ecmp_paths(networkx_graph, n):
	ecmp_paths = {}
	for a in range(n):
	    for b in range(a+1, n):
		shortest_paths = nx.all_shortest_paths(networkx_graph, source=str(a), target=str(b))
		ecmp_paths[(str(a), str(b))] = [p for p in shortest_paths]
	print "OK"
	return ecmp_paths

def k_shortest_paths(networkx_graph, n, k=8):
	all_ksp = {}
	for a in range(n):
	    for b in range(a+1, n):
		ksp = list(islice(nx.shortest_simple_paths(networkx_graph, source=str(a), \
								target=str(b)), k))
		all_ksp[(str(a), str(b))] = ksp
	print "OK"
	return all_ksp

def get_path_counts(ecmp_paths, all_ksp, traffic_matrix, all_links):
	print "Step 3: Counting the paths...",
	counts = {}
	for link in all_links:
	    a, b = link
	    counts[(str(a),str(b))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	    counts[(str(b),str(a))] = {"8-ksp":0, "8-ecmp": 0, "64-ecmp": 0} 
	for start_host in range(len(traffic_matrix)):
		dest_host = traffic_matrix[start_host]
		start_node = start_host/3
		dest_node = dest_host/3
		if start_node == dest_node:
		    continue
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
	print "OK"
	return counts

def make_graphic(num_paths, file_name):
	print "Step 4: Mounting the plot...",
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
	plot.savefig("figures/%s.png" % file_name)
	print "OK"

def save_obj(obj, name):
    with open('pickled_routes/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    print "OK"

def load_obj(name ):
    with open('pickled_routes/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    print "OK"

def derange(n):
	print "Step 1: Random Derangement...",
	s = range(n)
	d=s[:]
	while any([a==b for a,b in zip(d,s)]):random.shuffle(d)
	print "OK"
	return d
