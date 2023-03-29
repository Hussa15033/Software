import math
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from network import PopulationNetwork
from protocols import NMajorityProtocol


class Analyser(ABC):
	def __init__(self, nodes, states, state_config, protocol, rounds):
		self.nodes = nodes
		self.states = states
		self.state_config = state_config
		self.protocol = protocol
		self.rounds = rounds

	@abstractmethod
	def analyse(self):
		pass

	# Override this method to display info about the analyser
	@staticmethod
	def info():
		return "An analyser for analysing population networks"


def basic_analysis(data, state_colours=None):
	# A basic analyser that takes a round of data logs and produces a
	# plot of each state in the network against the

	# X value will show the round number
	x = list(data.keys())

	initial_states = list(set(data.get(0, [])))

	f = plt.figure()
	for state in initial_states:
		y = []
		for rnd in data.keys():
			count = data.get(rnd).count(state)
			y.append(count)

		line, = plt.plot(x, y)
		plt.xticks(x)
		if state_colours is not None:
			line.set_color(state_colours.get(state, "#000"))

		if (len(initial_states) <= 5):
			line.set_label(f'State {state}')
			plt.legend()

	# y1 = ['1000', '13k', '26k', '42k', '60k', '81k']
	# y2 = ['1000', '13k', '27k', '43k', '63k', '85k']

	# plt.plot(x, y1)
	# plt.plot(x, y2, '-.')

	plt.xlabel("Round number")
	plt.ylabel("Node count")
	plt.title('States in network')
	f.show()


# A basic analyser that just runs 1 round, and outputs the
# states over time
class BasicAnalyser(Analyser):
	def analyse(self):
		if self.rounds > 1:
			print("The basic analyser can only be run using 1 round")
		network = PopulationNetwork(self.nodes, self.states, self.protocol, self.state_config)
		while not network.has_converged():
			network.run_round()

		print(f"Finished, network converged on round {network.round - 1}")
		basic_analysis(network.data)

	@staticmethod
	def info():
		return "A basic analyser showing the number of nodes in each state over each round"


# An analyser that slowly increases the bias and plots a graph of the frequencies over time
class BiasAnalyser(Analyser):
	def analyse(self):
		if self.rounds < 100:
			print("Warning: A high number of rounds is recommended for the bias analyser")

		if self.state_config is not None or self.states != 2:
			print("Error: A state configuration/number of states is unnecessary for the bias analyser")
			return

		if self.nodes < 4:
			print("Error: A minimum of 4 nodes is required for the bias anylyser")
			return

		# We have 2 states, and start with a bias of 0 or 1 (depending on if the number of nodes is 1 or 0)
		state_0_initial_count = int(self.nodes / 2)
		bias = 0

		# We analyse the probability of state 0 winning
		# against the bias
		x_bias = []
		y_prob = []
		while bias + state_0_initial_count <= self.nodes:
			print(f"Running with bias {bias}")
			# Run the network and check the final counts
			state_0_count = bias + state_0_initial_count
			state_1_count = self.nodes - state_0_count
			states_config = [state_0_count, state_1_count]

			# Run this network with the specified number of rounds
			state_0_win_count = 0
			for i in range(self.rounds):
				network = PopulationNetwork(self.nodes, self.states, self.protocol, states_config)
				while not network.has_converged():
					network.run_round()

				# Now check the final configuration, as network has converged
				last_round = max(network.logger.data)
				last_round_states = network.logger.data.get(last_round)

				if last_round_states[0] == 0:
					state_0_win_count += 1

			# Once all the rounds have run, we can this data to out plot
			x_bias.append(bias)

			# Calculate probability of state 0 winning as the number of times it won
			prob_state_0_wins = state_0_win_count / self.rounds
			y_prob.append(prob_state_0_wins)

			bias += 1

		# Plot the data and show it
		f = plt.figure()
		plt.plot(x_bias, y_prob)

		plt.xlabel("Bias")
		plt.ylabel("Probability of convergence")
		plt.title(f"Probability change with bias")
		f.show()

	@staticmethod
	def info():
		return "An analyser that shows the probability of convergence in a 2 state network as the bias increases"


class NMajorityAnalyser(Analyser):
	def analyse(self):
		if self.rounds < 100:
			print("Warning: A high number of rounds is recommended for the N-Majority analyser")

		# if self.state_config is not None or self.states is not None:
		# 	print("Error: A state configuration/number of states is unnecessary for the N-Majority analyser")
		# 	return

		if self.nodes < 4:
			print("Error: A minimum of 4 nodes is required for the N-Majority analyser")
			return

		# We analyse the average number of rounds til convergence for each majority protocol
		x_majority_axis = []
		y_avg_rounds = []
		for n_majority in range(3, self.nodes, 2):
			print(f"Running {n_majority} protocol")
			# Increase n majority of protocol by 2 each time
			protocol = NMajorityProtocol(n_majority)

			# The state of each node should be different
			state_config = [1] * self.nodes
			print("LENGTH IS " + str(len(state_config)))

			total_convergence_rounds = 0
			for i in range(self.rounds):
				# Create and run the network
				network = PopulationNetwork(self.nodes, self.nodes, protocol, state_config)

				while not network.has_converged():
					network.run_round()

				number_of_rounds = len(network.data.keys())
				total_convergence_rounds += number_of_rounds

			# Calculate average number of rounds until convergence for this protocol
			avg_convergence_rounds = math.floor(total_convergence_rounds / self.rounds)

			print(f"AVG IS {avg_convergence_rounds}")

			x_majority_axis.append(n_majority)
			y_avg_rounds.append(avg_convergence_rounds)

		# Plot data and show it
		f = plt.figure()
		plt.plot(x_majority_axis, y_avg_rounds)

		plt.xlabel("N - Majority")
		plt.ylabel("Average number of rounds")
		plt.title(f"Average number of rounds until convergence for N-Majority protocols")
		f.show()

	@staticmethod
	def info():
		return "An analyser that increases the number of nodes sampled, with 3, 5, 7, etc majority, plotting the average number of rounds to convergence."