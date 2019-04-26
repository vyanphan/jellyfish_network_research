pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_01_local --routing=jelly,ecmp_8_rrg_5_10_01_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_local01_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_01_local --link tc --controller=remote --mac
source mn_script_ecmp_8_local01_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_05_local --routing=jelly,ecmp_8_rrg_5_10_05_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_local05_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_05_local --link tc --controller=remote --mac
source mn_script_ecmp_8_local05_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_10_local --routing=jelly,ecmp_8_rrg_5_10_10_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_local10_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_10_local --link tc --controller=remote --mac
source mn_script_ecmp_8_local10_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_01_global --routing=jelly,ecmp_8_rrg_5_10_01_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_global01_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_01_global --link tc --controller=remote --mac
source mn_script_ecmp_8_global01_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_05_global --routing=jelly,ecmp_8_rrg_5_10_05_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_global05_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_05_global --link tc --controller=remote --mac
source mn_script_ecmp_8_global05_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_10_global --routing=jelly,ecmp_8_rrg_5_10_10_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_global10_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_10_global --link tc --controller=remote --mac
source mn_script_ecmp_8_global10_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_01_cluster_local --routing=jelly,ecmp_8_rrg_5_10_01_cluster_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_local01_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_01_cluster_local --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_local01_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_05_cluster_local --routing=jelly,ecmp_8_rrg_5_10_05_cluster_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_local05_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_05_cluster_local --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_local05_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_10_cluster_local --routing=jelly,ecmp_8_rrg_5_10_10_cluster_local --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_local10_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_10_cluster_local --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_local10_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_01_cluster_global --routing=jelly,ecmp_8_rrg_5_10_01_cluster_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_global01_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_01_cluster_global --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_global01_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_05_cluster_global --routing=jelly,ecmp_8_rrg_5_10_05_cluster_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_global05_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_05_cluster_global --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_global05_10-5_flows

pox/pox.py riplpox.riplpox --topo=jelly,10,5,rrg_5_10_10_cluster_global --routing=jelly,ecmp_8_rrg_5_10_10_cluster_global --mode=reactive
python tcp_tests.py > mn_script_ecmp_8_cluster_global10_10-5_flows
sudo mn --custom ripl/ripl/mn.py --topo jelly,10,5,rrg_5_10_10_cluster_global --link tc --controller=remote --mac
source mn_script_ecmp_8_cluster_global10_10-5_flows

