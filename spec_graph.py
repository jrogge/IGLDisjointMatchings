import networkx as nx
import gutils

margin = 100
step_size = 50
base = 8
idx = 0
graph = nx.Graph()
for vert in range(8):
    coord = [margin + vert * step_size, margin]
    graph.add_node(idx, coord=coord)
    if (vert > 0):
        graph.add_edge(idx, idx - 1)
    idx += 1

for row in range(1,5):
    num_entries = 2 * (5 - row)
    for vert in range(num_entries):
        coord = [margin + (vert+row-1) * step_size, margin + row * step_size]
        graph.add_node(idx, coord=coord)
        if (vert > 0):
            graph.add_edge(idx, idx - 1)
            print("within row adding edge", idx, idx-1)
        if (row > 1):
            graph.add_edge(idx, idx - (num_entries + 1))
            print("between row adding edge", idx, idx - (num_entries + 1))
        else:
            graph.add_edge(idx, idx - (num_entries))
            print("first between row adding edge", idx, idx - (num_entries))
        idx += 1

gutils.save_graph(graph, "counter.txt")
