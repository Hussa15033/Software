from abc import ABC
import random
import collections
import math

class PopulationProtocol(ABC):
	def run(self, state, neighbour_states):
		pass

	@staticmethod
	def is_converged(states):
		state_counts = collections.Counter(states)
		if len(state_counts.keys()) == 1:
			return True

		return False

	@staticmethod
	def get_protocol_name():
		pass


class ThreeMajority(PopulationProtocol):
	def run(self, state, neighbour_states):
		# Get 3 random neighbours
		sampled_neighbours = random.sample(neighbour_states, 3)

		# Check for a majority
		state_counts = collections.Counter(sampled_neighbours)
		majority_state, majority_state_count = state_counts.most_common(1)[0]

		if majority_state_count >= 2:
			# Majority state was found in the neighbours, so use this as the new state
			return majority_state

		# A majority was not found, pick a random state from neighbours
		return random.choice(neighbour_states)

	@staticmethod
	def get_protocol_name():
		return "threemajority"


class NMajorityProtocol(PopulationProtocol):
	def __init__(self, n):
		# n represents the majority, e.g 3-majority selects 3 neighbours, 5-majority selects 5 neighbours
		# If there is a majority amongst these neighbours, that opinion is adopted, otherwise a random neighbour
		# is selected and their opinion is adopted
		self.n = n

	def run(self, state, neighbour_states):
		# Get n random neighbours
		sampled_neighbours = random.sample(neighbour_states, self.n)

		# Check for a majority
		state_counts = collections.Counter(sampled_neighbours)
		majority_state, majority_state_count = state_counts.most_common(1)[0]

		if majority_state_count >= math.ceil(self.n / 2):
			# Majority state was found in the neighbours, so use this as the new state
			return majority_state

		# A majority was not found, pick a random state from neighbours
		return random.choice(neighbour_states)

	@staticmethod
	def get_protocol_name():
		return "n-majority"
