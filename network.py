# This file contains an abstraction of the network and provides a GUI
# to access components of the networks, such as the agents, opinions etc.

import random
from agents import HonestAgent


# A network is simply a list of nodes/agents, each with a specified state
# Since the network is fully connected, we do not have to store the edges between the
# nodes, we can simply select any other node when looking for neighbours as all nodes
# neighbour each other
class PopulationNetwork:
	def __init__(self, number_of_nodes, number_of_states, protocol, state_config=None, max_rounds=None):
		# The network graph, list of agents
		self.graph = []

		# A dictionary of the states of this network in each round
		# The key is the round number (0 = initial state) and the value is the list of states
		# of the network in this round
		self.data = {}

		if number_of_states > number_of_nodes:
			raise ValueError("Number of states must be less than or equal to number of nodes.")

		self.max_rounds = max_rounds

		# Node configuration is the state of every single node, each element is the state 
		# and the index gives which node is in that state initially
		node_configuration = []
		if state_config is None:
			# No configuration given, choose a random state for each agent
			states = range(0, number_of_states)
			node_configuration.extend([random.choice(states) for j in range(number_of_nodes)])
		else:
			# A configuration was given, validate it to ensure configuration matches number of states
			if sum(state_config) != number_of_nodes:
				raise ValueError(f"The number of nodes in the state configuration ({sum(state_config)}) does not much the number of nodes provided ({number_of_nodes})")

			if len(state_config) != number_of_states:
				raise ValueError(f"The number of states in the state configuration ({len(state_config)}) does not much the number of states provided ({number_of_states})")

			# Use the given configuration to generate the node states
			for state in range(len(state_config)):
				node_configuration.extend([state for _ in range(state_config[state])])
			
		# Create representation of agents
		# Use the state configuration, if one is given to initialise the agents
		for i in range(len(node_configuration)):
			self.graph.append(HonestAgent(node_configuration[i]))

		self.protocol = protocol
		self.round = 0
		self.log_graph()

	def has_converged(self):
		return self.protocol.is_converged(self.get_states())

	def get_states(self):
		# Returns a list of all states in this graph
		return [agent.state for agent in self.graph]

	def log_graph(self):
		# Add the current configuration and increase round number
		self.data[self.round] = self.get_states()
		self.round += 1

	def has_finished(self):
		# Check if either the network has either converged
		# or the maximum round has been reached
		return (self.max_rounds is not None and self.round > self.max_rounds) or self.has_converged()

	def run_round(self):
		# This runs the protocol using synchronous interactions, i.e all nodes are updated
		# (seemingly) simultaneously
		# self.round holds the round that is currently about to run
		if self.max_rounds is not None and self.round > self.max_rounds:
			return

		if self.has_converged():
			return
		
		# Should copy the agents states
		graph_copy = [agent.state for agent in self.graph]
		
		# For every node, run the protocol
		for agent in range(len(self.graph)):
			# agent is the index of the agent
			# Calculate new state based on neighbours (using copy of graph)
			 
			# Agents state
			agent_state = graph_copy[agent]

			# Neighbouring states, all nodes that don't have the index as this current node
			# We remove this current node from the graph temporarily, then sample from the remaining list
			# Once it has been sampled, the node is then inserted back into the graph
			agent_copy = graph_copy.pop(agent)
			neighbour_states = graph_copy

			# Run protocol to find new state
			new_state = self.protocol.run(agent_state, neighbour_states)

			# Insert back into the list
			graph_copy.insert(agent, agent_copy)

			# Update this node using agent update method
			self.graph[agent].update_state(new_state)

		# Log the new state of the network
		self.log_graph()

	def get_number_of_nodes(self):
		# Number of nodes in the graph
		return len(self.graph)
		
	def get_graph(self):
		return self.graph
