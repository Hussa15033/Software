from abc import ABC, abstractmethod

class Agent(ABC):

	def __init__(self, initial_state):
		self.state = initial_state

	def get_state():
		return self.state

	@abstractmethod
	def update_state(self, new_state):
		pass