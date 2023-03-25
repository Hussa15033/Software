from abc import ABC
import random
import collections


class PopulationProtocol(ABC):
	@staticmethod
	@abstractmethod
	def run(cls, state, neighbour_states):
		pass

	@staticmethod
	@abstractmethod
	def is_converged(states):
		pass

	@staticmethod
	@abstractmethod
	def get_protocol_name():
		pass


class ThreeMajority(PopulationProtocol):
	@staticmethod
	def run(state, neighbour_states):
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
	def is_converged(states):
		state_counts = collections.Counter(states)
		if len(state_counts.keys()) == 1:
			return True

		return False

	@staticmethod
	def get_protocol_name():
		return "threemajority"
