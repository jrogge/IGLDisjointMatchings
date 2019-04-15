import networkx as nx
from tkinter import *
import gutils
import states as st

# TODO: wrap up into a config file
radius = 3
MATCHING_COLOR = 'yellow'

# TODO: wrap up into modes file
ADD_NODE = 0
ADD_EDGE = 1
ADD_PATH = 2
REMOVE_NODE = 3
REMOVE_EDGE = 4

class GraphMaker(object):
    '''Interactive Tkinter window for creating a graph'''

    def __init__(self, mode=ADD_NODE):
        self.filename = ""

        self.graph = nx.Graph() # TODO: add functionality for loading a graph
        self.mode = mode

        #index of last selected node, used in adding/deleting edges
        self.last_node = -1
        # keeps track of the line indicating the nearest node
        # stores canvas object
        self.indicator = -1

        # Tkinter boilerplate
        self.root = Tk()
        window = Frame(self.root)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        x = screenwidth /2
        y = screenheight/2
        self.root.geometry('%dx%d+%d+%d' % (screenwidth/2, screenwidth, x, y))
        window.pack()

        # set up canvas
        self.canvas = Canvas(window, height=screenheight, width=screenwidth/2)
        self.state = st.AddNode(self.graph, self.canvas, radius)

        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<Key>", self.key)

    def begin(self):
        self.root.mainloop()

    def load_graph(self, filename):
        graph = gutils.load_graph(filename)
        self.graph = graph
        
        self.state = st.AddNode(self.graph, self.canvas, radius)
        print("node mode")

        # clear any edge clicking
        self.last_node = -1

        self.draw_graph()

    def draw_graph(self):
        '''Draw the whole graph from scratch. Used when loading a graph'''
        for node in self.graph.nodes(data=True):
            coords = node[-1]['coord']
            self.graph.nodes[node[0]]['obj'] = self.draw_node(coords[0], coords[1])
        for edge in self.graph.edges():
            new_edge_obj = self.draw_edge(edge)
            self.graph[edge[0]][edge[1]]['obj'] = new_edge_obj

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

    # is duplicated in State, should just be in one place?
    def get_nearest_node(self, x, y):
        dist = -1
        index = -1
        for node in self.graph.nodes(data=True):
            curr_coords = node[-1]['coord']
            curr_dist = (curr_coords[0] - x)**2 + (curr_coords[1] - y)**2
            if (curr_dist < dist) or (dist == -1):
                dist = curr_dist
                index = node[0]

        return index

    # maybe belongs in State?
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
        if char == 'e':
            self.mode = ADD_EDGE
            self.state = st.AddEdge(self.graph, self.canvas, radius)
            # clear any edge clicking
            self.last_node = -1
            print("edge mode")

        if char == 'x':
            self.state = st.ColorEdge(self.graph, self.canvas, radius, "red")

        if char == 'u':
            self.state = st.ColorEdge(self.graph, self.canvas, radius, "blue")

        # TODO: implement loading a graph
        #elif char == 'l':
        #    self.graph = nx.Graph()
        #    print("self.graph currently has:", self.graph.number_of_nodes(), "nodes")
        #    self.graph = gutils.load_graph("counter.txt")
        #    print("and now:", self.graph.number_of_nodes(), "nodes")
        #    setup_self.graph()

        elif char == 'n':
            self.mode = ADD_NODE
            self.state = st.AddNode(self.graph, self.canvas, radius)
            # clear any edge clicking
            self.last_node = -1
            print("node mode")

        elif char == 'm':
            self.maximum_matching()

        elif char == 'b':
            self.clear_edges()

        elif char == 'p':
            self.mode = ADD_PATH
            self.state = st.AddPath(self.graph, self.canvas, radius)
            print("path mode")

        elif char == 's':
            gutils.save_graph(self.graph, self.filename)
            print("file saved as", self.filename)

        elif char == 'g':
            self.mode = REMOVE_EDGE
            self.state = st.RemoveEdge(self.graph, self.canvas, radius)
            self.last_node = -1
            print("remove edge mode")
        
        elif char == 'r':
            self.mode = REMOVE_NODE
            self.state = st.RemoveNode(self.graph, self.canvas, radius)
            self.last_node = -1
            print("remove node mode")

    def click(self, event):
        self.state.on_click(event)

    def motion(self, event):
        if self.graph.number_of_nodes() < 1:
            return

        if self.indicator != -1:
            self.canvas.delete(self.indicator)
        index = self.get_nearest_node(event.x, event.y)
        coords = self.graph.nodes[index]['coord']
        self.indicator = self.canvas.create_line(event.x, event.y, coords[0],
                coords[1], fill='green')
