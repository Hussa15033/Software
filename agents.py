from abc import ABC, abstractmethod


class Agent(ABC):

	def __init__(self, initial_state):
		self.state = initial_state

	def get_state(self):
		return self.state

	@abstractmethod
	def update_state(self, new_state):
		pass


class HonestAgent(Agent):
	def update_state(self, new_state):
		self.state = new_state


class FaultyAgent(Agent):
	def update_state(self, new_state):
		# This agent does not update it's state
		return
