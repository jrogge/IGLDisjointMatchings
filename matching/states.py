import networkx as nx
import numpy as np
from tkinter import *

class MatchingState(object):
    '''Base MatchingState class'''

    def __init__(self, graph, canvas, remaining_edges):
        self.graph = graph
        self.canvas = canvas
        self.remaining_edges = remaining_edges
        self.matching_edges = []
        self.nonmatching_edges = []

    def color_remaining(self):
        pass
    
    def get_edge_midpoint(self, u, v):
        u_coords = np.array(self.graph.nodes[u]['coord'])
        v_coords = np.array(self.graph.nodes[v]['coord'])
        return (u_coords + v_coords) / 2

    def get_nearest_edge_index(self, x, y):
        '''Get index in 'self.remaining_edges' of the edge whose midpoint is
        closest to (x,y)'''
        dist = -1
        index = -1
        for curr_idx, edge in enumerate(self.remaining_edges):
            coords = self.get_edge_midpoint(edge[0], edge[1])
            curr_dist = (coords[0] - x)**2 + (coords[1] - y)**2
            if (curr_dist < dist) or (dist == -1):
                dist = curr_dist
                index = curr_idx

        return index

    def get_nearest_edge_midpoint(self, x, y):
        '''Wrapper around above two functions, might not get used if we decide
        not to go with MID_LINE indicator'''
        index = self.get_nearest_edge_index(x, y)
        edge = self.remaining_edges[index]
        return self.get_edge_midpoint(edge[0], edge[1])

    def remove_adjacent_edges(self, edge):
        '''Find all edges adjacent to edge, create a new remaining list
        excluding those. Add the removed edges to the unused edges list
        (nonmatching_edges)'''
        new_remaining = []
        for curr_edge in self.remaining_edges:
            same_0 = curr_edge[0] == edge[0] or curr_edge[0] == edge[1]
            same_1 = curr_edge[1] == edge[0] or curr_edge[1] == edge[1]
            is_adj = same_0 or same_1
            # this works assuming no multi-edges and no loops
            is_edge = same_0 and same_1
            if (not is_adj):
                # an edge safe to keep in the remaining list
                new_remaining.append(curr_edge)
            elif(is_adj and (not is_edge)):
                # one of the edges removed from possible use
                old_obj = self.graph[curr_edge[0]][curr_edge[1]]['obj']
                self.canvas.itemconfig(old_obj, fill='black', width=1)
                self.nonmatching_edges.append(curr_edge)

        self.remaining_edges = new_remaining

    def on_click(self, event):
        pass

class ColorEdge(MatchingState):
    '''Clicking colors an edge'''

    def __init__(self, graph, canvas, remaining_edges, color, secondary_color):
        super(ColorEdge, self).__init__(graph, canvas, remaining_edges)
        self.color = color
        self.secondary_color = secondary_color

    def color_remaining(self):
        '''Color remaining edges with the secondary color to indicate they are
        available in the matching. Is currently in own function as graph has not
        necessarily been loaded by the time state has been created. This is bad
        and ugly though, will fix eventually.'''
        for edge in self.remaining_edges:
            old_obj = self.graph[edge[0]][edge[1]]['obj']
            self.canvas.itemconfig(old_obj, fill=self.secondary_color, width=3)

    def on_click(self, event):
        '''Add the nearests available edge (if one exists) to the matching.
        Color it with the main color, add it to the matching, and remove
        all adjacent edges from the remaining possibilities (add those to the
        corresponding list)'''
        nearest_edge_index = self.get_nearest_edge_index(event.x, event.y)
        if nearest_edge_index == -1:
            return
        nearest_edge = self.remaining_edges[nearest_edge_index]
        self.matching_edges.append(nearest_edge)

        # color edge to indicate it is in the matching, remove the adjacent
        #   edges so they cannot be added. updating of unused edges
        #   happens in 'self.remove_adjacent_edges'
        self.remove_adjacent_edges(nearest_edge)
        old_obj = self.graph[nearest_edge[0]][nearest_edge[1]]['obj']
        self.canvas.itemconfig(old_obj, fill=self.color, width=3)
