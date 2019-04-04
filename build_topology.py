import os
import sys
import networkx
import matplotlib as mpl
import random
import sys
import math
mpl.use('Agg')
import matplotlib.pyplot as plt
import pickle
from itertools import islice
from jelly_utils import *

def compute_ecmp_paths(networkx_graph, n):
    ecmp_paths = {}
    for a in range(n):
        for b in range(a+1, n):
            shortest_paths = networkx.all_shortest_paths(networkx_graph, source=str(a), target=str(b))
            ecmp_paths[(str(a), str(b))] = [p for p in shortest_paths]
    return ecmp_paths

def compute_k_shortest_paths(networkx_graph, n, k=8):
    all_ksp = {}
    for a in range(n):
        for b in range(a+1, n):
            ksp = list(islice(networkx.shortest_simple_paths(networkx_graph, source=str(a), \
                                                            target=str(b)), k))
            all_ksp[(str(a), str(b))] = ksp
    return all_ksp


def get_path_counts(ecmp_paths, all_ksp, traffic_matrix, all_links):
    counts = {}
    # initialize counts for all links
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


def assemble_histogram(path_counts, file_name):
    ksp_distinct_paths_counts = []
    ecmp_8_distinct_paths_counts = []
    ecmp_64_distinct_paths_counts = []
    

    for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["8-ksp"],k)):
        ksp_distinct_paths_counts.append(value["8-ksp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["8-ecmp"],k)):
        ecmp_8_distinct_paths_counts.append(value["8-ecmp"])
    for _, value in sorted(path_counts.iteritems(), key=lambda (k,v): (v["64-ecmp"],k)):
        ecmp_64_distinct_paths_counts.append(value["64-ecmp"])

#       print ksp_distinct_paths_counts
#       print ecmp_8_distinct_paths_counts
#       print ecmp_64_distinct_paths_counts
    x = range(len(ksp_distinct_paths_counts))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, ksp_distinct_paths_counts, color='b', label="8 Shortest Paths")
    ax1.plot(x, ecmp_64_distinct_paths_counts, color='r', label="64-way ECMP")
    ax1.plot(x, ecmp_8_distinct_paths_counts, color='g', label="8-way ECMP")
    plt.legend(loc="upper left");
    ax1.set_xlabel("Rank of Link")
    ax1.set_ylabel("# of Distinct Paths Link is on")
    plt.savefig("plots/%s_plot.png" % file_name)
        
def save_obj(obj, name):
    with open('pickled_routes/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('pickled_routes/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

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

# global miswirings
#m = percent of miswirings
def global_miswire(n,d,m):
    graph = networkx.random_regular_graph(d, n)
    # convert to int
    m = math.floor(n*m)
    for i in range(0,m):
        source = 0
        destination = 0
        while source != destination:
            source = random.randint(0, n)
            destination = random.randint(0, n)
        graph.remove_edge(source, destination)
    for i in range(0,m):
        source = 0
        destination = 0
        while source != destination:
            source = random.randint(0, n)
            destination = random.randint(0, n)
        graph.add_edge(source, destination)
    return graph

#cluster miswirings
#m = percent of miswirings
def clustered_miswire(n,d,m):
    graph = networkx.random_regular_graph(d, n)
    # convert to int
    m = math.floor(n*m)
    for i in range(0,m):
        source = random.randint(0, n)
        neighbors_iter = networkx.all_neighbors(graph,source)
        neighbors_list = []
        for n in neighbors_iter:
            neighbors_list += [n]
        # pick a random node from list of neighbors
        miswire = neighbors_list[random.randint(0, len(neighbors_list))]
        neighbors_list.remove(miswire)
        # pick another random node form list without miswire node
        rewire = neighbors_list[random.randint(0, len(neighbors_list))]
        graph.remove_edge(source, miswire)
        graph.add_edge(source,rewire)
    return graph

# local miswirings
# r = size of local subgraph
# m = percent of miswirings -> as a function of r/relative to r)
def local_miswire(n,d,r,m):
    graph = networkx.random_regular_graph(d, n)
    range_start = random.randint(0, n)
    node_list = list(G.nodes)
    # convert percent into int
    m = math.floor(r*m)
    local_list = []
    # if the endpoiint of the range is larger than the length of the list
    if range_start + r >= len(node_list):
        # break into two pieces and combine to form the complete subgraph
        local_list = node_list[range_start:len(node_list)]
        local_list += node_list[0:(range_start + r) - len(node_list)]
    # normal within bounds range
    else:
        local_list = node_list[range_start:(range_start + m)]
    local_graph = graph.subgraph(local_list)
    size_local = len(local_list)

    #copy pasta from global miswirings
    for i in range(0,m):
        source = 0
        destination = 0
        while source != destination:
            source = random.randint(0, size_local)
            destination = random.randint(0, size_local)
        local_graph.remove_edge(source, destination)
    for i in range(0,m):
        source = 0
        destination = 0
        while source != destination:
            source = random.randint(0, size_local)
            destination = random.randint(0, size_local)
        local_graph.add_edge(source, destination)
    return local_graph

# script ex -> build_topology.py n(int) d(int) type(string) m (float ~ decimal)

def main():
    n = sys.argv[1]
    numHosts = 3*n
    d = sys.argv[2]
    type = sys.argv[3]
    # percent miswirings in decimal form
    m = sys.argv[4]
    reuse_old_result = False
    ecmp_paths = {}
    all_ksp = {}
    file_name = "rrg_%s_%s" % (d, n)
    if not reuse_old_result:
        graph = networkx.empty_graph()
        if type.compare("local") == 0:
            # constant ~ possible number of miswirings in a local setting
            size_subgraph = 10
            graph = local_miswire(n, d, size_subgraph, m)
        elif type.compare("global") == 0:
            graph = global_miswire(n, d, m)
        elif type.compare("cluster") == 0:
            graph = clustered_miswire(n, d, m)
        else:
            print("invalid type")
            return
        networkx.write_adjlist(graph, file_name)
        graph = networkx.read_adjlist(file_name)

        print "Computing ECMP paths"
        ecmp_paths = compute_ecmp_paths(graph, n)
        save_obj(ecmp_paths, "ecmp_%s" % (file_name))
        print "Computing K shortest paths"
        all_ksp = compute_k_shortest_paths(graph, n)
        save_obj(all_ksp, "ksp_%s" % (file_name))
    else:
        graph = networkx.read_adjlist(file_name)

        ecmp_paths = load_obj("ecmp_%s" % (file_name))
        all_ksp = load_obj("ksp_%s" % (file_name))
    print "Assembling counts from paths"

    derangement = random_derangement(numHosts)
    all_links = graph.edges()
    path_counts = get_path_counts(ecmp_paths, all_ksp, derangement, all_links)
    print "Making the plot"
    assemble_histogram(path_counts=path_counts, file_name=file_name)
    
    print "Transforming routes for Ripl/Riplpox use"
    print "Transforming KSP"
    transformed_ksp_routes = transform_paths_dpid("ksp_%s" % (file_name), n, 8)
    save_routing_table(transformed_ksp_routes, "ksp_%s" % (file_name))
    print "Transforming ECMP 8"
    transformed_ecmp_routes = transform_paths_dpid("ecmp_%s" % (file_name), n, 8)
    save_routing_table(transformed_ecmp_routes, "ecmp_8_%s" % (file_name))
    
if __name__ == "__main__":
    main()
