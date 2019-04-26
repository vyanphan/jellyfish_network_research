#!/bin/sh

miswire_percentages=(
	"0.01"
	"0.05"
	"0.1"
)
miswire_percent_strings=(
	"01"
	"05"
	"1"
)
formats=(
	"local"
	"global"
	"cluster_local"
	"cluster_global"
)

for i in "${formats[@]}"; do
	for j in "${miswire_percentages[@]}"; do
    	python build_topology.py 100 15 $i $j
	done
done

for i in "${formats[@]}"; do
	for j in "${miswire_percent_strings[@]}"; do
		python tcp_test.py adjlist_files/rrg_15_100_$j\_$i 100 15 8 mn_script_ecmp_8_$i$j\_15-100_results > flow_scripts/mn_script_ecmp_8_$i$j\_15-100_flow
	done
done
