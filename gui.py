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


def show_config_modal():
	configModal = ConfigurationModal(root)
	root.wait_window(configModal.top)
	print("Finished.")

class SimulationGUI:
	def __init__(self):
		self.window = tk.Tk()
		self.window.geometry("800x500")
		self.window.title("Population Protocol")

		# Top bar
		top_bar = tk.Frame(self.window, bg="blue")

		# Right panel
		right_panel = tk.Frame(self.window, bg="yellow", width="300px")

		# Add Buttons
		# create_protocol_btn = tk.Button(top_bar, text = "Create protocol..", command = show_config_modal)
		create_protocol_btn = tk.Button(top_bar, text = "Create protocol..", command = self.create_network)
		# play_btn = tk.Button(right_panel, text="Play", command = self.start)
		play_btn = tk.Button(right_panel, text="Play", command = self.start )
		pause_btn = tk.Button(right_panel, text="Pause", command = self.pause)

		# Graph and canvas panel
		graph = tk.Frame(self.window, bg="#ff0000")
		f = plt.figure(figsize=(10, 5), dpi=100)
		self.canvas = FigureCanvasTkAgg(f, graph)

		# Pack all components
		self.canvas.get_tk_widget().pack()


		# Top bar packing
		create_protocol_btn.pack(side=tk.LEFT)
		top_bar.pack(fill = "x")

		# Right panel
		play_btn.pack()
		pause_btn.pack()
		right_panel.pack(side=tk.RIGHT, fill="y", ipadx=20)

		# Graph panel
		graph.pack(expand = True, side=tk.BOTTOM, fill = "both")

		# This is only for testing purposes
		self.create_network()
		self.show_network()
		self.paused = True
		self.window.bind("<<update_network>>", self.show_network_evt)
		self.window.mainloop()

	def show_network(self):
		print("Show network shown")
		# Show the current network in the canvas
		color_map = list(map(lambda node: self.state_colours.get(node.state), self.network.get_agents()))

		# Create network graph GUI, fix pos seed to not randomize graph each time
		pos = nx.spring_layout(self.network.get_graph(), seed = 1)

		nx.draw(self.network.get_graph(), pos = pos, node_color = color_map)
		self.canvas.draw()

	def start(self):
		self.paused = False

		event = threading.Event()
		thread = threading.Thread(target = self.propel)
		thread.start()
		print("We have started the thread, does this print?")
		# Start and simulate the network
		# Create a thread to do the computation, using an event to wait for the result
		# This frees the GUI thread to allow simulation to be paused
		# while not self.paused:

		# 	self.network.run_round()

		# 	if self.network.has_converged():
		# 	# Network has converged, we can exit
		# 	self.paused = True
		# 	break
		# 	time.sleep(1)
		# 		# canvas.get_tk_widget().pack_forget()
		
		# 		# f = plt.figure(figsize=(10, 5), dpi=100)
		# 		# canvas = FigureCanvasTkAgg(f, graph)
	
		# 		# canvas.get_tk_widget().pack()
	
		# 		# nx.draw(pop.get_graph(), pos = pos, node_color = color_map)
		# 		# canvas.draw()
		# 	print("Play button clicked")

	def show_network_evt(self, evt):
		self.show_network()

	def propel(self):
		while not self.network.has_converged():
			if self.paused:
				return
			self.network.run_round()
			print("Sleeping for 5 secs")
			time.sleep(1)
			self.window.event_generate("<<update_network>>", when="tail")

	def pause(self):
		print("Pause button clicked")
		self.paused = True

	def create_network(self):
		# A test method to add and create a fixed network
		self.network = PopulationNetwork(50, 20, ThreeMajority)
		self.state_colours = {state: f"#{random.randrange(0x1000000):06x}" for state in self.network.get_states()}

		print("Create protocol button clicked")
		pass


SimulationGUI()

exit()
f = plt.figure(figsize=(10, 5), dpi=100)
# f = plt.figure(figsize=(10, 5), dpi=100)


# Create the population network + GUI
pop = PopulationNetwork(10, 2, ThreeMajority)

state_colours = {state: f"#{random.randrange(0x1000000):06x}" for state in pop.get_states()}

color_map = list(map(lambda node: state_colours.get(node.state), pop.get_agents()))

# Create network graph GUI, fix pos seed to not randomize graph each time
pos = nx.spring_layout(pop.get_graph(), seed = 1)

nx.draw(pop.get_graph(), pos = pos, node_color = color_map)

rnd = 1
while (not pop.has_converged()):
	rnd += 1
	print(rnd)
	pop.run_round()
	print("1")
	time.sleep(1)
	canvas.get_tk_widget().pack_forget()
	plt.close('all')
	print("2")
	f = plt.figure(figsize=(10, 5), dpi=100)
	canvas = FigureCanvasTkAgg(f, graph)
	print("3")
	canvas.get_tk_widget().pack()
	print("4")
	color_map = list(map(lambda node: state_colours.get(node.state), pop.get_agents()))
	nx.draw(pop.get_graph(), pos = pos, node_color = color_map)
	print("5")
	canvas.draw()
	print("6")

exit()