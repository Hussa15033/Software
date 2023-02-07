import tkinter as tk
import random
import collections
import agents
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np
# from protocols import ThreeMajority, ThreeMajorityConverged
from protocols.three_majority import ThreeMajority
# import pylab as py
# from agents.honest_agent import HonestAgent
# 
from agents.honest_agent import HonestAgent
import networkx as nx
import time
from network import PopulationNetwork
import threading

	# def update_graph(self):
		# a = f.add_subplot(111)
		# color_map = list(map(lambda agent: self.state_colours.get(agent.state), self.agents.values()))
		# pos = nx.spring_layout(self.graph, seed = 1)
		# # plt.pause(1)
# plt.clf()
		# nx.draw(self.graph, pos = pos, node_color = color_map)	
# plt.show()
		# return plt.figure(figsize=(10, 5), dpi = 100)
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.run_1_round()
# pop.show_graph()
# for i in range(0, 10):
	# pop.run_1_round()
	# pop.update_graph()
	# print("Ran a round ", i)
# pop.show_graph()


# pop.update_graph()
# pop.run_1_round()
# pop.update_graph()

class ConfigurationModal:
	def __init__(self, parent):
		# Setup validation variable -> Modal is not validated intially
		self.validated = False

		self.top = tk.Toplevel(parent)
		self.top.grab_set()
		tk.Label(self.top, text='Number of nodes:').pack()
		self.number_nodes_entry = tk.Entry(self.top)
		self.number_nodes_entry.pack()

		tk.Label(self.top, text='Max number of states:').pack()
		self.number_states_entry = tk.Entry(self.top)
		self.number_states_entry.pack()

		tk.Label(self.top, text='Number of faulty nodes:').pack()
		self.number_faulty_nodes_entry = tk.Entry(self.top)
		self.number_faulty_nodes_entry.pack()

		tk.Label(self.top, text='Max number of rounds (optional):').pack()
		self.number_rounds_entry = tk.Entry(self.top)
		self.number_rounds_entry.pack()

		tk.Label(self.top, text='Protocol:').pack()

		# Protocol selection menu
		protocol_list = ["voter", "2-choice", "3-majority"]

		chosen_protocol = tk.StringVar(self.top)
		chosen_protocol.set("Select protocol")

		w = tk.OptionMenu(self.top, chosen_protocol, *protocol_list)
		w.pack()

		tk.Button(self.top, text='Simulate!', command=self.is_valid).pack()

	def is_valid(self):
		# Check all inputs are valid, if so destroy modal
		# otherwise show an alert for the relevant input
		self.top.destroy()


def show_config_modal(root):
	configModal = ConfigurationModal(root)
	root.wait_window(configModal.top)
	print("Finished.")


class StateEntryWidget(tk.Frame):
	def __init__(self, parent, state_colour, state_id, state_nodes):
		tk.Frame.__init__(self, parent)

		# Create node colour dot, and add labels for texts
		canvas = tk.Canvas(self, height=10, width=20)
		canvas.create_oval(5, 5, 15, 15, fill = state_colour)
		canvas.pack(side=tk.LEFT, fill="both")
		self.state_id_label = tk.Label(self, text = "State " + str(state_id))
		self.state_id_label.pack(side=tk.LEFT, fill = "x", expand = True)

		self.node_count_label = tk.Label(self, text = state_nodes, anchor="e")
		self.node_count_label.pack(side=tk.RIGHT, fill = "both", expand = True)

	def set_state_count(self, count):
		self.node_count_label.config(text = count)

class SimulationGUI:
	def __init__(self, network):
		self.window = tk.Tk()
		self.window.geometry("800x500")
		self.window.title("Population Protocol")

		self.add_menu_bar()

		# Top bar
		top_bar = tk.Frame(self.window, bg="blue")

		# Right panel
		right_panel = tk.Frame(self.window, width="300px")

		# State list
		self.state_list = tk.Frame(right_panel)
		# self.state_list = tk.Scrollbar(right_panel, orient="vertical")
		scrollbar = tk.Scrollbar(self.state_list, orient="vertical")
		scrollbar.pack(side=tk.RIGHT, fill="y", expand = True)

		# Graph and canvas panel
		graph = tk.Frame(self.window, bg="#ff0000")

		# Round info label
		self.status_label = tk.Label(top_bar, text = "Start network")

		# List of tuples for all states of (color, id, nodes supporting)
		self.state_node_list = []

		# Add Buttons
		# create_protocol_btn = tk.Button(top_bar, text = "Create protocol..", command = show_config_modal)
		create_protocol_btn = tk.Button(graph, text = "Create protocol..", command = self.create_network)
		play_btn = tk.Button(right_panel, text="Play", command = self.start)
		pause_btn = tk.Button(right_panel, text="Pause", command = self.pause)
		step_btn = tk.Button(right_panel, text = "Step", command = self.step)

		f = plt.figure(figsize=(10, 5), dpi=100)
		self.canvas = FigureCanvasTkAgg(f, graph)

		# Pack all components
		# todo Do not pack canvas widget yet
		self.canvas.get_tk_widget().pack(fill = "both", expand = True)
		# create_protocol_btn.pack()

		# Top bar packing
		# create_protocol_btn.pack(side=tk.LEFT)
		self.status_label.pack(side=tk.LEFT)
		top_bar.pack(fill = "x")

		# Right panel
		play_btn.pack()
		pause_btn.pack()
		step_btn.pack()

		# Create the state list frame and pack all necessary elements
		state_panel = tk.Frame(right_panel)
		tk.Label(right_panel, text='States', font='10', pady=10).pack(fill="x")
		self.state_list.pack(fill="y", expand = True)
		self.state_entries = None
		right_panel.pack(side=tk.RIGHT, fill="y", ipadx=20)
		state_panel.pack(fill="both", expand = True)


		# Graph panel
		graph.pack(expand = True, side=tk.BOTTOM, fill = "both")

		self.set_network(network)
		self.update_state_entries()
		self.show_network()
		self.paused = True
		self.window.bind("<<update_network>>", self.show_network_evt)
		self.window.protocol("WM_DELETE_WINDOW", self.quit)
		self.window.mainloop()

	def quit(self):
		self.window.quit()

	def add_menu_bar(self):
		menu = tk.Menu(self.window)

		file_menu = tk.Menu(menu, tearoff=0)
		file_menu.add_command(label="Create protocol..", command=lambda: show_config_modal(self.window))
		file_menu.add_separator()
		file_menu.add_command(label="Quit", command = self.quit)
		menu.add_cascade(label = "File", menu=file_menu)

		self.window.config(menu=menu)

	def show_network(self):
		print("Show network shown")
		# Show the current network in the canvas
		# Clear current network
		plt.clf()

		color_map = list(map(lambda state: self.state_colours.get(state), self.network.get_states()))

		# Create network graph GUI, fix pos seed to not randomize graph each time
		pos = nx.spring_layout(self.graph, seed = 1)

		nx.draw(self.graph, pos = pos, node_color = color_map)
		self.canvas.draw()

	def start(self):
		self.paused = False

		# Start and simulate the network
		# Create a thread to do the computation, using an event to wait for the result
		# This frees the GUI thread to allow simulation to be paused
		event = threading.Event()
		self.running_thread = threading.Thread(target = self.propel)
		self.running_thread.start()

	def step(self):
		self.paused = True
		# Wait on the running thread if it exists
		try:
			if self.running_thread.is_alive():
				self.running_thread.join()
		except:
			# If the thread doesn't exist yet, it is irrelevant to process this exception
			pass
			
		self.network.run_round()
		self.window.event_generate("<<update_network>>", when = "tail")

	def show_network_evt(self, evt):
		# Update all necessary GUI elements, including network
		# Show the network
		self.show_network()

		# Update the round/status label
		current_round = self.network.round - 1
		if (self.network.has_converged()):
			self.status_label.config(text = "Network converged on round " + str(current_round))
		else:
			self.status_label.config(text = "Round " + str(self.network.round - 1))

		# Update the state entry list
		self.update_state_entries()

	def propel(self):
		while not self.network.has_converged() and not self.paused:
			self.network.run_round()
			self.window.event_generate("<<update_network>>", when="tail")
			time.sleep(1)

		print("Number of rounds:")
		print(self.network.logger.get_number_of_rounds())

	def pause(self):
		print("Pause button clicked")
		self.paused = True

	def set_network(self, network):
		self.network = network
		self.graph = nx.complete_graph(self.network.get_number_of_nodes())
		self.state_colours = {state: f"#{random.randrange(0x1000000):06x}" for state in self.network.get_states()}

	def update_state_entries(self):
		# print(self.state_list.get())
		# Set the state entry list
		if self.state_entries is None:
			# Entries have not yet been created, add them to the array
			self.state_entries = []

			# Get the list of states, sorted in ascending order
			states_in_network = list(self.state_colours.keys())
			states_in_network.sort()
			for state in states_in_network:
				state_entry = StateEntryWidget(self.state_list, self.state_colours.get(state), state, 0)
				state_entry.pack(fill="x")
				self.state_entries.insert(state, state_entry)

		# Adjust the number of nodes in each entry
		network_states = self.network.get_states()

		for i in range(0, len(self.state_colours.keys())):
			self.state_entries[i].set_state_count(network_states.count(i))




	def create_network(self):
		# A test method to add and create a fixed network
		print("Create protocol button clicked")
		pass


# SimulationGUI()

# exit()