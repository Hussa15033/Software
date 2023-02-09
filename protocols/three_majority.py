from protocols.protocol import PopulationProtocol
import random
import collections

class ThreeMajority(PopulationProtocol):
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

	def is_converged(states):
		state_counts = collections.Counter(states)
		if len(state_counts.keys()) == 1:
			return True

		return False

	def get_protocol_name():
		return "threemajority"