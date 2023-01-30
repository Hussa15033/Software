from network import PopulationNetwork
from protocols.three_majority import ThreeMajority

import collections
pop = PopulationNetwork(10, 2, ThreeMajority)

for i in range(0, 1000):
	print(collections.Counter(pop.get_states()))
	pop.run_round()

