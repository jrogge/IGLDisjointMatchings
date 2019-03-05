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
mode = ADD_NODE
graph = nx.Graph()
node_list = []
new_edge_first = -1
filename = ""

def draw_graph():
    for node in graph.nodes(data=True):
        print("node:", node)
        coords = node[-1]['coord']
        canvas.create_oval(coords[0]-radius,coords[1]-radius,
                coords[0]+radius,coords[1]+radius)
    for edge in graph.edges():
        #print("edge:", edge)
        #print("graph[edge[0]]", graph[edge[0]])
        #print("graph.nodes[edge[0]]", graph.nodes[edge[0]])
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
    canvas.create_oval(x0,y0,x1,y1)
    global indx
    graph.add_node(indx, coord=[x,y])
    indx += 1

def get_nearest_node(x, y):
    dist = -1
    index = -1
    for ind, node in enumerate(node_list):
        curr_dist = (node[0] - x)**2 + (node[1] - y)**2
        if (curr_dist < dist) or (dist == -1):
            dist = curr_dist
            index = ind

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

def add_edge_click(x,y):
    global new_edge_first
    nearest_index = get_nearest_node(x, y)
    if new_edge_first == -1:
        new_edge_first = nearest_index
    else:
        x0 = node_list[new_edge_first][0]
        y0 = node_list[new_edge_first][1]
        x1 = node_list[nearest_index][0]
        y1 = node_list[nearest_index][1]
        new_edge_obj = canvas.create_line(x0,y0,x1,y1)
        graph.add_edge(new_edge_first, nearest_index, obj = new_edge_obj)

        if mode == ADD_EDGE:
            # reset this
            new_edge_first = -1
        elif mode == ADD_PATH:
            new_edge_first = nearest_index


def click(event):
    if mode == ADD_NODE:
        #add_node(indx, coord=[event.x, event.y])
        add_node(event.x, event.y)
    elif (mode == ADD_EDGE) or (mode == ADD_PATH):
        add_edge_click(event.x, event.y)

def motion(event):
    #print("motion!")
    if len(node_list) < 1:
        return

    global indicator # is this bad practice? Probably should wrap this up into a class
    if indicator != -1:
        canvas.delete(indicator)
    index = get_nearest_node(event.x, event.y)
    node = node_list[index]
    indicator = canvas.create_line(event.x, event.y, node[0], node[1], fill='green')


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
graph = gutils.load_graph("counter.txt")
draw_graph()
#load()
#canvas.bind("<Key>", redrawDirectionMarker)
#canvas.bind("<B1-Motion>", drag)
#root.call('wm', 'attributes', '.', '-topmost', True)
root.mainloop()
