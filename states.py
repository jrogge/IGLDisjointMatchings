import networkx as nx
from tkinter import *

class State(object):
    '''Base State class'''

    def __init__(self, graph, canvas, radius=3):
        self.graph = graph
        self.canvas = canvas
        self.radius = radius

    def get_nearest_node(self, x, y):
        dist = -1
        index = -1
        for node in self.graph.nodes(data=True):
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
        x0 = event.x - self.radius
        y0 = event.y - self.radius
        x1 = event.x + self.radius
        y1 = event.y + self.radius
        self.canvas.create_oval(x0,y0,x1,y1)
        next_index = self.graph.number_of_nodes()
        self.graph.add_node(next_index, coord=[event.x,event.y])

class AddEdge(State):
    '''Clicking adds an edge to graph'''

    def __init__(self, graph, canvas, radius):
        # call State constructor
        super(AddEdge, self).__init__(graph, canvas, radius)
        self.first_node = -1

    def on_click(self, event):
        nearest_index = self.get_nearest_node(event.x, event.y)
        if self.first_node == -1:
            self.first_node = nearest_index
        else:
            v0 = self.graph.nodes[nearest_index]['coord']
            v1 = self.graph.nodes[self.first_node]['coord']
            new_edge_obj = self.canvas.create_line(v0[0],v0[1],v1[0],v1[1])
            self.graph.add_edge(self.first_node, nearest_index,
                    obj = new_edge_obj)
            # reset first node
            self.first_node = -1

class AddPath(State):
    '''Select initial node then create a path stemming from that node'''

    def __init__(self, graph, canvas, radius):
        # call State constructor
        super(AddPath, self).__init__(graph, canvas, radius)
        self.first_node = -1

    def on_click(self, event):
        nearest_index = self.get_nearest_node(event.x, event.y)
        if self.first_node == -1:
            self.first_node = nearest_index
        else:
            v0 = self.graph.nodes[nearest_index]['coord']
            v1 = self.graph.nodes[self.first_node]['coord']
            new_edge_obj = self.canvas.create_line(v0[0],v0[1],v1[0],v1[1])
            self.graph.add_edge(self.first_node, nearest_index,
                    obj = new_edge_obj)
            # reset first node
            self.first_node = nearest_index
