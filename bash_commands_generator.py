import os


pox = "pox/pox.py riplpox.riplpox --topo=jelly,{0},{1},{2} --routing=jelly,{3} --mode=reactive"
mnscript = "python tcp_tests.py > mn_script_ecmp_8_{0}{1}_{2}-{3}_flows"
mnrun = "sudo mn --custom ripl/ripl/mn.py --topo jelly,{0},{1},{2} --link tc --controller=remote --mac"
mnsource = "source mn_script_ecmp_8_{0}{1}_{2}-{3}_flows"


def make_command(nswitches, nports, topo, percent):
	adjlist = "rrg_{0}_{1}_{2}_{3}".format(nports, nswitches, percent, topo)
	routfile = "ecmp_8_rrg_{0}_{1}_{2}_{3}".format(nports, nswitches, percent, topo)

	with open("bash_commands.sh", "a") as file:
		file.write(pox.format(nswitches, nports, adjlist, routfile) + "\n")
		file.write(mnscript.format(topo, percent, nswitches, nports) + "\n")
		file.write(mnrun.format(nswitches, nports, adjlist) + "\n")
		file.write(mnsource.format(topo, percent, nswitches, nports) + "\n\n")

for i in ["local", "global", "cluster_local", "cluster_global"]:
	for j in ["01", "05", "10"]:
		make_command("10", "5", i, j)
