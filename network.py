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

# A network is simply a list of nodes/agents, each with a specified state
# Since the network is fully connected, we do not have to store the edges between the
# nodes, we can simply select any node when looking for neighbours as all nodes
# neighbour each other
class PopulationNetwork:
	def __init__(self, number_of_nodes, number_of_states, protocol, state_config = None, max_rounds = None):
		# The network graph, list of agents

		if number_of_states > number_of_nodes:
			raise ValueError("Number of states must be less than number of nodes.")

		# Create states


		# Node configuration is the state of every single node, each element is the state 
		# and the index gives which node is in that state initially
		self.graph = []
		node_configuration = []
		if state_config is None:
			# No configuration given, choose a random state for each agent
			states = range(0, number_of_states)
			node_configuration.extend([random.choice(states) for j in range(number_of_nodes)])
		else:
			if sum(state_config) != number_of_nodes:
				raise ValueError(f"The number of nodes in the state configuration ({sum(state_config)}) does not much the number of nodes provided ({number_of_nodes})")

			if len(state_config) != number_of_states:
				raise ValueError(f"The number of states in the state configuration ({len(state_config)}) does not much the number of states provided ({number_of_states})")

			# Use the given configuration to generate the node states
			for state in range(len(state_config)):
				node_configuration.extend([state for x in range(state_config[state])])
			
		# Create representation of agents, store dictionary pair
		# associating each node with a type of agent
		# Use the state configuration, if one is given to initialise the agents

		for i in range(len(node_configuration)):
			self.graph.append(HonestAgent(node_configuration[i]))

		# print(collections.Counter([agent.state for agent in self.graph]))
		self.protocol = protocol
		self.logger = DataLogger()
		self.round = 0
		self.log_graph()

	def has_converged(self):
		return self.protocol.is_converged([n.state for n in self.graph])

	def get_states(self):
		# Returns a list of all states in this graph
		# print(collections.Counter([agent.state for agent in self.graph]))
		# input()
		return [agent.state for agent in self.graph]

	def log_graph(self):
		self.logger.log_graph(self.round, self.get_states())
		self.round += 1

	def run_round(self):
		# This runs the protocol using synchronous interactions, i.e all nodes are updated
		# (seemingly) simultaneously
		if (self.has_converged()):
			print("Network has converged in " + str(self.round) + " rounds")
			exit()
			return
		
		# Should copy the agents states
		# print("Graph:")
		# print(self.graph)
		self.graph_copy = [agent.state for agent in self.graph]
		
		# For every node, run the protocol
		for agent in range(len(self.graph)):
			# agent is the index
			# Calculate new state based on neighbours (using copy of agents)
			 
			# Agents state
			agent_state = self.graph_copy[agent]

			# Neighbouring states, all nodes that dont have the index as this current node
			# use different methods based on number of nodes, as node size increases
			# random sampling is better than copying list
			if len(self.graph) < 100:
				# Create copy of list
				neighbour_states = [self.graph_copy[a] for a in range(len(self.graph_copy)) if a != agent]

				# Run protocol to find new state
				new_state = self.protocol.run(agent_state, neighbour_states)
			else:
				agent_copy = self.graph_copy.pop(agent)
				neighbour_states = self.graph_copy

				# Run protocol to find new state
				new_state = self.protocol.run(agent_state, neighbour_states)

				# Insert back into the list
				self.graph_copy.insert(agent, agent_copy)


			# Update this node using agent
			self.graph[agent].update_state(new_state)

		# print("Run round " + str(self.round))
		# print(self.get_states())
		# print([abg.state for abg in self.graph])
		# print(collections.Counter([agent.state for agent in self.graph]))
		# Log the new state of the network
		self.log_graph()

	def get_number_of_nodes(self):
		return len(self.graph)

	def get_agents(self):
		return self.agents.values()
		
	def get_graph(self):
		return self.graph