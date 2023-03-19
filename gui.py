import tkinter as tk
import customtkinter as ctk
import random
import collections
import agents
import matplotlib
from analysers import basic_analysis
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
# from parser import GUI_NODE_LIMIT
import numpy as np
# from protocols import ThreeMajority, ThreeMajorityConverged
# from protocols import ThreeMajority, PopulationProtocol
from protocols.protocol import PopulationProtocol
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

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

GUI_NODE_LIMIT = 50
class ConfigurationModal:
	def __init__(self, parent):
		# Setup validation variable -> Modal is not validated intially
		self.validated = False
		self.nodes = None
		self.states = None
		self.rounds = None

		self.top = ctk.CTkToplevel(parent)
		self.top.grab_set()
		self.top.focus_set()
		ctk.CTkLabel(self.top, text='Number of nodes:').pack()
		self.number_nodes_entry = ctk.CTkEntry(self.top)
		self.number_nodes_entry.pack()

		ctk.CTkLabel(self.top, text='Max number of states:').pack()
		self.number_states_entry = ctk.CTkEntry(self.top)
		self.number_states_entry.pack()

		ctk.CTkLabel(self.top, text='Max number of rounds (optional):').pack()
		self.number_rounds_entry = ctk.CTkEntry(self.top)
		self.number_rounds_entry.pack()

		ctk.CTkLabel(self.top, text='Protocol:').pack()

		# Protocol selection menu
		self.protocol_dict = {protocol_class.get_protocol_name(): protocol_class for protocol_class in PopulationProtocol.__subclasses__()}
		protocol_list = list(self.protocol_dict.keys())

		self.chosen_protocol = ctk.CTkStringVar(self.top)
		self.chosen_protocol.set("Select protocol")

		protocol_option = ctk.CTkOptionMenu(self.top, self.chosen_protocol, *protocol_list)
		protocol_option.pack()

		ctk.CTkButton(self.top, text='Simulate!', command=self.validate).pack()

	def validate(self):
		print("LOL TEST1")
		# Check all inputs are valid, if so destroy modal
		# otherwise show an alert for the relevant incorrect input(s)
		# return self.number_nodes_entry.get()
		
		# Assume all inputs are valid
		is_valid = True

		# Check the nodes
		number_nodes = self.number_nodes_entry.get()
		if (not number_nodes.isnumeric()) or int(number_nodes) <= 0 or int(number_nodes) > GUI_NODE_LIMIT:
			ctk.CTkmessagebox.showerror("Error", f"Node input is invalid. Please enter a number between 1 and {GUI_NODE_LIMIT}")
			return

		self.nodes = int(number_nodes)

		# Check states
		number_states = self.number_states_entry.get()
		if (not number_states.isnumeric()) or int(number_states) > self.nodes or int(number_states) < 1:
			ctk.CTkmessagebox.showerror("Error", f"Number of states must between 1 and the number of nodes")
			return

		self.states = int(number_states)

		# Check max rounds, if empty then just use None
		max_rounds = self.number_rounds_entry.get()
		if max_rounds.isnumeric() and int(max_rounds) >= 1:
			self.max_rounds = int(max_rounds)
		elif max_rounds == "":
			self.max_rounds = None
		else:
			ctk.CTkmessagebox.showerror("Error", f"Please enter a valid number of rounds, or leave blank for convergence")
			return
		
		# Check a valid protocol has been selected
		self.protocol = self.protocol_dict.get(self.chosen_protocol.get(), None)
		if self.protocol is None:
			ctk.CTkmessagebox.showerror("Error", "Please select a valid protocol")
			return

		self.top.destroy()

class StateEntryWidget(ctk.CTkFrame):
	def __init__(self, parent, state_colour, state_id, state_nodes):
		ctk.CTkFrame.__init__(self, parent)

		# Create node colour dot, and add labels for texts
		canvas = ctk.CTkCanvas(self, height=10, width=20)
		canvas.create_oval(5, 5, 15, 15, fill = state_colour)
		canvas.pack(side=ctk.LEFT, fill="both")
		self.state_id_label = ctk.CTkLabel(self, text = "State " + str(state_id))
		self.state_id_label.pack(side=ctk.LEFT, fill = "x", expand = True)

		self.node_count_label = ctk.CTkLabel(self, text = state_nodes, anchor="e")
		self.node_count_label.pack(side=ctk.RIGHT, fill = "both", expand = True)

	def set_state_count(self, count):
		self.node_count_label.configure(text = count)

class SimulationGUI:
	def __init__(self, network):
		self.window = ctk.CTk()
		self.window.geometry("800x500")
		self.window.title("Population Protocol")

		self.add_menu_bar()

		# Top bar
		top_bar = ctk.CTkFrame(self.window, fg_color="blue")

		# Right panel
		right_panel = ctk.CTkFrame(self.window, width=50)

		# State list
		self.state_list = ctk.CTkScrollableFrame(right_panel)
		# self.state_list = ctk.CTkScrollbar(right_panel, orient="vertical")
		# scrollbar = ctk.CTkScrollbar(self.state_list, orient="vertical")
		# scrollbar.pack(side=ctk.RIGHT, fill="y", expand = True)

		# Graph and canvas panel
		self.graph_window = ctk.CTkFrame(self.window, fg_color="#ff0000")
		
		# Pack all components
		# todo Do not pack canvas widget yet

		# Round info label
		self.status_label = ctk.CTkLabel(top_bar, text = "Start network")

		# List of tuples for all states of (color, id, nodes supporting)
		self.state_node_list = []

		# Add Buttons
		# create_protocol_btn = ctk.CTkButton(top_bar, text = "Create protocol..", command = show_config_modal)
		create_protocol_btn = ctk.CTkButton(self.graph_window, text = "Create protocol..", command = self.show_config_modal)
		play_btn = ctk.CTkButton(right_panel, text="Play", command = self.start)
		pause_btn = ctk.CTkButton(right_panel, text="Pause", command = self.pause)
		step_btn = ctk.CTkButton(right_panel, text = "Step", command = self.step)
		view_data_btn = ctk.CTkButton(right_panel, text = "View data", command = self.show_basic_analysis)

		
		# Pack all components
		# create_protocol_btn.pack()
		# Top bar packing
		# create_protocol_btn.pack(side=ctk.LEFT)
		self.status_label.pack(side=ctk.LEFT)
		top_bar.pack(fill = "x")

		# Right panel
		play_btn.pack()
		pause_btn.pack()
		step_btn.pack()
		view_data_btn.pack()
	

		# Create the state list frame and pack all necessary elements
		state_panel = ctk.CTkFrame(right_panel)
		ctk.CTkLabel(right_panel, text='States', pady=10).pack(fill="x")
		self.state_list.pack(fill="y", expand = True)
		
		right_panel.pack(side=ctk.RIGHT, fill="y", ipadx=20)
		state_panel.pack(fill="both", expand = True)


		# Graph panel
		self.graph_figure = plt.figure(1, figsize=(10, 5), dpi=100)
		self.canvas = FigureCanvasTkAgg(self.graph_figure, self.graph_window)
		self.canvas.get_tk_widget().pack(fill = "both", expand = True)
		self.graph_window.pack(expand = True, side=ctk.BOTTOM, fill = "both")

		self.state_entries = None
		self.set_network(network)
		
		self.paused = True
		self.window.bind("<<update_network>>", self.show_network_evt)
		self.window.protocol("WM_DELETE_WINDOW", self.quit)
		self.window.mainloop()

	def quit(self):
		self.window.quit()

	def show_basic_analysis(self):
		self.wait_round()
		self.close_extra_figures()
		analyser = basic_analysis(self.network.logger, self.state_colours)
		

	def add_menu_bar(self):
		menu = tk.Menu(self.window)

		file_menu = tk.Menu(menu, tearoff=0)
		file_menu.add_command(label="Create protocol..", command=lambda: self.show_config_modal())
		file_menu.add_separator()
		file_menu.add_command(label="Quit", command = self.quit)
		menu.add_cascade(label = "File", menu=file_menu)

		self.window.config(menu=menu)

	def show_config_modal(self):
		config = ConfigurationModal(self.window)
		self.window.wait_window(config.top)
		new_network = PopulationNetwork(config.nodes, config.states, config.protocol, max_rounds = config.max_rounds)
		self.set_network(new_network)

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
		# Close any open figures
		self.close_extra_figures()
		self.paused = False

		# Start and simulate the network
		# Create a thread to do the computation, using an event to wait for the result
		# This frees the GUI thread to allow simulation to be paused
		event = threading.Event()
		self.running_thread = threading.Thread(target = self.propel)
		self.running_thread.start()

	def wait_round(self):
		# This method waits for the current round to finish processing (if it is running)
		# and then pauses the network
		self.paused = True
		# Wait on the running thread if it exists
		try:
			if self.running_thread.is_alive():
				self.running_thread.join()
		except:
			# If the thread doesn't exist yet, it is irrelevant to process this exception
			pass

	def close_extra_figures(self):
		# If there multiple open figures, close all other figures, except the current open one
		for i in range(1, len(plt.get_fignums())):
			plt.close()

	def step(self):
		self.close_extra_figures()
		self.wait_round()
			
		self.network.run_round()
		self.window.event_generate("<<update_network>>", when = "tail")

	def show_network_evt(self, evt):
		# Update all necessary GUI elements, including network

		# Update the round/status label
		current_round = self.network.round - 1
		if (self.network.max_rounds is not None and current_round >= self.network.max_rounds):
			self.status_label.configure(text = f"Maximum round of {self.network.max_rounds} reached")
		elif (self.network.has_converged()):
			self.status_label.configure(text = f"Network converged on round {str(current_round)}")
		else:
			self.status_label.configure(text = f"Round {str(self.network.round - 1)}")

		# Update the state entry list
		self.update_state_entries()

		# Show the network
		self.show_network()

	def propel(self):
		while not self.network.has_finished() and not self.paused:
			self.network.run_round()
			self.window.event_generate("<<update_network>>", when="tail")
			time.sleep(1)

		print("Number of rounds:")
		print(self.network.logger.get_number_of_rounds())

	def pause(self):
		print("Pause button clicked")
		self.paused = True

	def set_network(self, network):
		# This method clears any current network, and resets the GUI to load a new network
		self.status_label.configure(text = "Start network")
		self.network = network

		# Clear state entry list GUI
		if self.state_entries is not None:
			for i in range(len(self.state_entries)):
				# Delete any previous entry widgets
				self.state_entries[i].pack_forget()
			self.state_entries = None

		# Create graph and coloured nodes
		self.graph = nx.complete_graph(self.network.get_number_of_nodes())
		self.state_colours = {state: f"#{random.randrange(0x1000000):06x}" for state in self.network.get_states()}
		self.update_state_entries()
		self.show_network()

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