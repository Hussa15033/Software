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

class PopulationNetwork:
	def __init__(self, number_of_nodes, number_of_states, protocol):
		# The network graph
		self.graph = nx.complete_graph(number_of_nodes)

		if number_of_states > number_of_nodes:
			raise ValueError("Number of states must be less than number of nodes.")

		# Create states
		states = range(0, number_of_states)

		self.state_colours = {}

		# Create representation of agents, store dictionary pair
		# associating each node with a type of agent
		self.agents = {}
		for g in self.graph.nodes():
			self.agents[g] = HonestAgent(random.choice(states))

		self.protocol = protocol

	def has_converged(self):
		return self.protocol.is_converged([n.state for n in self.agents.values()])

	def get_states_in_graph(self):
		# Returns a list of all states in this graph
		return [agent.state for agent in self.agents.values()]
		
	def run_round(self):
		if (self.has_converged()):
			return
		
		# Should copy the agents states
		self.agents_states_copy = self.agents.copy()

		# For every node, run the protocol
		for node in self.graph.nodes():
			# node is the index
			# Calculate new state based on neighbours (using copy of agents)
			 
			# Agents state
			agent_state = self.agents_states_copy[node]

			# Neighbouring states
			neighbouring_nodes = self.graph.neighbors(node)
			neighbour_states = [self.agents_states_copy[n] for n in neighbouring_nodes]

			# Run protocol to find new state
			new_state = self.protocol.run(agent_state, neighbour_states)

			# Update this node using agent
			self.agents[node].update_state(new_state)



	def show_graph(self):
		color_map = list(map(lambda agent: self.state_colours.get(agent.state), self.agents.values()))
		pos = nx.spring_layout(self.graph, seed = 1)
		nx.draw(self.graph, pos = pos, node_color = color_map)

	def update_graph(self):
		# f = plt.figure(figsize=(10, 5), dpi=100)
		# a = f.add_subplot(111)
		color_map = list(map(lambda agent: self.state_colours.get(agent.state), self.agents.values()))
		pos = nx.spring_layout(self.graph, seed = 1)
		# plt.pause(1)
		plt.clf()
		nx.draw(self.graph, pos = pos, node_color = color_map)	
		# plt.show()
		return plt.figure(figsize=(10, 5), dpi = 100)
pop = Simulation(10, 2, ThreeMajority)