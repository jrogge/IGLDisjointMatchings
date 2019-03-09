import networkx as nx
from tkinter import *
import gutils

radius = 3
indicator = -1
indx = 0

MATCHING_COLOR = 'yellow'
ADD_NODE = 0
ADD_EDGE = 1
ADD_PATH = 2
REMOVE_NODE = 3
REMOVE_EDGE = 4
mode = ADD_NODE
graph = nx.Graph()
node_list = []
new_edge_first = -1
filename = ""

def setup_graph():
    for node in graph.nodes(data=True):
        coords = node[-1]['coord']
        add_node(coords[0], coords[1])
    for edge in graph.edges():
        x0 = graph.nodes[edge[0]]['coord'][0]
        y0 = graph.nodes[edge[0]]['coord'][1]
        x1 = graph.nodes[edge[1]]['coord'][0]
        y1 = graph.nodes[edge[1]]['coord'][1]
        new_edge_obj = canvas.create_line(x0,y0,x1,y1)
        graph[edge[0]][edge[1]]['obj'] = new_edge_obj
        graph.add_edge(edge[0], edge[1], obj = new_edge_obj)

def add_node(x, y):
    node_list.append((x, y))
    x0 = x - radius
    y0 = y - radius
    x1 = x + radius
    y1 = y + radius
    new_obj = canvas.create_oval(x0,y0,x1,y1)
    global indx
    graph.add_node(indx, coord=[x,y], obj=new_obj)
    indx += 1

def remove_node(x, y):
    node = get_nearest_node(x,y)
    # delete adjacent edges
    adj_list = graph[node].copy()
    for adj_node in adj_list:
        remove_edge(node, adj_node)
    canvas.delete(graph.nodes[node]['obj'])
    graph.remove_node(node)

def get_nearest_node(x, y):
    dist = -1
    index = -1
    for node in graph.nodes(data=True):
        curr_coords = node[-1]['coord']
        curr_dist = (curr_coords[0] - x)**2 + (curr_coords[1] - y)**2
        if (curr_dist < dist) or (dist == -1):
            dist = curr_dist
            index = node[0]

    return index

def clear_edges():
    # recolor all edges black
    for curr_edge in graph.edges(data=True):
        obj = curr_edge[-1]['obj']
        canvas.itemconfig(obj, fill='black', width=1)

def maximum_matching():
    clear_edges()

    #indicate the matching
    max_matching = nx.max_weight_matching(graph)
    for curr_edge in max_matching:
        extant_edge = graph[curr_edge[0]][curr_edge[1]]
        canvas.itemconfig(extant_edge['obj'], fill=MATCHING_COLOR, width=3)

def key(event):
    char = event.char
    global mode
    global new_edge_first
    if char == 'e':
        mode = ADD_EDGE
        # clear any edge clicking
        new_edge_first = -1
        print("edge mode")
    elif char == 'n':
        print("node mode")
        mode = ADD_NODE
        # clear any edge clicking
        new_edge_first = -1
    elif char == 'm':
        maximum_matching()
    elif char == 'b':
        clear_edges()
    elif char == 'p':
        mode = ADD_PATH
        print("path mode")
    elif char == 's':
        gutils.save_graph(graph, filename)
    elif char == 'g':
        mode = REMOVE_EDGE
        new_edge_first = -1
        print("remove edge mode")
    elif char == 'r':
        mode = REMOVE_NODE
        new_edge_first = -1
        print("remove node mode")

def remove_edge(u, v):
    old_obj = graph[u][v]['obj']
    canvas.delete(old_obj)
    graph.remove_edge(u, v)

def remove_edge_click(x,y):
    global new_edge_first
    nearest_index = get_nearest_node(x, y)
    if new_edge_first == -1:
        new_edge_first = nearest_index
    else:
        remove_edge(new_edge_first, nearest_index)

        if mode == REMOVE_EDGE:
            # reset this
            new_edge_first = -1


def add_edge_click(x,y):
    global new_edge_first
    nearest_index = get_nearest_node(x, y)
    if new_edge_first == -1:
        new_edge_first = nearest_index
    else:
        v0 = graph.nodes[nearest_index]['coord']
        v1 = graph.nodes[new_edge_first]['coord']
        new_edge_obj = canvas.create_line(v0[0],v0[1],v1[0],v1[1])
        graph.add_edge(new_edge_first, nearest_index, obj = new_edge_obj)

        if mode == ADD_EDGE:
            # reset this
            new_edge_first = -1
        elif mode == ADD_PATH:
            new_edge_first = nearest_index


def click(event):
    if mode == ADD_NODE:
        add_node(event.x, event.y)
    elif mode == REMOVE_NODE:
        remove_node(event.x, event.y)
    elif (mode == ADD_EDGE) or (mode == ADD_PATH):
        add_edge_click(event.x, event.y)
    elif (mode == REMOVE_EDGE):
        remove_edge_click(event.x, event.y)

def motion(event):
    #print("motion!")
    if graph.number_of_nodes() < 1:
        return

    global indicator # is this bad practice? Probably should wrap this up into a class
    if indicator != -1:
        canvas.delete(indicator)
    index = get_nearest_node(event.x, event.y)
    coords = graph.nodes[index]['coord']
    indicator = canvas.create_line(event.x, event.y, coords[0], coords[1],
            fill='green')


# Tkinter boilerplate
root = Tk()
#window = Frame(root, width=windowDim, height=windowDim)
window = Frame(root)
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
x = screenwidth /2
y = screenheight/2
root.geometry('%dx%d+%d+%d' % (screenwidth/2, screenwidth, x, y))
window.pack()
canvas = Canvas(window, height=screenheight, width=screenwidth/2)
canvas.pack()

canvas.focus_set()
canvas.bind("<Button-1>", click)
canvas.bind("<Motion>", motion)
canvas.bind("<Key>", key)
######## load graph manually ########
#graph = gutils.load_graph("counter.txt")
#setup_graph()
root.mainloop()
