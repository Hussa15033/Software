# This file contains an abstraction of the network and provides a GUI
# to access components of the networks, such as the agents, opinions etc.

import random
import collections
import agents
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np
# from protocols import ThreeMajority, ThreeMajorityConverged
from protocols.three_majority import ThreeMajority
# import pylab as py
# from agents.honest_agent import HonestAgent
# 
from agents.honest_agent import HonestAgent
import networkx as nx
from datalogger import DataLogger

class PopulationNetwork:
	def __init__(self, number_of_nodes, number_of_states, protocol, state_config = None):
		# The network graph
		self.graph = nx.complete_graph(number_of_nodes)

		if number_of_states > number_of_nodes:
			raise ValueError("Number of states must be less than number of nodes.")

		# Create states

		self.state_colours = {}

		# Node configuration is the state of every single node, each element is the state 
		# and the index gives which node is in that state initially
		node_configuration = []
		if state_config is None:
			# No configuration given, choose a random state
			states = range(0, number_of_states)
			node_configuration = [random.choice(states) for j in range(len(self.graph.nodes()))]
		else:
			# Use the given configuration to generate the node states
			for state in range(len(state_config)):
				node_configuration.extend([state for x in range(state_config[state])])
			
		# Create representation of agents, store dictionary pair
		# associating each node with a type of agent
		# Use the state configuration, if one is given to initialise the agents

		self.agents = {}
		for i in range(len(self.graph.nodes())):
			self.agents[i] = HonestAgent(node_configuration[i])

		self.protocol = protocol
		self.logger = DataLogger()
		self.round = 0
		self.log_graph()

	def has_converged(self):
		return self.protocol.is_converged([n.state for n in self.agents.values()])

	def get_states(self):
		# Returns a list of all states in this graph
		# print(collections.Counter([agent.state for agent in self.agents.values()]))
		# input()
		return [agent.state for agent in self.agents.values()]

	def log_graph(self):
		self.logger.log_graph(self.round, self.get_states())
		self.round += 1

	def run_round(self):
		if (self.has_converged()):
			return
		
		# Should copy the agents states
		self.agents_copy = self.agents.copy()

		# For every node, run the protocol
		for node in self.graph.nodes():
			# node is the index
			# Calculate new state based on neighbours (using copy of agents)
			 
			# Agents state
			agent_state = self.agents_copy[node].state

			# Neighbouring states
			neighbouring_nodes = self.graph.neighbors(node)
			neighbour_states = [self.agents_copy[n].state for n in neighbouring_nodes]

			# Run protocol to find new state
			new_state = self.protocol.run(agent_state, neighbour_states)

			# Update this node using agent
			self.agents.get(node).update_state(new_state)

		# Log the new state of the network
		self.log_graph()

	def get_agents(self):
		return self.agents.values()
		
	def get_graph(self):
		return self.graph