import argparse


# The parser for commandline arguments for the population protocols
# Options:
# -nogui : Boolean ; Disables the GUI for faster computation
# -r, -rounds : int ; The number of rounds to run (only enabled when using nogui)
# -n, -nodes  : int ; The number of nodes in the network
# -s, -states : int or list of ints ; The number of states in the network (< -n) or a list of how many nodes in each state initially
# 				(must add up to -n)
# -o, -output : string ; The output of the function, currently unknown options
# 