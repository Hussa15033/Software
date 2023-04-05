from network import PopulationNetwork
from protocols import ThreeMajority
import time
import timeit

def benchmark():
	n = 100000
	network = PopulationNetwork.network_from_configuration(n, 2, ThreeMajority(), [int(n / 2), int(n / 2)])

	while not network.has_converged():
		network.run_round()


a = timeit.timeit(benchmark, number=1)

print(a)
# start_time = time.time()

# print("Time taken: %s seconds" % str(time.time() - start_time))



