from abc import ABC, abstractstaticmethod, abstractclassmethod

class PopulationProtocol(ABC):
	@abstractclassmethod
	def run(state, neighbour_states):
		pass

	# @staticmethod
	@abstractclassmethod
	def is_converged(states):
		pass

	@abstractclassmethod
	# @classmethod
	def get_protocol_name():
		pass