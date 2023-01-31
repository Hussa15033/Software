# This class is a simple data logger object to store the state of the graph
# in particular rounds

class DataLogger:
	def __init__(self):
		# The data, stores a list of states for every round
		# The round number is the key to the dict
		self.data = {}

	def log_graph(self, round_no, state_list):
		if (self.data.get(round_no) is not None):
			raise ValueError(f"Data for round {round_no} already exists in data logger!")

		self.data[round_no] = state_list

	def get_number_of_rounds(self):
		return len(self.data.keys())