import networkx as nx
import numpy as np
from tkinter import *
import gutils
import matching.states as mst
import matching

MID_LINE = 0
BIGGER = 1
IND_MODE = BIGGER

radius = 3

primary = 'red'
light_primary = "#ffbebe"
secondary = 'blue'
light_secondary = "#bedbff"

class MatchingDevice(object):
    '''Interactive Tkinter window for creating a graph'''

    def __init__(self, filepath="../graphs/counter.txt", max_edges=27):
        '''
        filepath: the name of a file to load
        indicator: tkinter canvas object corresponding to current nearest edge
        total_edges: the number of edges that the user has added to their
            pair of dijoint matchings
        max_edges: the max possible number of edges for the currently loaded
            graph
        state: the device state, manages clicks and the matchings
        root, canvas: tkinter objects
        '''
        
        self.filepath = filepath
        self.max_edges = max_edges
        self.total_edges = 0

        # keeps track of the line indicating the nearest edge
        # stores canvas object
        self.indicator = -1

        # Tkinter boilerplate
        self.root = Tk()
        window = Frame(self.root)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        x = screenwidth /2
        y = screenheight/2
        self.root.geometry('%dx%d+%d+%d' % (screenwidth, screenwidth, x, y))
        window.pack()

        # set up canvas
        self.canvas = Canvas(window, height=screenheight, width=screenwidth)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<Key>", self.key)

        self.load_graph()
        edge_list = list(self.graph.edges(data=False))
        self.state = mst.ColorEdge(self.graph, self.canvas, edge_list, primary,
                light_primary)

    def begin(self):
        self.root.mainloop()

    def load_graph(self):
        self.graph = gutils.load_graph(self.filepath)
        
        edge_list = list(self.graph.edges(data=False))
        self.state = mst.ColorEdge(self.graph, self.canvas, edge_list, primary,
                light_primary)

        self.draw_graph()
        self.state.color_remaining()

    def draw_graph(self):
        '''Draw the whole graph from scratch. Used when loading a graph'''
        for edge in self.graph.edges():
            new_edge_obj = self.draw_edge(edge)
            self.graph[edge[0]][edge[1]]['obj'] = new_edge_obj
        for node in self.graph.nodes(data=True):
            coords = node[-1]['coord']
            self.graph.nodes[node[0]]['obj'] = self.draw_node(coords[0], coords[1])

        # not be safe if nodes have been deleted
        # self.indx = self.graph.number_of_nodes()

    def draw_edge(self, edge):
        p0 = self.graph.nodes[edge[0]]['coord']
        x0 = p0[0]
        y0 = p0[1]

        p1 = self.graph.nodes[edge[1]]['coord']
        x1 = p1[0]
        y1 = p1[1]
        return self.canvas.create_line(x0,y0,x1,y1)

    def draw_node(self, x, y):
        x0 = x - radius
        y0 = y - radius

        x1 = x + radius
        y1 = y + radius

        return self.canvas.create_oval(x0,y0,x1,y1)

    def clear_edges(self):
        '''recolor all edges black'''
        for curr_edge in self.graph.edges(data=True):
            obj = curr_edge[-1]['obj']
            self.canvas.itemconfig(obj, fill='black', width=1)

    # maybe belongs in State?
    def maximum_matching(self):
        self.clear_edges()

        #indicate the matching
        max_matching = nx.max_weight_matching(self.graph)
        for curr_edge in max_matching:
            extant_edge = self.graph[curr_edge[0]][curr_edge[1]]
            self.canvas.itemconfig(extant_edge['obj'], fill=MATCHING_COLOR, width=3)

    def key(self, event):
        char = event.char

        if char == 'l':
            #self.graph = nx.Graph()
            #print("self.graph currently has:", self.graph.number_of_nodes(), "nodes")
            #self.graph = gutils.load_graph("counter.txt")
            #print("and now:", self.graph.number_of_nodes(), "nodes")
            #setup_self.graph()
            print("load mode")

        elif char == 'n':
            remaining_edges = self.state.nonmatching_edges + self.state.remaining_edges
            self.total_edges += len(self.state.matching_edges)
            self.state = mst.ColorEdge(self.graph, self.canvas, remaining_edges,
                    secondary, light_secondary)
            self.state.color_remaining()

        elif char == 'd':
            # NOTE: only press 'd' once
            self.total_edges += len(self.state.matching_edges)
            print("      Edges used: %d" % (self.total_edges))
            print("Maximum possible: %d" % (self.max_edges))
            if (self.max_edges - self.total_edges >= 2):
                print("press 'r' to try again or 'l' to try the next graph")
            elif (self.max_edges - self.total_edges == 1):
                print("So close! press 'r' to try again")
            else:
                print("Well done!")

        elif char == 'r':
            # reset the graph. Uncolor all edges, reset state, 
            self.clear_edges()
            edge_list = list(self.graph.edges(data=False))
            self.state = mst.ColorEdge(self.graph, self.canvas, edge_list, primary,
                    light_primary)
            self.state.color_remaining()
            self.indicator = -1
            self.total_edges = 0
            self.manual_indicator_update()

        elif char == 'c':
            self.clear_edges()

    def click(self, event):
        self.state.on_click(event)
        self.manual_indicator_update()

    def manual_indicator_update(self):
        '''Show a new indicator. Code taken from
        https://stackoverflow.com/a/22943296'''
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        abs_coord_x = x - self.root.winfo_rootx()
        abs_coord_y = y - self.root.winfo_rooty()
        self.update_indicator(abs_coord_x, abs_coord_y)

    def motion(self, event):
        self.update_indicator(event.x, event.y)

    def update_indicator(self, x, y):
        '''Update the indicator showing the nearest edge'''
        if len(self.state.remaining_edges) < 1:
            return

        if IND_MODE == MID_LINE:
            # kind of ugly and the other one is cute
            if self.indicator != -1:
                self.canvas.delete(self.indicator)

            midpoint = self.state.get_nearest_edge_midpoint(x, y)
            self.indicator = self.canvas.create_line(x, y, midpoint[0],
                    midpoint[1], fill='green')
        elif IND_MODE == BIGGER:
            if self.indicator != -1:
                self.canvas.itemconfig(self.indicator, width=3)

            nearest_index = self.state.get_nearest_edge_index(x, y)
            nearest_edge = self.state.remaining_edges[nearest_index]
            self.indicator = self.graph[nearest_edge[0]][nearest_edge[1]]['obj']
            self.canvas.itemconfig(self.indicator, width=7)
