import networkx as nx
from tkinter import *

class State(object):
    '''Base State class'''

    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas

    def get_nearest_node(x, y):
        dist = -1
        index = -1
        for node in self.graph.nodes(data=True):

            #TODO: debugging
            print("node:", node)

            coords = node[-1]['coord']
            curr_dist = (coords[0] - x)**2 + (coords[1] - y)**2
            if (curr_dist < dist) or (dist == -1):
                dist = curr_dist
                index = node[0]

        return index

    def on_click(self, event):
        pass

class AddNode(State):
    '''Clicking adds a node to graph'''

    def on_click(self, event):
        node_list.append((event.x, event.y))
        x0 = x - radius
        y0 = y - radius
        x1 = x + radius
        y1 = y + radius
        self.canvas.create_oval(x0,y0,x1,y1)
        next_index = self.graph.number_of_nodes()
        graph.add_node(next_index, coord=[event.x,event.y])

class AddEdge(State):
    '''Clicking adds a edge to graph'''
    def __init__(self):
        self.first_node = -1

    def on_click(self, event):
        nearest_index = self.get_nearest_node(event.x, event.y)
        if self.first_node == -1:
            self.first_node = nearest_index
        else:
            x0 = node_list[self.first_node][0]
            y0 = node_list[self.first_node][1]
            x1 = node_list[nearest_index][0]
            y1 = node_list[nearest_index][1]
            new_edge_obj = canvas.create_line(x0,y0,x1,y1)
            graph.add_edge(self.first_node, nearest_index, obj = new_edge_obj)

            if mode == ADD_EDGE:
                # reset this
                self.first_node = -1
            elif mode == ADD_PATH:
                self.first_node = nearest_index


