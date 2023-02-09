import argparse
from network import PopulationNetwork
from protocols.protocol import PopulationProtocol
from protocols.three_majority import ThreeMajority
import networkx as nx
from gui import SimulationGUI
import matplotlib.pyplot as plt


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

	return [int(a) for a in split_list]

subs = PopulationProtocol.__subclasses__()
for i in range(len(subs)):
	cl = subs[i]
	print(cl.get_protocol_name())

DEFAULT_NODE_COUNT = 10
DEFAULT_STATE_COUNT = 2
DEFAULT_ROUNDS_COUNT = 1
GUI_NODE_LIMIT = 50 # Maximum number of nodes allowed when using the GUI

# Dictionary of protocol name -> protocol
PROTOCOLS = {protocol_class.get_protocol_name(): protocol_class for protocol_class in PopulationProtocol.__subclasses__()}

parser = argparse.ArgumentParser(prog = 'Population Protocol Visualiser',
								description = 'Analyse and visualise population protocol networks')

parser.add_argument('-nogui', '--nogui', action = 'store_true', dest = 'nogui', help='Run the analyser without a GUI', default=False)
parser.add_argument('-r', '-rounds', dest = 'rounds', help = 'The number of rounds to run the protocol for, only valid when used with -nogui', type = positive_number, default=DEFAULT_ROUNDS_COUNT)
parser.add_argument('-n', '-nodes', dest = 'nodes', help = 'The number of nodes in the network', type=positive_number, default=DEFAULT_NODE_COUNT)
parser.add_argument('-s', '-states', dest = 'states', help = 'The number of initial states, or a list of comma separated numbers indicating how many nodes in each state (must add up to n, the number of nodes)', type=network_config, default=[DEFAULT_STATE_COUNT])
parser.add_argument('-p', '-protocol', dest='protocol', help='The protocol to run this network with', choices=PROTOCOLS.keys(), required=True)
# parser.add_argument('-o', '-output', dest='output', help='The output type of the network')
# parser.add_argument('-o')

args = parser.parse_args()

if (len(args.states) > 1 and sum(args.states) != args.nodes):
	# If a state config is given, check the number of nodes in the configuration matches the nodes specified in the network
	raise argparse.ArgumentTypeError(f"The number of nodes specified ({args.nodes}) does not match the nodes in the state configuration ({sum(args.states)})")

# Check if GUI is used, if nogui is specified then this also allows the rounds

# Create the network specified by the number of nodes and the state configuration
protocol = PROTOCOLS.get(args.protocol)

if len(args.states) == 1:
	# Only 1 state provided, this means this is the given state
	if (args.states[0]) > args.nodes:
		raise argparse.ArgumentTypeError(f"The number of states must be less than or equal to the number of nodes ({args.nodes})")
	network_states = args.states[0]
	state_config = None
else:
	network_states = len(args.states)
	state_config = args.states

network = PopulationNetwork(args.nodes, network_states, protocol, state_config)


if args.nogui:
	# pass
	for j in range(0, args.rounds):
		# print("Running with no gui..?")
		network = PopulationNetwork(args.nodes, network_states, protocol, state_config)
		while not network.has_converged():
			network.run_round()


	data = network.logger.data

	# X value will show the round number
	x = list(data.keys())

	# 0: [0, 1, 0]
	# 1: [1, 1, 0]
	# 2: [1, 1, 1]
	# Output:
	# [0, 1, 2]
	# [2, 1, 0]
	# [1, 2, 3]

	# Y values for each state
	# Initial state of the network is stored in round 0
	initial_states = list(set(data.get(0, [])))

	for state in initial_states:
		y = []
		for rnd in data.keys():
			count = data.get(rnd).count(state)
			y.append(count)

		plt.plot(x, y)

	# y1 = ['1000', '13k', '26k', '42k', '60k', '81k']
	# y2 = ['1000', '13k', '27k', '43k', '63k', '85k']

	# plt.plot(x, y1)
	# plt.plot(x, y2, '-.')

	plt.xlabel("Round number")
	plt.ylabel("Node count")
	plt.title('States in network')
	plt.show()

else:
	if (args.rounds > 1):
		parser.error("Multiple rounds may only be run without the GUI (use -nogui)")

	if args.nodes > GUI_NODE_LIMIT:
		parser.error(f"Only networks up to and including {GUI_NODE_LIMIT} nodes may be created with the GUI (use -nogui)")
	SimulationGUI(network)


print("Done")
# if (args.)