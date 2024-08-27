import tkinter as tk
from tkinter import messagebox
window = tk.Tk()
window.title("Dijkstra's Algorithm with Resources")
window.geometry("400x600")

inputs_frame = tk.Frame(window)
inputs_frame.pack(pady=20)


num_nodes_label = tk.Label(inputs_frame, text="Number of Nodes:")
num_nodes_label.grid(row=0, column=0, padx=10, pady=5)
num_nodes_entry = tk.Entry(inputs_frame)
num_nodes_entry.grid(row=0, column=1)


start_node_label = tk.Label(inputs_frame, text="Start Node:")
start_node_label.grid(row=1, column=0, padx=10, pady=5)
start_node_entry = tk.Entry(inputs_frame)
start_node_entry.grid(row=1, column=1)


resources_label = tk.Label(inputs_frame, text="Resource Availability:")
resources_label.grid(row=2, column=0, padx=10, pady=5)

resources_entry = []
resource_labels = ["Medicine:", "Food:", "Water:"]
for i in range(3):
    resource_label = tk.Label(inputs_frame, text=resource_labels[i])
    resource_label.grid(row=2 + i, column=0, padx=10, pady=5)
    resource_entry = tk.Entry(inputs_frame)
    resource_entry.grid(row=2 + i, column=1)
    resources_entry.append(resource_entry)


demand_frame = tk.Frame(window)
demand_frame.pack(pady=20)


demand_labels = ["Medicine:", "Food:", "Water:"]
for i, label_text in enumerate(demand_labels):
    demand_label = tk.Label(demand_frame, text=label_text)
    demand_label.grid(row=0, column=i + 1, padx=5)


demand_entries = []
def create_demand_entries(num_nodes):
    for i in range(num_nodes):
        node_label = tk.Label(demand_frame, text=f"Node {i}:")
        node_label.grid(row=i + 1, column=0, padx=5)

        entries = []
        for j in range(3):
            entry = tk.Entry(demand_frame)
            entry.grid(row=i + 1, column=j + 1, padx=5)
            entries.append(entry)

        demand_entries.append(entries)


def add_demand_entries():
    num_nodes = int(num_nodes_entry.get())
    create_demand_entries(num_nodes)
    add_demand_entries_button.config(state=tk.DISABLED)

add_demand_entries_button = tk.Button(inputs_frame, text="Add Demand Entries", command=add_demand_entries)
add_demand_entries_button.grid(row=3, columnspan=2, pady=10)


edges_frame = tk.Frame(window)
edges_frame.pack(pady=20)


edges_label = tk.Label(edges_frame, text="Edges:")
edges_label.pack()

edges_listbox = tk.Listbox(edges_frame, width=30, height=5)
edges_listbox.pack(pady=5)


add_edge_frame = tk.Frame(edges_frame)
add_edge_frame.pack()

u_label = tk.Label(add_edge_frame, text="u:")
u_label.grid(row=0, column=0, padx=5)
u_entry = tk.Entry(add_edge_frame)
u_entry.grid(row=0, column=1)

v_label = tk.Label(add_edge_frame, text="v:")
v_label.grid(row=0, column=2, padx=5)
v_entry = tk.Entry(add_edge_frame)
v_entry.grid(row=0, column=3)

weight_label = tk.Label(add_edge_frame, text="Weight:")
weight_label.grid(row=0, column=4, padx=5)
weight_entry = tk.Entry(add_edge_frame)
weight_entry.grid(row=0, column=5)

def add_edge():
    u = u_entry.get()
    v = v_entry.get()
    weight = weight_entry.get()
    edges_listbox.insert(tk.END, f"{u}, {v}, {weight}")
    u_entry.delete(0, tk.END)
    v_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)

add_button = tk.Button(add_edge_frame, text="Add Edge", command=add_edge)
add_button.grid(row=0, column=6, padx=5)


buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=20)

clear_button = tk.Button(buttons_frame, text="Clear Edges", command=lambda: edges_listbox.delete(0, tk.END))
clear_button.grid(row=0, column=0, padx=5)

def dijkstra(graph, start_node, resources):
    num_nodes = len(graph)
    distances = [float('inf')] * num_nodes
    distances[start_node] = 0
    visited = [False] * num_nodes

    for _ in range(num_nodes):
        min_dist = float('inf')
        min_node = None
        for i in range(num_nodes):
            if not visited[i] and distances[i] < min_dist:
                min_dist = distances[i]
                min_node = i

        if min_node is None:
            break

        visited[min_node] = True

        
        for neighbor in graph[min_node]:
            weight = graph[min_node][neighbor]
            if distances[min_node] + weight < distances[neighbor]:
                distances[neighbor] = distances[min_node] + weight

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Shortest Distances from Node {start_node}:\n")
    for i in range(num_nodes):
        output_text.insert(tk.END, f"Node {i} - Shortest Distance: {distances[i]}\n")
        output_text.insert(tk.END, f"Delivering Resources to Node {i}:\n")
        for j, resource in enumerate(resources):
            demand = demand_entries[i][j].get()
            if int(demand) <= resource:
                output_text.insert(tk.END, f"Delivered {demand} {resource_labels[j]} to Node {i}\n")
                resources[j] -= int(demand)
            else:
                output_text.insert(tk.END, f"Insufficient {resource_labels[j]} to deliver to Node {i}\n")
        output_text.insert(tk.END, "\n")

def run_dijkstra():
    num_nodes = int(num_nodes_entry.get())
    start_node = int(start_node_entry.get())

    resources = []
    for entry in resources_entry:
        resources.append(int(entry.get()))

    graph = {}
    for i in range(num_nodes):
        graph[i] = {}

    for edge in edges_listbox.get(0, tk.END):
        u, v, weight = edge.split(", ")
        u = int(u.strip())
        v = int(v.strip())
        weight = int(weight.strip())
        graph[u][v] = weight

    dijkstra(graph, start_node, resources)

run_button = tk.Button(buttons_frame, text="Run Dijkstra", command=run_dijkstra)
run_button.grid(row=0, column=1, padx=5)


output_text = tk.Text(window, height=10)
output_text.pack(pady=20)


def show_about():
    messagebox.showinfo("About", "This is a Dijkstra's Algorithm implementation with resource constraints.")

about_button = tk.Button(window, text="About", command=show_about)
about_button.pack(pady=10)


window.mainloop()
