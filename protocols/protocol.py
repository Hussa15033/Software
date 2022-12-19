from abc import ABC, abstractmethod

class PopulationProtocol(ABC):
	@classmethod
	@abstractmethod
	def run(state, neighbour_states):
		pass

	@staticmethod
	@abstractmethod
	def is_converged(states):
		pass
