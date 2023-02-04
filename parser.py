import argparse
from network import PopulationNetwork
from protocols.three_majority import ThreeMajority
import networkx as nx


# The parser for commandline arguments for the population protocols
# Options:
# -nogui : Boolean ; Disables the GUI for faster computation
# -r, -rounds : int ; The number of rounds to run (only enabled when using nogui)
# -n, -nodes  : int ; The number of nodes in the network
# -s, -states : int or list of ints ; The number of states in the network (< -n) or a list of how many nodes in each state initially
# 				(must add up to -n)
# -o, -output : string ; The output of the function, currently unknown options

def positive_number(val):
	if int(val) <= 0:
		raise argparse.ArgumentTypeError("Exepcted a positive integer greater than 0")

	return int(val)


def network_config(val):
	# Network configuration is given either as a number, or list of numbers (comma separeted)
	# Ensure all elements are numbers if using a list
	split_list = val.split(",")
	state_numbers = [e.isdigit() for e in split_list]

	if not all(state_numbers):
		raise argparse.ArgumentTypeError("Expected a number or list of comma-separated numbers")

	print("LOl")
	return [int(a) for a in split_list]


DEFAULT_NODE_COUNT = 10
DEFAULT_STATE_COUNT = 2
DEFAULT_ROUNDS_COUNT = 1
GUI_NODE_LIMIT = 100 # Maximum number of nodes allowed when using the GUI

# Dictionary of protocol name -> protocol
PROTOCOLS = {"threemajority": ThreeMajority}

parser = argparse.ArgumentParser(prog = 'Population Protocol Visualiser',
								description = 'Analyse and visualise population protocol networks')

parser.add_argument('-nogui', '--nogui', action = 'store_true', dest = 'nogui', help='Run the analyser without a GUI', default=True)
parser.add_argument('-r', '-rounds', dest = 'rounds', help = 'The number of rounds to run the protocol for', type = positive_number, default=DEFAULT_ROUNDS_COUNT)
parser.add_argument('-n', '-nodes', dest = 'nodes', help = 'The number of nodes in the network', type=positive_number, default=DEFAULT_NODE_COUNT)
parser.add_argument('-s', '-states', dest = 'states', help = 'The number of initial states, or a list of comma separated numbers indicating how many nodes in each state (must add up to n, the number of nodes)', type=network_config, default=[DEFAULT_STATE_COUNT])
parser.add_argument('-p', '-protocol', dest='protocol', help='The protocol to run until convergence', choices=PROTOCOLS.keys(), required=True)
# parser.add_argument('-o')
 
args = parser.parse_args()

if (len(args.states) > 1 and sum(args.states) != args.nodes):
	# If a state config is given, check the number of nodes in the configuration matches the nodes specified in the network
	raise argparse.ArgumentTypeError(f"The number of nodes specified ({args.nodes}) does not match the nodes in the state configuration ({sum(args.states)})")

# Check if GUI is used, if nogui is specified then this also allows the rounds

# Create the network specified by the number of nodes and the state configuration
protocol = PROTOCOLS.get(args.protocol)

network = PopulationNetwork(10, 2, ThreeMajority, [8, 2])
for i in range(100000000):
	network.run_round()
print("Done")
# if (args.)