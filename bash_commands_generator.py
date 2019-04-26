import os


pox = "pox/pox.py riplpox.riplpox --topo=jelly,{0},{1},{2} --routing=jelly,{3} --mode=reactive"
mnrun = "sudo mn --custom ripl/ripl/mn.py --topo jelly,{0},{1},{2} --link tc --controller=remote --mac"
mnsource = "source mn_script_ecmp_8_{0}{1}_{2}-{3}_flow"

def make_command(nswitches, nports, topo, percent):
	adjlist = "adjlist_files/rrg_{0}_{1}_{2}_{3}".format(nswitches, nports, percent, topo)
	routfile = "ecmp_8_rrg_{0}_{1}_{2}_{3}".format(nswitches, nports, percent, topo)
	with open("bash_commands.sh", "a") as file:
		file.write(pox.format(nports, nswitches, adjlist, routfile) + "\n")
		file.write(mnrun.format(nports, nswitches, adjlist) + "\n")
		file.write(mnsource.format(topo, percent, nswitches, nports) + "\n\n")

topos = ["local", "global", "cluster_local", "cluster_global"]
percs = ["01", "05", "10"]

for i in topos:
	for j in percs:
		make_command("15", "100", i, j)
