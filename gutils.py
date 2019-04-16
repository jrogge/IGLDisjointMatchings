import networkx as nx

def save_graph(G, filename):
    '''Writes networkx graph to file using custom format'''
    f = open(filename, 'w')
    nodes = G.nodes(data=True)
    # write vertices coordinates
    for node in nodes:
        coords = node[-1]['coord']
        c_str = ''
        for c in coords[:-1]:
            c_str += str(c) + ' ' 
        c_str += str(coords[-1]) + '\n'
        f.write(c_str)
    f.write('\n')
    # write edge vertices and type
    edges = G.edges(data=True)
    for edge in edges:
        v1 = edge[0]
        v2 = edge[1]
        f.write('%d %d\n'%(v1, v2))
        #type = edge
    f.close()


def load_graph(filename):
    '''Read graph data from a file.
    Returns a networkx graph'''
    new_graph = nx.Graph()
    f = open(filename, 'r')
    lines = f.read().split('\n\n')
    nodes = lines[0]
    edges = lines[1]

    for ind, node in enumerate(nodes.split('\n')):
        vals = [float(coord) for coord in node.split(' ')]
        new_graph.add_node(ind, coord=vals)

    for edge in edges.split('\n'):
        if (edge == ''):
            continue
        data = edge.split(' ')
        new_graph.add_edge(int(data[0]), int(data[1]))

    f.close()
    return new_graph

def get_bounding_box(graph):
    ''' Get a bounding box for the coordinates of the graph. Assumes that the
    node coordinate data is saved as 'coord' in node data'''
    min_x = -1
    min_y = -1
    max_x = -1
    max_y = -1
    for node in graph.nodes(data=True):
        coords = node[-1]['coord']
        # check x
        if (coords[0] < min_x or min_x == -1):
            min_x = coords[0]
        elif (coords[0] > max_x or max_x == -1):
            max_x = coords[0]

        # check y
        if (coords[1] < min_y or min_y == -1):
            min_y = coords[1]
        elif (coords[1] > max_y or max_y == -1):
            max_y = coords[1]
    return ((min_x, min_y), (max_x, max_y))

def scale_graph(graph, factor):
    ''' Scale node coordinates by a factor. Python is pass by reference so we
    do not need to return a modified graph.'''
    for node in graph.nodes():
        graph.nodes[node]['coord'][0] *= factor
        graph.nodes[node]['coord'][1] *= factor

def translate_graph(graph, delta):
    ''' Translate node coordinates by a vector delta. Python is pass by
    reference so we do not need to return a modified graph.'''
    for node in graph.nodes():
        graph.nodes[node]['coord'][0] += delta[0]
        graph.nodes[node]['coord'][1] += delta[1]
