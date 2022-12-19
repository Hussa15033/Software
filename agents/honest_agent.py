from agents.agent import Agent

class HonestAgent(Agent):
	def update_state(self, new_state):
		self.state = new_state

