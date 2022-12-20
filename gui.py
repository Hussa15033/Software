import tkinter as tk

root = tk.Tk()
root.geometry("800x500")
root.title("Population Protocol")
# Top bar
top_bar = tk.Frame(root, bg="blue")
create_protocol = tk.Button(top_bar, text = "Create protocol..")

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