from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
class Analyser(ABC):
	def __init__(self, nodes, state_config, protocol, rounds):
		self.nodes = nodes
		self.state_config = state_config
		self.protocol = protocol
		self.rounds = rounds

	@abstractmethod
	def analyse():
		pass

def basic_analysis(data_logger, state_colours = None):
	# A basic analyser that takes a round of data logs and produces a
	# plot of each state in the network against the 
	data = data_logger.data

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
		if (state_colours is not None):
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