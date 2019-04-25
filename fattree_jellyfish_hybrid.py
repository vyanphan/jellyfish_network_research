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

# https://image.slidesharecdn.com/fataugust13-130922092035-phpapp01/95/fattree-a-scalable-commodity-data-center-network-architecture-23-638.jpg?cb=1379842614

def make_fattree():
	core = [Node() for i in range(4)]
	agg1 = [Node() for i in range(8)]
	agg2 = [Node() for i in range(8)]
	edge = [Node() for i in range(16)]

	for i in range(len(agg1)):
		if i % 2:		# i is odd
			add_edge(agg1[i], core[2])
			add_edge(agg1[i], core[3])
		else:
			add_edge(agg1[i], core[0])
			add_edge(agg1[i], core[1])

	for i in range(0, len(agg1), 2):
		add_edge(agg1[i]  , agg2[i]  )
		add_edge(agg1[i]  , agg2[i+1])
		add_edge(agg1[i+1], agg2[i]  )
		add_edge(agg1[i+1], agg2[i+1])

	for i in range(len(agg2)):
		add_edge(agg2[i], edge[2*i])
		add_edge(agg2[i], edge[2*i + 1])

	return core


root_list = []
NUM_DATACENTERS = 1000
for i in range(NUM_DATACENTERS):
	root_list += make_fattree()


jellyfish(root_list)


