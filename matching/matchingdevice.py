import networkx as nx
import numpy as np
from tkinter import *
import gutils
import matching.states as mst
import matching as consts

MID_LINE = 0
BIGGER = 1
IND_MODE = BIGGER
#TODO: make it easier to restart, currently juggling definitions in a lot of
#places

class MatchingDevice(object):
    '''Interactive Tkinter window for creating a graph'''

    def __init__(self, filepaths=["../graphs/spanner.txt"]):
        '''
        filepaths: a list containing the paths to files to load
        indicator: tkinter canvas object corresponding to current nearest edge
        total_edges: the number of edges that the user has added to their
            pair of dijoint matchings
        state: the device state, manages clicks and the matchings
        root, canvas: tkinter objects
        '''
        self.filepaths = filepaths
        self.curr_file = filepaths[0]
        self.total_edges = 0
        self.on_second_matching = False

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

        # set up the graph and screen
        self.load_graph()

    def begin(self):
        self.root.mainloop()

    def center(self):
        ''' Center and scale a graph on the screen changing coordinate data
        so that it is fairly large. What this is really doing is finding the
        largest centered square on the screen and fitting the graph in that
        square.
        Should probably be broken up into two functions: scale and center'''
        bbx = gutils.get_bounding_box(self.graph)
        bbx_width = bbx[1][0] - bbx[0][0]
        bbx_height = bbx[1][1] - bbx[0][1]
        max_bbx_coord = max(bbx_width, bbx_height)

        # get the largest square that will fit in the screen
        screenwidth = self.canvas.winfo_width()
        screenheight = self.canvas.winfo_height()

        # if you check before the mainloop the canvas size is 1x1
        if screenwidth == 1:
            screenwidth = self.root.winfo_screenwidth()
        if screenheight == 1:
            screenheight = self.root.winfo_screenheight()
        is_wide_screen = screenwidth > screenheight
        min_screen_dim = 0
        if is_wide_screen:
            min_screen_dim = screenheight
        else:
            min_screen_dim = screenwidth

        # want to leave a margin on both sides
        tight_dim = min_screen_dim - (consts.margin * 2)
        scale_factor = tight_dim / max_bbx_coord
        gutils.scale_graph(self.graph, scale_factor)

        #new_base_x = consts.margin
        #new_base_y = consts.margin
        new_base_x = 0
        new_base_y = 0
        new_base_x = (screenwidth - (bbx_width * scale_factor)) / 2
        new_base_y = (screenheight - (bbx_height * scale_factor)) / 2
        #new_base_y -= 25
        delta_x = new_base_x - (bbx[0][0] * scale_factor)
        delta_y = new_base_y - (bbx[0][1] * scale_factor)

        gutils.translate_graph(self.graph, (delta_x, delta_y))

    def load_graph(self):
        self.graph = gutils.load_graph(self.curr_file)
        self.center()
        
        edge_list = list(self.graph.edges(data=False))
        self.state = mst.ColorEdge(self.graph, self.canvas, edge_list,
                consts.primary_color, consts.light_primary)
        self.on_second_matching = False

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

    def draw_edge(self, edge):
        p0 = self.graph.nodes[edge[0]]['coord']
        x0 = p0[0]
        y0 = p0[1]

        p1 = self.graph.nodes[edge[1]]['coord']
        x1 = p1[0]
        y1 = p1[1]
        return self.canvas.create_line(x0,y0,x1,y1)

    def draw_node(self, x, y):
        x0 = x - consts.radius
        y0 = y - consts.radius

        x1 = x + consts.radius
        y1 = y + consts.radius

        return self.canvas.create_oval(x0,y0,x1,y1)

    def clear_edges(self):
        '''recolor all edges black'''
        for curr_edge in self.graph.edges(data=True):
            obj = curr_edge[-1]['obj']
            self.canvas.itemconfig(obj, fill='black', width=1)

    def take_second_matching(self):
        '''Progress on to second matching'''
        if self.on_second_matching:
            return
        remaining_edges = self.state.nonmatching_edges + self.state.remaining_edges
        self.total_edges += len(self.state.matching_edges)
        self.state = mst.ColorEdge(self.graph, self.canvas, remaining_edges,
                consts.secondary_color, consts.light_secondary)
        self.state.color_remaining()
        self.on_second_matching = True

    def key(self, event):
        char = event.char

        # load a different graph
        if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            index = int(char) - 1
            if index < len(self.filepaths):
                self.canvas.delete('all')
                self.curr_file = self.filepaths[index]
                self.load_graph()
                self.manual_indicator_update()

        elif char == 'n':
            self.take_second_matching()

        # reset the graph. Uncolor all edges, reset state, 
        elif char == 'r':
            self.clear_edges()
            edge_list = list(self.graph.edges(data=False))
            self.state = mst.ColorEdge(self.graph, self.canvas, edge_list,
                    consts.primary_color, consts.light_primary)
            self.state.color_remaining()
            self.indicator = -1
            self.total_edges = 0
            self.manual_indicator_update()
            self.on_second_matching = False

        elif char == 'c':
            self.clear_edges()

    def click(self, event):
        self.state.on_click(event)
        self.manual_indicator_update()
        if len(self.state.remaining_edges) == 0:
            self.take_second_matching()

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
