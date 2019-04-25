#!/bin/sh

miswire_percentages=(
	"0.01"
	"0.05"
	"0.1"
)
formats=(
	"local"
	"global"
	"cluster_local"
	"cluster_global"
)
for i in "${formats[@]}"; do
	for j in "${miswire_percentages[@]}"; do
    	python build_topology.py 1000 20 $i $j
	done
done
