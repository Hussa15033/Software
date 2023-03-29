import argparse
from network import PopulationNetwork
from protocols import PopulationProtocol, ThreeMajority, NMajorityProtocol
from gui import SimulationGUI
import matplotlib.pyplot as plt
from analysers import BasicAnalyser, BiasAnalyser, NMajorityAnalyser

# The parser for commandline arguments for the population protocols
# Options:
# -nogui : Boolean ; Disables the GUI for faster computation
# -r, -rounds : int ; The number of rounds to run (only enabled when using nogui)
# -n, -nodes  : int ; The number of nodes in the network
# -s, -states : int or list of ints ; The number of states in the network (< -n) or a list of how many nodes in each state initially
# 				(must add up to -n)
# -o, -output : string ; The output of the function, currently unknown options

# Constants
DEFAULT_NODE_COUNT = 10
DEFAULT_STATE_COUNT = 2
DEFAULT_ROUNDS_COUNT = 1

# Maximum number of nodes allowed when using the GUI
GUI_NODE_LIMIT = 50

# Dictionary of protocol name -> protocol
# todo: fix this!
CLI_PROTOCOLS = [ThreeMajority(), NMajorityProtocol(97)]
PROTOCOLS = {protocol.get_protocol_name(): protocol for protocol in CLI_PROTOCOLS}
# Different types of analysis that can be performed name -> callback
ANALYSERS = {
	"basic": BasicAnalyser,
	"bias": BiasAnalyser,
	"n-majority": NMajorityAnalyser
}


def positive_number(val):
	if int(val) <= 0:
		raise argparse.ArgumentTypeError("Expected a positive integer greater than 0")

	return int(val)


def network_config(val):
	# Network configuration is given either as a number, or list of numbers (comma separeted)
	# Ensure all elements are numbers if using a list
	split_list = val.split(",")
	state_numbers = [e.isdigit() for e in split_list]

	if not all(state_numbers):
		raise argparse.ArgumentTypeError("Expected a number or list of comma-separated numbers")

	return [int(a) for a in split_list]


parser = argparse.ArgumentParser(prog = 'Population Protocol Visualiser',
								description = 'Analyse and visualise population protocol networks',
								formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-nogui', '--nogui', action = 'store_true', dest = 'nogui', help='Run the analyser without a GUI', default=False)
parser.add_argument('-r', '-rounds', dest='rounds', help = 'The number of rounds to run the protocol for, only valid when used with -nogui', type = positive_number, default=DEFAULT_ROUNDS_COUNT)
parser.add_argument('-n', '-nodes', dest='nodes', help = 'The number of nodes in the network', type=positive_number, default=None)
parser.add_argument('-s', '-states', dest='states', help = 'The number of initial states, or a list of comma separated numbers indicating how many nodes in each state (must add up to n, the number of nodes)', type=network_config, default=None)
parser.add_argument('-p', '-protocol', dest='protocol', help='The protocol to run this network with', choices=PROTOCOLS.keys(), default=None)
parser.add_argument('-o', '-output', dest='output', help="\n".join(f"{name:<6}" + " : " + analyser.info() for name, analyser in ANALYSERS.items()), choices = ANALYSERS.keys(), default = "basic")

# Parser verifies arguments are correct for ALL analysers
# Each analyser then uses whatever arguments it requires from the parser

# Essentially, if the nogui command is used, we ignore ALL other stuff, the CLI is only useful for analysers
# so only allow analyses with these. Verify all arguments BEFORE the analyses, but no arguments should be
# required by the parser except the analyser, then the analyser will choose what arguments it wishes to accept
args = parser.parse_args()


# Network created is invalid to begin with.
network = None

# Validate all commands given by the user
if args.nodes is not None and args.protocol is not None:
	input("TEST")
	# if args.states is not None and len(args.states) > 1 and sum(args.states) != args.nodes:
		# If a state config is given, check the number of nodes in the configuration matches the nodes specified in the network
		# raise argparse.ArgumentTypeError(f"The number of nodes specified ({args.nodes}) does not match the nodes in the state configuration ({sum(args.states)})")

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


# Check if GUI is used, if nogui is specified then this also allows the rounds
# If a GUI is not selected, then the network created above must be valid
if args.nogui:
	if network is None:
		parser.error("Incorrect arguments passed. Use the help command for more information")
	# Using the CLI
	# Get the analyser that was selected
	analyser_type = ANALYSERS.get(args.output, None)
	if analyser_type is None:
		print("An unknown analyser was selected")

	analyser = analyser_type(args.nodes, network_states, state_config, protocol, args.rounds)
	analyser.analyse()
	plt.show()

else:
	# GUI is being used
	if args.rounds > 1:
		parser.error("Multiple rounds may only be run without the GUI (use -nogui)")

	if args.nodes is not None and args.nodes > GUI_NODE_LIMIT:
		parser.error(f"Only networks up to and including {GUI_NODE_LIMIT} nodes may be created with the GUI (use -nogui)")
	SimulationGUI(network)