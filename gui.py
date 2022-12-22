import tkinter as tk

root = tk.Tk()
root.geometry("800x500")
root.title("Population Protocol")

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

# Top bar
top_bar = tk.Frame(root, bg="blue")

create_protocol = tk.Button(top_bar, text = "Create protocol..", command = show_config_modal)

# Graph panel
graph = tk.Frame(root, bg="#ff0000")

p = tk.Button(graph, text="Test")
p.pack()

# Right panel creation
right_panel = tk.Frame(root, bg="yellow", width="300px")

play_simulation = tk.Button(right_panel, text="Play")
pause_simulation = tk.Button(right_panel, text="Pause")

# Top bar packing
create_protocol.pack(side=tk.LEFT)
top_bar.pack(fill = "x")

# Right panel packing
play_simulation.pack()
pause_simulation.pack()
right_panel.pack(side=tk.RIGHT, fill="y", ipadx=20)

# Graph window packing
graph.pack(expand = True, side=tk.BOTTOM, fill = "both")

root.mainloop()