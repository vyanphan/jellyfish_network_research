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


def generate_jellyfish(n, d):
    graph = networkx.random_regular_graph(d, n)
    # a list that represents a node and the number of empty ports a node has left.
    nodes = [[node, graph.edges(node)] for node in graph.nodes]
    # all ports already used
    for x in range(0, len(nodes)):
        if nodes[x][1] == d:
            nodes.pop(x)

    # while nodes list is not empty
    while len(nodes) > 0:
        src = random.randint(0, len(nodes) - 1)
        dst = random.randint(0, len(nodes) - 1)

        while dst == src or graph.has_edge(nodes[src][0], nodes[dst][0]):
            dst = random.randint(0, len(nodes) - 1)

        graph.add_edge(nodes[src][0], nodes[dst][0])
        # update ports left
        nodes[src][1] = graph.edges(nodes[src][0])
        nodes[dst][1] = graph.edges(nodes[dst][0])
        if len(nodes[src][1]) == d:
            nodes.pop(src)
        if len(nodes[dst][1]) == d:
            nodes.pop(dst)

    return graph
    # should be completely connected


# global miswirings
#m = percent of miswirings
def global_miswire(n,d,m):
    graph = generate_jellyfish(n,d)
    # convert to int
    edges = [e for e in graph.edges]
    new_m = int(math.floor(len(edges)*m))
    for i in range(0,new_m):
        edges = [e for e in graph.edges]
        # new_m = int(math.floor(len(edges)*m))
        # pick random edge

        random_edge_1 = edges[random.randint(0, len(edges)-1)]
        src_1 = random_edge_1[0]
        dest_1 = random_edge_1[1]
        graph.remove_edge(src_1, dest_1)

        edges = [e for e in graph.edges]

        random_edge_2 = edges[random.randint(0, len(edges) - 1)]
        src_2 = random_edge_2[0]
        dest_2 = random_edge_2[1]

        # prevent self links
        if dest_2 != src_1 or dest_1 != src_2:
            graph.add_edge(src_1, dest_1)
            continue
        # swap random edge with another random edge.

        graph.remove_edge(src_2, dest_2)
        graph.add_edge(src_1, dest_2)
        graph.add_edge(src_2, dest_1)
    return graph

# local miswirings
# m = percent of miswirings
def local_miswire(n,d,m):
    graph = generate_jellyfish(n,d)
    edges = [e for e in graph.edges]
    # convert to int
    new_m = int(math.floor(len(edges)*m))
    for i in range(0, new_m):
        edges = [e for e in graph.edges]
        # pick a random edge in graph
        random_edge = edges[random.randint(0, len(edges)-1)]
        source = random_edge[0]
        dest = random_edge[1]
        # Get iterator of neighbors of destination node
        neighbors_list = list(networkx.all_neighbors(graph, dest))
        x = random.randint(0, len(neighbors_list)-1)
        rewire = neighbors_list[x]
        rewire_edges = graph.edges(rewire)
        rewire_edge = rewire_edges[random.randint(0, len(rewire_edges)-1)]
        if rewire_edge[0] == rewire:
            rewire_dst = rewire_edge[1]
        else:
            rewire_dst = rewire_edge[0]
        # swap
        # should never have parellel edges
        graph.remove_edge(source, dest)
        graph.add_edge(source,rewire)
        graph.remove_edge(rewire, rewire_dst)
        graph.add_edge(rewire_dst, dest)
    return graph

# cluster miswiring
# r = size of local subgraph
# m = percent of miswirings -> as a function of r/relative to r)
def clustered_global_miswire(n,d,r,m):
    graph = generate_jellyfish(n,d)
    edges = [e for e in graph.edges]
    range_start = random.randint(0, n)
    node_list = list(graph.nodes)
    # if the endpoint of the range is larger than the length of the list
    if range_start + r >= len(node_list):
        # break into two pieces and combine to form the complete subgraph
        local_list = node_list[range_start:len(node_list)]
        local_list += node_list[0:(range_start + r) - len(node_list)]
    # normal within bounds range
    else:
        # try to get range of nodes from G that is from range start -> range start + r
        local_list = node_list[range_start:(range_start + r)]
    # convert percent into int
    new_m = int(math.floor(len(edges)* m))
    #copy pasta from global miswirings
    for i in range(0,new_m):
        # finds a random edge that contains a node in the local list
        edges = [e for e in graph.edges]
        source = -1
        dest = -1
        while source not in local_list and dest not in local_list:
            random_edge = edges[random.randint(0, len(edges)-1)]
            source = random_edge[0]
            dest = random_edge[1]

        graph.remove_edge(source, dest)

        edges = [e for e in graph.edges]

        # random node from local list cluster
        # add an edge going from this node to a random node in Gsource = local_list[random.randint(0, len(local_list))]
        source_2 = local_list[random.randint(0, len(local_list)-1)]
        destination_2 = random.randint(0, len(node_list) - 1)

        if destination_2 != source or dest != source_2:
            graph.add_edge(source, dest)
            continue

        # perform swap.
        graph.remove_edge(source_2, destination_2)
        graph.add_edge(source, destination_2)
        graph.add_edge(source_2, dest)
    return graph

# cluster miswiring
# r = size of local subgraph
# m = percent of miswirings -> as a function of r/relative to r)
def clustered_local_miswire(n,d,r,m):
    graph = generate_jellyfish(n,d)
    edges = [e for e in graph.edges]
    range_start = random.randint(0, n)
    node_list = list(graph.nodes)
    # if the endpoint of the range is larger than the length of the list
    if range_start + r >= len(node_list):
        # break into two pieces and combine to form the complete subgraph
        local_list = node_list[range_start:len(node_list)]
        local_list += node_list[0:(range_start + r) - len(node_list)]
    # normal within bounds range
    else:
        # try to get range of nodes from G that is from range start -> range start + r
        local_list = node_list[range_start:(range_start + r)]
    # convert percent into int
    new_m = int(math.floor(len(edges)* m))
    #copy pasta from local miswirings
    for i in range(0,new_m):
        edges = [e for e in graph.edges]
        source = -1
        dest = -1
        # finds a random edge that contains a node in the local list
        while source not in local_list and dest not in local_list:
            random_edge = edges[random.randint(0, len(edges)-1)]
            source = random_edge[0]
            dest = random_edge[1]
        neighbors_iter = networkx.all_neighbors(graph, dest)
        neighbors_list = []
        for n in neighbors_iter:
            neighbors_list += [n]
        # pick random node from neighbor list as miswired node
        rewire = neighbors_list[random.randint(0, len(neighbors_list) - 1)]

        rewire_edges = graph.edges(rewire)
        rewire_edge = rewire_edges[random.randint(0, len(rewire_edges) - 1)]
        if rewire_edge[0] == rewire:
            rewire_dst = rewire_edge[1]
        else:
            rewire_dst = rewire_edge[0]
        # swap
        # should never have parellel edges
        graph.remove_edge(source, dest)
        graph.add_edge(source, rewire)
        graph.remove_edge(rewire, rewire_dst)
        graph.add_edge(rewire_dst, dest)

    return graph

def make_fattree(graph, start_num):
    # 4 nodes in a core
    core = [i for i in range(start_num, start_num + 4)]
    start_num += 4
    # 8 in agg1
    agg1 = [i for i in range(start_num, start_num + 8)]
    start_num += 8
    # 8 more in agg2
    agg2 = [i for i in range(start_num,start_num + 8)]
    start_num += 8
    # 16 in edge
    edge = [i for i in range(start_num, start_num + 16)]
    start_num += 16
    graph.add_nodes_from(core)
    graph.add_nodes_from(agg1)
    graph.add_nodes_from(agg2)
    graph.add_nodes_from(edge)
    for i in range(len(agg1)):
        if i % 2:       # i is odd
            graph.add_edge(agg1[i], core[2])
            graph.add_edge(agg1[i], core[3])
        else:
            graph.add_edge(agg1[i], core[0])
            graph.add_edge(agg1[i], core[1])

    for i in range(0, len(agg1), 2):
        graph.add_edge(agg1[i]  , agg2[i]  )
        graph.add_edge(agg1[i]  , agg2[i+1])
        graph.add_edge(agg1[i+1], agg2[i]  )
        graph.add_edge(agg1[i+1], agg2[i+1])

    for i in range(len(agg2)):
        graph.add_edge(agg2[i], edge[2*i])
        graph.add_edge(agg2[i], edge[2*i + 1])
    return core

def datacenter():
    graph = networkx.Graph()
    start_num = 0
    cores = []
    ports_p_pod = 20
    while start_num < 1000:
        cores += [make_fattree(graph,start_num)]
        start_num += 3
    # connect the cores using jellyfish
    aval_ports_p_core = [ports_p_pod for i in range(len(cores))]
    # while there is still more than 1 pod left
    while not len(aval_ports_p_core) <= 1:
        # pick random pods
        src_pod = random.randint(0,len(cores))
        dst_pod = random.randint(0,len(cores))
        while dst_pod == src_pod:
            dst_pod = random.randint(0, len(cores))
        # if no more ports left for that pod
        if not aval_ports_p_core[src_pod]:
            cores.remove(src_pod)
            aval_ports_p_core.remove(src_pod)
        elif not aval_ports_p_core[dst_pod]:
            cores.remove(dst_pod)
            aval_ports_p_core.remove(dst_pod)
        else :
            src_node = cores[src_pod][random.randint(0, len(cores[src_pod]))]
            dst_node = cores[dst_pod][random.randint(0, len(cores[dst_pod]))]
            while graph.has_edge(src_node,dst_node):
                dst_node = cores[dst_pod][random.randint(0,len(cores[dst_pod]))]
            aval_ports_p_core[src_pod] -= 1
            aval_ports_p_core[dst_pod] -= 1
            graph.add_edge(src_node,dst_node)
    return graph





# script ex -> build_topology.py n(int) d(int) t(string) m(float ~ decimal)
# n - number of nodes
# d - degree per a node
# t - type of miswiring
# m - percent miswiring of total nodes

def main():
    n = int(sys.argv[1])
    numHosts = int(3*n)
    d = int(sys.argv[2])
    t = str(sys.argv[3])

    # percent miswirings in decimal form
    m = float(sys.argv[4])
    reuse_old_result = False
    ecmp_paths = {}
    all_ksp = {}
    file_name = "rrg_%s_%s_%s_" % (d, n, str(m)[2:])

    # constant ~ possible number of miswirings in a local setting
    size_subgraph = 10
    if not reuse_old_result:
        if t == "local":
            graph = local_miswire(n, d, m)
            file_name += "local"
        elif t == "global":
            graph = global_miswire(n, d, m)
            file_name += "global"
        elif t == "cluster_global":
            graph = clustered_global_miswire(n, d, size_subgraph, m)
            file_name += "cluster_global"
        elif t == "cluster_local":
            graph = clustered_local_miswire(n, d, size_subgraph, m)
            file_name += "cluster_local"
        elif t == "datacenter":
            graph = datacenter()
            file_name += "datacenter"
        else:
            graph = generate_jellyfish(n,d)
        networkx.write_adjlist(graph, "adjlist_files/"+file_name)
        graph = networkx.read_adjlist("adjlist_files/"+file_name)

        print("Computing ECMP paths")
        ecmp_paths = compute_ecmp_paths(graph, n)
        save_obj(ecmp_paths, "ecmp_%s" % (file_name))
        print("Computing K shortest paths")
        all_ksp = compute_k_shortest_paths(graph, n)
        save_obj(all_ksp, "ksp_%s" % (file_name))
    else:
        graph = networkx.read_adjlist(file_name)
        ecmp_paths = load_obj("ecmp_%s" % (file_name))
        all_ksp = load_obj("ksp_%s" % (file_name))
    print("Assembling counts from paths")

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
