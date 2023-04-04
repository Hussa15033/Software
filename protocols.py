from abc import ABC, abstractmethod
import random
import collections
import math


class PopulationProtocol(ABC):
	@abstractmethod
	def run(self, state, neighbour_states):
		pass

	@abstractmethod
	def is_converged(self, states):
		pass

	@abstractmethod
	def get_protocol_name(self):
		pass


# A class for the majority protocols
class MajorityProtocol(PopulationProtocol, ABC):
	def is_converged(self, states):
		state_counts = collections.Counter(states)
		if len(state_counts.keys()) == 1:
			return True

		return False


class VoterModel(MajorityProtocol):
	def run(self, state, neighbour_states):
		# Voter model simply selects a neighbour at random and changes its state
		return random.choice(neighbour_states)

	def get_protocol_name(self):
		return "voter"


class TwoChoiceProtocol(MajorityProtocol):
	def run(self, state, neighbour_states):
		# Two choice selects 2 neighbours and if the state matches, change its opinion to that
		# otherwise keep its current state

		sampled_neighbours = random.sample(neighbour_states, 2)

		if sampled_neighbours[0] == sampled_neighbours[1]:
			return sampled_neighbours[0]

		# Keep current state
		return state

	def get_protocol_name(self):
		return "twochoice"


class NMajorityProtocol(MajorityProtocol):
	def __init__(self, n):
		# n represents the majority, e.g 3-majority selects 3 neighbours, 5-majority selects 5 neighbours
		# If there is a majority amongst these neighbours, that opinion is adopted, otherwise a random neighbour
		# is selected and their opinion is adopted
		self.n = int(n)

		if n % 2 != 1:
			raise ValueError("N must be an odd integer for the N-majority protocol")

	def run(self, state, neighbour_states):
		if len(neighbour_states) < self.n:
			raise ValueError(f"This majority protocol requires {self.n} neighbours ({len(neighbour_states)} neighbours found)")

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

	def get_protocol_name(self):
		return "n-majority"


class ThreeMajority(NMajorityProtocol):
	def run(self, state, neighbour_states):
		return super().run(state, neighbour_states)

	def __init__(self):
		super().__init__(3)

	def get_protocol_name(self):
		return "threemajority"


