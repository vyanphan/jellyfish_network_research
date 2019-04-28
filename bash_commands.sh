# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_01_local --routing=jelly,ecmp_8_rrg_15_100_01_local --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_01_local --link tc --controller=remote --mac
# source mn_script_ecmp_8_local01_15-100_flow

pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_05_local --routing=jelly,ecmp_8_rrg_15_100_05_local --mode=reactive
sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_05_local --link tc --controller=remote --mac
source mn_script_ecmp_8_local05_15-100_flow

pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_1_local --routing=jelly,ecmp_8_rrg_15_100_1_local --mode=reactive
sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_1_local --link tc --controller=remote --mac
source mn_script_ecmp_8_local1_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_01_global --routing=jelly,ecmp_8_rrg_15_100_01_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_01_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_global01_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_05_global --routing=jelly,ecmp_8_rrg_15_100_05_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_05_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_global05_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_1_global --routing=jelly,ecmp_8_rrg_15_100_1_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_1_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_global1_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_01_cluster_local --routing=jelly,ecmp_8_rrg_15_100_01_cluster_local --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_01_cluster_local --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_local01_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_05_cluster_local --routing=jelly,ecmp_8_rrg_15_100_05_cluster_local --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_05_cluster_local --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_local05_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_1_cluster_local --routing=jelly,ecmp_8_rrg_15_100_1_cluster_local --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_1_cluster_local --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_local1_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_01_cluster_global --routing=jelly,ecmp_8_rrg_15_100_01_cluster_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_01_cluster_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_global01_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_05_cluster_global --routing=jelly,ecmp_8_rrg_15_100_05_cluster_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_05_cluster_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_global05_15-100_flow

# pox/pox.py riplpox.riplpox --topo=jelly,100,15,adjlist_files/rrg_15_100_1_cluster_global --routing=jelly,ecmp_8_rrg_15_100_1_cluster_global --mode=reactive
# sudo mn --custom ripl/ripl/mn.py --topo jelly,100,15,adjlist_files/rrg_15_100_1_cluster_global --link tc --controller=remote --mac
# source mn_script_ecmp_8_cluster_global1_15-100_flow

